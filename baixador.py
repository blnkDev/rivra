import yt_dlp
import yt_dlp.version as yt_dlp_version
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
import threading
import re
import json
import requests
from io import BytesIO
from PIL import Image

# Configuração Dark Mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def _obter_config_dir():
    """Retorna o diretório de configurações, preferindo AppData/Local, com fallback para home."""
    # Tenta LOCALAPPDATA primeiro (Windows padrão)
    local_app = os.environ.get('LOCALAPPDATA', '')
    if local_app and os.path.isdir(local_app):
        return os.path.join(local_app, 'YtDownloader')
    # Fallback: pasta oculta na home do usuário
    return os.path.join(os.path.expanduser("~"), '.ytdownloader')

def carregar_config():
    """Carrega as configurações salvas do usuário."""
    try:
        config_file = os.path.join(_obter_config_dir(), 'config.json')
        if os.path.isfile(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def salvar_config(novos_dados):
    """Salva as configurações do usuário (merge com o existente)."""
    try:
        config_dir = _obter_config_dir()
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, 'config.json')
        # Merge para não apagar outras configurações
        config_atual = {}
        if os.path.isfile(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_atual = json.load(f)
            except Exception:
                pass
        config_atual.update(novos_dados)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_atual, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# Determina pasta padrão persistente
config_salva = carregar_config()
pasta_salva = config_salva.get("pasta_destino", "")
pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
# Se a pasta salva existir, usa ela; senão usa Downloads; senão o diretório do exe
pasta_destino = (
    pasta_salva if (pasta_salva and os.path.isdir(pasta_salva))
    else (pasta_downloads if os.path.isdir(pasta_downloads)
          else os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)))
)

# Regex para detecção de URLs suportadas (YouTube, TikTok, Instagram, X/Twitter, SoundCloud, etc.)
PADRAO_URL_SUPORTADA = re.compile(
    r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|tiktok\.com|instagram\.com|twitter\.com|x\.com|soundcloud\.com|facebook\.com|fb\.watch|vimeo\.com|twitch\.tv|pin\.it|pinterest\.com)/.+',
    re.IGNORECASE
)

def remover_ansi(texto):
    """Remove códigos de escape ANSI."""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', str(texto))

def formatar_segundos(segundos):
    """Formata segundos em HH:MM:SS ou MM:SS."""
    if not segundos or not isinstance(segundos, (int, float)):
        return "N/A"
    segundos = int(segundos)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return f"{minutos:02d}:{segs:02d}"

def caminho_binario(nome_executavel):
    """Localiza executáveis auxiliares como ffmpeg.exe e deno.exe."""
    diretorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(diretorio_base, 'ffmpeg', nome_executavel)
    if os.path.isfile(caminho):
        return caminho
    caminho_direto = os.path.join(diretorio_base, nome_executavel)
    if os.path.isfile(caminho_direto):
        return caminho_direto
    return nome_executavel

