# ⚡ Media Downloader Pro

Aplicativo moderno, rápido e poderoso para baixar vídeos e músicas de **mais de 1000 plataformas** (YouTube, TikTok, Instagram, X/Twitter, SoundCloud e muito mais), com interface gráfica elegante em **Dark Mode** usando Python, CustomTkinter e yt-dlp.

---

## ✨ Funcionalidades

- 🎬 **Vídeos em MP4:** Suporte a resoluções desde 480p até 1080p Full HD (codec H.264 + AAC).
- 🎵 **Músicas em MP3:** Extração de áudio com seleção de qualidade (320 kbps, 192 kbps, 128 kbps).
- 🌐 **Suporte Multiplataforma:** YouTube, TikTok, Instagram Reels, X/Twitter, SoundCloud, Facebook, Vimeo, Twitch e outros 1000+ sites via yt-dlp.
- 🖼️ **Pré-Visualização em Tempo Real:** Carrega automaticamente thumbnail, título, canal e duração ao colar o link.
- 📋 **Auto-Paste:** Detecta links copiados na área de transferência ao focar na janela e preenche automaticamente.
- 🎨 **Injeção de Capa e Metadados:** Embutimento automático da capa oficial e tags ID3 em MP3 e MP4.
- 📑 **Suporte a Playlists:** Detecção inteligente e opção de baixar playlists completas em pastas organizadas.
- ⚡ **Alta Velocidade:** Até 8 conexões concorrentes e chunks de 10 MB para download acelerado.
- 🔄 **Auto-Update do yt-dlp:** Verifica e instala atualizações do motor de download automaticamente em background.
- 💾 **Pasta Persistente:** Lembra a última pasta de destino escolhida entre sessões.
- ⏹️ **Botão Cancelar:** Interrompe downloads em andamento a qualquer momento.
- 🌙 **Interface Dark Mode:** Visual moderno estilo Windows 11 com CustomTkinter.
- 📦 **Executável Portátil (.exe):** Roda sem instalar Python, FFmpeg ou Deno separadamente.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| [Python 3.12+](https://www.python.org/) | Linguagem principal |
| [CustomTkinter](https://customtkinter.tomschimansky.com/) | Interface gráfica Dark Mode |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Motor de extração e download |
| [FFmpeg](https://ffmpeg.org/) | Processamento de mídia, conversão e merge |
| [Pillow](https://pypi.org/project/Pillow/) | Processamento de thumbnails |
| [Requests](https://pypi.org/project/requests/) | Fetch de thumbnails e verificação de updates |
| [PyInstaller](https://pyinstaller.org/) | Geração do executável standalone |

---

## 🚀 Como Executar (via código fonte)

### Pré-requisitos
- Python 3.10 ou superior
- FFmpeg na pasta `ffmpeg/` do projeto

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/blnkDev/Yt-Downloader.git
   cd Yt-Downloader
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo:**
   ```bash
   python baixador.py
   ```

---

## 📦 Como Gerar o Executável (.exe)

```bash
pip install pyinstaller
python -m PyInstaller --clean baixador.spec
```

O executável será gerado em `dist/baixador.exe` com ícone e todos os componentes embutidos.

---

## 🤝 Contribuições

Sinta-se à vontade para abrir **Issues** ou enviar um **Pull Request**. Toda ajuda é bem-vinda!

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