def caminho_icone():
    """Localiza o arquivo de ícone favicon.ico."""
    diretorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(diretorio_base, 'favicon.ico')
    return caminho if os.path.isfile(caminho) else None

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Janela Compacta e Elegante
        self.title("Rivra")
        self.geometry("620x540")
        self.resizable(False, False)
        self.centralizar_janela()

        # Ícone
        icone = caminho_icone()
        if icone:
            try:
                self.iconbitmap(icone)
            except Exception:
                pass

        # Variáveis
        self.pasta_destino = pasta_destino
        self.formato_var = ctk.StringVar(value="mp4")
        self.qualidade_var = ctk.StringVar(value="Melhor Disponível")
        self.baixar_playlist_var = ctk.BooleanVar(value=False)
        self.em_download = False
        self.cancelar_solicitado = False
        self.timer_busca_previa = None
        self.ultimo_url_buscado = ""
        self.preview_image_ref = None

        self.criar_widgets()

        # Detecção Automática ao Focar na Janela (Auto-Paste)
        self.bind("<FocusIn>", self.ao_focar_janela)

        # Verificação de atualização do yt-dlp em background
        threading.Thread(target=self._verificar_atualizacao_ytdlp, daemon=True).start()

    def centralizar_janela(self):
        largura, altura = 620, 540
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_widgets(self):
        # 0. Banner de atualização do yt-dlp (oculto por padrão)
        self.update_banner = ctk.CTkFrame(self, fg_color="#78350f", corner_radius=0, height=32)
        # Não é empacotado aqui — só aparece quando há update disponível

        self.lbl_update_texto = ctk.CTkLabel(
            self.update_banner,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#fef3c7",
            anchor="w"
        )
        self.lbl_update_texto.pack(side="left", padx=(12, 8), fill="y")

        self.btn_update_ytdlp = ctk.CTkButton(
            self.update_banner,
            text="⬆ Atualizar",
            width=90,
            height=22,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#d97706",
            hover_color="#b45309",
            corner_radius=4,
            command=self._executar_atualizacao_ytdlp
        )
        self.btn_update_ytdlp.pack(side="right", padx=(0, 10))

        self.btn_dismiss_update = ctk.CTkButton(
            self.update_banner,
            text="✕",
            width=22,
            height=22,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color="#92400e",
            corner_radius=4,
            command=lambda: self.update_banner.pack_forget()
        )
        self.btn_dismiss_update.pack(side="right", padx=(0, 4))

        # 1. Entrada de Link Direta
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=20, pady=(20, 8))

        self.entrada_url = ctk.CTkEntry(
            self.url_frame,
            placeholder_text="Cole o link aqui (YouTube, TikTok, Reels, X, SoundCloud...)",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entrada_url.bind("<KeyRelease>", self.ao_digitar_url)

        self.btn_colar = ctk.CTkButton(
            self.url_frame,
            text="📋 Colar",
            width=75,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            command=self.colar_link
        )
        self.btn_colar.pack(side="right")

        # 2. Card de Prévia (Surge apenas ao detectar o vídeo/áudio)
        self.preview_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#1e293b")
        self.preview_frame.pack(fill="x", padx=20, pady=(0, 8))
        self.preview_frame.pack_forget()

        self.thumb_label = ctk.CTkLabel(self.preview_frame, text="", width=105, height=60, corner_radius=6)
        self.thumb_label.pack(side="left", padx=10, pady=8)

        self.preview_info_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.preview_info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=8)

        self.lbl_preview_titulo = ctk.CTkLabel(
            self.preview_info_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
            wraplength=440,
            justify="left"
        )
        self.lbl_preview_titulo.pack(fill="x", anchor="w")

        self.lbl_preview_detalhes = ctk.CTkLabel(
            self.preview_info_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
            anchor="w"
        )
        self.lbl_preview_detalhes.pack(fill="x", anchor="w", pady=(1, 0))

        self.chk_playlist = ctk.CTkCheckBox(
            self.preview_info_frame,
            text="Baixar playlist completa",
            variable=self.baixar_playlist_var,
            font=ctk.CTkFont(size=11),
            checkbox_height=18,
            checkbox_width=18
        )
        self.chk_playlist.pack(anchor="w", pady=(3, 0))
        self.chk_playlist.pack_forget()

        # 3. Controles Funcionais (Formato & Qualidade)
        self.controles_frame = ctk.CTkFrame(self, corner_radius=8)
        self.controles_frame.pack(fill="x", padx=20, pady=0)

        self.linha_formato = ctk.CTkFrame(self.controles_frame, fg_color="transparent")
        self.linha_formato.pack(fill="x", padx=12, pady=(10, 6))

        self.btn_formato = ctk.CTkSegmentedButton(
            self.linha_formato,
            values=["🎬 MP4 (Vídeo)", "🎵 MP3 (Áudio)"],
            command=self.ao_mudar_formato,
            height=34,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_formato.set("🎬 MP4 (Vídeo)")
        self.btn_formato.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.menu_qualidade = ctk.CTkOptionMenu(
            self.linha_formato,
            variable=self.qualidade_var,
            values=["Melhor Disponível", "1080p (Full HD)", "720p (HD)", "480p (SD)"],
            height=34,
            font=ctk.CTkFont(size=12)
        )
        self.menu_qualidade.pack(side="right", fill="x", expand=True)

        # Pasta de Destino (Linha 2)
        self.linha_pasta = ctk.CTkFrame(self.controles_frame, fg_color="transparent")
        self.linha_pasta.pack(fill="x", padx=12, pady=(0, 10))

        self.lbl_caminho_pasta = ctk.CTkLabel(
            self.linha_pasta,
            text=self.pasta_destino,
            anchor="w",
            fg_color="#0f172a",
            corner_radius=6,
            height=32,
            padx=10,
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8"
        )
        self.lbl_caminho_pasta.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_alterar_pasta = ctk.CTkButton(
            self.linha_pasta,
            text="📁",
            width=38,
            height=32,
            font=ctk.CTkFont(size=14),
            fg_color="#334155",
            hover_color="#475569",
            command=self.escolher_pasta
        )
        self.btn_alterar_pasta.pack(side="left", padx=(0, 4))

        self.btn_abrir_pasta = ctk.CTkButton(
            self.linha_pasta,
            text="📂",
            width=38,
            height=32,
            font=ctk.CTkFont(size=14),
            fg_color="#334155",
            hover_color="#475569",
            command=self.abrir_pasta_destino
        )
        self.btn_abrir_pasta.pack(side="left")

        # 4. Botão Principal de Ação
        self.botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.botoes_frame.pack(fill="x", padx=20, pady=(10, 6))

        self.btn_baixar = ctk.CTkButton(
            self.botoes_frame,
            text="⬇ Baixar",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=8,
            command=self.iniciar_download
        )
        self.btn_baixar.pack(side="left", fill="x", expand=True)

        self.btn_cancelar = ctk.CTkButton(
            self.botoes_frame,
            text="❌ Cancelar",
            height=42,
            width=100,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            corner_radius=8,
            command=self.solicitar_cancelamento
        )
        self.btn_cancelar.pack(side="right", padx=(8, 0))
        self.btn_cancelar.pack_forget()

        # 5. Barra de Progresso e Status
        self.progresso_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progresso_frame.pack(fill="x", padx=20, pady=(2, 6))

        self.barra_progresso = ctk.CTkProgressBar(self.progresso_frame, height=8, corner_radius=4)
        self.barra_progresso.pack(fill="x", pady=(0, 3))
        self.barra_progresso.set(0)

        self.lbl_status = ctk.CTkLabel(
            self.progresso_frame,
            text="Pronto",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
            anchor="w"
        )
        self.lbl_status.pack(fill="x")

        # 6. Log Compacto e Discreto
        self.caixa_log = ctk.CTkTextbox(
            self,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="#0f172a",
            text_color="#cbd5e1",
            corner_radius=8
        )
        self.caixa_log.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    # ── Atualização do yt-dlp ─────────────────────────────────────────────────

    def _verificar_atualizacao_ytdlp(self):
        """Verifica se há uma versão mais nova do yt-dlp no PyPI (roda em background)."""
        try:
            resp = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=6)
            if resp.status_code != 200:
                return
            ultima_versao = resp.json()["info"]["version"]
            versao_atual = yt_dlp_version.__version__

            # Normaliza para comparação: "2026.8.19" → (2026, 8, 19)
            def _parsear(v):
                try:
                    return tuple(int(p) for p in str(v).split("."))
                except Exception:
                    return (0,)

            if _parsear(ultima_versao) > _parsear(versao_atual):
                def _mostrar_banner():
                    self.lbl_update_texto.configure(
                        text=f"⚠ yt-dlp desatualizado: {versao_atual}  →  {ultima_versao}"
                    )
                    self.update_banner.pack(fill="x", before=self.url_frame)
                self.after(0, _mostrar_banner)
        except Exception:
            pass  # Falha silenciosa (sem internet, timeout, etc.)

    def _executar_atualizacao_ytdlp(self):
        """Atualiza o yt-dlp via pip em background e notifica o usuário."""
        self.btn_update_ytdlp.configure(state="disabled", text="Atualizando...")
        self.log("Atualizando yt-dlp, aguarde...", "status")

        def _rodar():
            try:
                import subprocess
                python_exe = sys.executable
                resultado = subprocess.run(
                    [python_exe, "-m", "pip", "install", "-U", "yt-dlp", "--quiet"],
                    capture_output=True, text=True, timeout=60
                )
                if resultado.returncode == 0:
                    # Recarrega a versão instalada para confirmar
                    import importlib
                    import yt_dlp.version as _v
                    importlib.reload(_v)
                    nova_versao = _v.__version__

                    def _ok():
                        self.log(f"yt-dlp atualizado para {nova_versao} ✔", "ok")
                        self.update_banner.pack_forget()
                        messagebox.showinfo(
                            "yt-dlp Atualizado",
                            f"Atualizado com sucesso para v{nova_versao}!\n"
                            "Reinicie o app para que as mudanças entrem em vigor."
                        )
                    self.after(0, _ok)
                else:
                    erro = resultado.stderr.strip() or "Erro desconhecido."
                    def _falhou():
                        self.log(f"Falha na atualização: {erro}", "erro")
                        self.btn_update_ytdlp.configure(state="normal", text="⬆ Atualizar")
                        messagebox.showerror("Erro ao atualizar", f"Não foi possível atualizar o yt-dlp:\n{erro}")
                    self.after(0, _falhou)
            except Exception as e:
                def _ex():
                    self.log(f"Erro ao atualizar yt-dlp: {e}", "erro")
                    self.btn_update_ytdlp.configure(state="normal", text="⬆ Atualizar")
                self.after(0, _ex)

        threading.Thread(target=_rodar, daemon=True).start()

    # ── Área de transferência / URL ───────────────────────────────────────────

    def ao_focar_janela(self, event=None):
        """Detecção automática de link na área de transferência ao focar no app."""
        if self.em_download:
            return
        try:
            conteudo = self.clipboard_get().strip()
            # Se for uma URL válida diferente da atual
            if conteudo and PADRAO_URL_SUPORTADA.match(conteudo) and conteudo != self.entrada_url.get().strip():
                self.entrada_url.delete(0, "end")
                self.entrada_url.insert(0, conteudo)
                self.agendar_busca_previa()
        except Exception:
            pass

    def colar_link(self):
        """Cola o link da área de transferência manualmente."""
        try:
            conteudo = self.clipboard_get()
            if conteudo:
                self.entrada_url.delete(0, "end")
                self.entrada_url.insert(0, conteudo.strip())
                self.agendar_busca_previa()
        except Exception:
            pass

    def ao_digitar_url(self, event=None):
        """Dispara busca de prévia com debounce."""
        self.agendar_busca_previa()

    def agendar_busca_previa(self):
        """Debounce de 500ms."""
        if self.timer_busca_previa:
            self.after_cancel(self.timer_busca_previa)
        self.timer_busca_previa = self.after(500, self.buscar_previa_async)

    def buscar_previa_async(self):
        """Busca metadados em background para qualquer link suportado."""
        url = self.entrada_url.get().strip()
        if not url or url == self.ultimo_url_buscado or not (url.startswith("http://") or url.startswith("https://")):
            return

        self.ultimo_url_buscado = url
        thread = threading.Thread(target=self._obter_metadados, args=(url,), daemon=True)
        thread.start()

    def _obter_metadados(self, url):
        """Obtém metadados rápidos e imagem da capa (YouTube, TikTok, Reels, SoundCloud, etc)."""
        try:
            deno_path = caminho_binario('deno.exe')
            js_runtimes_config = {'deno': {'path': deno_path}} if os.path.isfile(deno_path) else {'deno': {}}

            ydl_opts = {
                'skip_download': True,
                'extract_flat': 'in_playlist',
                'quiet': True,
                'no_warnings': True,
                'js_runtimes': js_runtimes_config,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            if not info:
                return

            titulo = info.get('title', 'Mídia detectada')
            canal = (
                info.get('uploader') or info.get('channel') or
                info.get('artist') or info.get('creator') or
                info.get('extractor_key', '')
            )
            duracao = formatar_segundos(info.get('duration'))
            is_playlist = 'entries' in info or 'list=' in url

            # --- Resolução de thumbnail para múltiplas plataformas ---
            # Prioridade: artwork_url (SoundCloud) > thumbnail > melhor de thumbnails[]
            thumb_url = (
                info.get('artwork_url') or
                info.get('thumbnail') or
                self._melhor_thumbnail(info.get('thumbnails'))
            )

            thumb_img = None
            if thumb_url:
                try:
                    resp = requests.get(thumb_url, timeout=5)
                    if resp.status_code == 200:
                        pil_img = Image.open(BytesIO(resp.content))
                        pil_img.thumbnail((105, 60), Image.Resampling.LANCZOS)
                        thumb_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
                except Exception:
                    thumb_img = None

            def _atualizar_card():
                self.lbl_preview_titulo.configure(text=titulo[:75] + ("..." if len(titulo) > 75 else ""))
                detalhes = f"{canal} • {duracao}" if (canal and duracao != "N/A") else (canal or duracao)
                if is_playlist:
                    qtd = len(info.get('entries', [])) if 'entries' in info else "Vários"
                    detalhes += f" • Playlist ({qtd} itens)"
                    self.chk_playlist.pack(anchor="w", pady=(3, 0))
                    self.chk_playlist.configure(text=f"Baixar playlist completa ({qtd} itens)")
                else:
                    self.chk_playlist.pack_forget()

                self.lbl_preview_detalhes.configure(text=detalhes)

                if thumb_img:
                    self.preview_image_ref = thumb_img
                    self.thumb_label.configure(image=thumb_img, text="")
                else:
                    self.thumb_label.configure(image=None, text="🎬")

                self.preview_frame.pack(fill="x", padx=20, pady=(0, 8), after=self.url_frame)

            self.after(0, _atualizar_card)

        except Exception:
            pass

    def _melhor_thumbnail(self, thumbnails):
        """Seleciona a melhor URL de thumbnail de uma lista (maior resolução)."""
        if not thumbnails or not isinstance(thumbnails, list):
            return None
        # Filtra as que têm URL e tenta pegar a de maior resolução
        validas = [t for t in thumbnails if isinstance(t, dict) and t.get('url')]
        if not validas:
            return None
        # Ordena por largura*altura (maior primeiro), sem erros se não tiver dimensão
        def _area(t):
            try:
                return (t.get('width') or 0) * (t.get('height') or 0)
            except Exception:
                return 0
        validas.sort(key=_area, reverse=True)
        return validas[0]['url']

    def ao_mudar_formato(self, valor):
        """Atualiza a lista de qualidades conforme o formato."""
        if "MP3" in valor:
            self.formato_var.set("mp3")
            self.menu_qualidade.configure(values=["320 kbps (Alta)", "192 kbps (Padrão)", "128 kbps (Leve)"])
            self.qualidade_var.set("192 kbps (Padrão)")
        else:
            self.formato_var.set("mp4")
            self.menu_qualidade.configure(values=["Melhor Disponível", "1080p (Full HD)", "720p (HD)", "480p (SD)"])
            self.qualidade_var.set("Melhor Disponível")

    def escolher_pasta(self):
        """Abre o seletor de pasta e salva a preferência do usuário."""
        pasta = filedialog.askdirectory(title="Pasta de destino", initialdir=self.pasta_destino)
        if pasta:
            self.pasta_destino = pasta
            self.lbl_caminho_pasta.configure(text=pasta)
            salvar_config({"pasta_destino": pasta})
            self.log(f"Pasta salva: {pasta}", "info")

    def abrir_pasta_destino(self):
        """Abre a pasta no Explorador."""
        if os.path.isdir(self.pasta_destino):
            os.startfile(self.pasta_destino)

    def log(self, msg, tipo="info"):
        """Escreve mensagem no console de logs."""
        prefixos = {
            "info": "• ",
            "ok": "✔ ",
            "erro": "✖ ",
            "status": "→ ",
            "aviso": "▲ "
        }
        texto_formatado = f"{prefixos.get(tipo, '')}{msg}\n"

        def _inserir():
            self.caixa_log.insert("end", texto_formatado)
            self.caixa_log.see("end")

        self.after(0, _inserir)

    def atualizar_progresso_ui(self, percentual=0.0, texto_status="Pronto"):
        """Atualiza barra de progresso e texto de status."""
        def _atualizar():
            self.barra_progresso.set(max(0.0, min(1.0, percentual / 100.0)))
            self.lbl_status.configure(text=texto_status)
        self.after(0, _atualizar)

    def progresso_hook(self, d):
        """Hook invocado pelo yt-dlp."""
        if self.cancelar_solicitado:
            raise yt_dlp.utils.DownloadCancelled("Download cancelado.")

        if d['status'] == 'downloading':
            total = remover_ansi(d.get('_percent_str', '0%')).strip()
            velocidade = remover_ansi(d.get('_speed_str', 'N/A')).strip()
            eta = remover_ansi(d.get('_eta_str', 'N/A')).strip()

            percent_num = 0.0
            try:
                limpo = total.replace('%', '').strip()
                percent_num = float(limpo)
            except (ValueError, AttributeError):
                total_b = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                down_b = d.get('downloaded_bytes', 0)
                if total_b > 0:
                    percent_num = (down_b / total_b) * 100.0

            idx = d.get('playlist_index')
            count = d.get('playlist_count')
            prefixo = f"[{idx}/{count}] " if idx and count else ""

            self.atualizar_progresso_ui(
                percent_num,
                f"{prefixo}Baixando: {total} • {velocidade} • Restante: {eta}"
            )
        elif d['status'] == 'finished':
            self.atualizar_progresso_ui(100.0, "Processando mídia e embutindo capa...")

    def solicitar_cancelamento(self):
        """Cancela o download."""
        if self.em_download:
            self.cancelar_solicitado = True
            self.btn_cancelar.configure(state="disabled", text="Cancelando...")
            self.log("Cancelamento solicitado.", "aviso")

    def _executar_download(self, url, formato, qualidade, destino, baixar_playlist):
        """Thread de download universal com alta velocidade e injeção de capas."""
        try:
            ffmpeg_path = caminho_binario('ffmpeg.exe')
            deno_path = caminho_binario('deno.exe')

            js_runtimes_config = {'deno': {'path': deno_path}} if os.path.isfile(deno_path) else {'deno': {}}

            ydl_opts = {
                'outtmpl': os.path.join(destino, '%(playlist_title)s/%(title)s.%(ext)s' if baixar_playlist else '%(title)s.%(ext)s'),
                'ffmpeg_location': ffmpeg_path,
                'progress_hooks': [self.progresso_hook],
                'concurrent_fragment_downloads': 8,
                'http_chunk_size': 10485760,
                'js_runtimes': js_runtimes_config,
                'noplaylist': not baixar_playlist,
                'writethumbnail': True,
                'nocheckcertificate': True,
                'retries': 10,
                'fragment_retries': 10,
                'quiet': True,
                'no_warnings': False,
            }

            if formato == "mp3":
                bitrate = "192"
                if "320" in qualidade:
                    bitrate = "320"
                elif "128" in qualidade:
                    bitrate = "128"

                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate},
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
                ]
                ydl_opts['postprocessor_args'] = {
                    'ExtractAudio': ['-id3v2_version', '3']
                }
            else: # mp4
                if "1080p" in qualidade:
                    formato_str = (
                        'bestvideo[height<=1080][vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/'
                        'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                    )
                elif "720p" in qualidade:
                    formato_str = (
                        'bestvideo[height<=720][vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/'
                        'bestvideo[height<=720]+bestaudio/best[height<=720]'
                    )
                elif "480p" in qualidade:
                    formato_str = (
                        'bestvideo[height<=480][vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/'
                        'bestvideo[height<=480]+bestaudio/best[height<=480]'
                    )
                else:
                    formato_str = (
                        'bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/'
                        'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/'
                        'bestvideo[ext=mp4]+bestaudio[ext=m4a]/'
                        'bestvideo+bestaudio/best'
                    )

                ydl_opts['format'] = formato_str
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'] = [
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
                ]
                ydl_opts['postprocessor_args'] = {
                    'merger': ['-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart']
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'Mídia') if info else 'Mídia'
                self.log(f"Salvo: {titulo}", "ok")

            if not self.cancelar_solicitado:
                self.atualizar_progresso_ui(100.0, "Download concluído com sucesso!")
                self.after(0, lambda: self.entrada_url.delete(0, "end"))
                self.after(0, lambda: messagebox.showinfo("Sucesso", f"Download concluído!\nSalvo em: {destino}"))

        except yt_dlp.utils.DownloadCancelled:
            self.log("Download cancelado pelo usuário.", "aviso")
            self.atualizar_progresso_ui(0.0, "Cancelado")
            self.after(0, lambda: messagebox.showinfo("Cancelado", "O download foi cancelado."))

        except Exception as e:
            if self.cancelar_solicitado or "cancelado" in str(e).lower():
                self.log("Download cancelado.", "aviso")
                self.atualizar_progresso_ui(0.0, "Cancelado")
            else:
                msg_erro = remover_ansi(str(e))
                self.log(f"Erro: {msg_erro}", "erro")
                self.atualizar_progresso_ui(0.0, "Falha")
                self.after(0, lambda: messagebox.showerror("Erro", f"Falha no download:\n{msg_erro}"))

        finally:
            def _restaurar():
                self.em_download = False
                self.cancelar_solicitado = False
                self.entrada_url.configure(state="normal")
                self.btn_colar.configure(state="normal")
                self.btn_baixar.configure(state="normal", text="⬇ Baixar")
                self.btn_cancelar.configure(state="normal", text="❌ Cancelar")
                self.btn_cancelar.pack_forget()
                self.btn_alterar_pasta.configure(state="normal")
            self.after(0, _restaurar)

    def iniciar_download(self):
        """Inicia o download."""
        if self.em_download:
            return

        url = self.entrada_url.get().strip()
        formato = self.formato_var.get()
        qualidade = self.qualidade_var.get()
        destino = self.pasta_destino
        baixar_playlist = self.baixar_playlist_var.get()

        if not url:
            messagebox.showwarning("Aviso", "Por favor, cole um link de vídeo ou música.")
            return

        if not destino or not os.path.isdir(destino):
            messagebox.showwarning("Aviso", "Selecione uma pasta de destino válida.")
            return

        self.em_download = True
        self.cancelar_solicitado = False
        self.entrada_url.configure(state="disabled")
        self.btn_colar.configure(state="disabled")
        self.btn_baixar.configure(state="disabled", text="⏳ Baixando...")
        self.btn_alterar_pasta.configure(state="disabled")

        self.btn_cancelar.pack(side="right", padx=(8, 0))
        self.barra_progresso.set(0)
        self.lbl_status.configure(text="Conectando...")

        self.log(f"Iniciando: {url} ({formato.upper()} • {qualidade})", "status")

        thread = threading.Thread(
            target=self._executar_download,
            args=(url, formato, qualidade, destino, baixar_playlist),
            daemon=True
        )
        thread.start()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
