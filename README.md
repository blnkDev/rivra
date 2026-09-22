<div align="center">

  <img src="docs/logo.png" alt="Rivra Logo" width="130" />

  # Rivra

  **Baixador multimídia moderno, rápido e intuitivo para Windows**  
  Construído com Python, CustomTkinter e o poder do [yt-dlp](https://github.com/yt-dlp/yt-dlp).

  <p>
    <a href="https://github.com/blnkDev/Yt-Downloader/releases/latest">
      <img src="https://img.shields.io/badge/Download-Windows%20(.exe)-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Download Windows" />
    </a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=flat-square" alt="CustomTkinter" />
    <img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=flat-square" alt="yt-dlp" />
    <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License MIT" />
  </p>

</div>

---

## 📖 Visão Geral

O **Rivra** é um aplicativo desktop para Windows projetado para baixar vídeos e músicas de mais de 1.000 plataformas com facilidade, velocidade e uma interface moderna em Dark Mode. Sem necessidade de usar terminal ou configurar comandos.

---

## 📦 Como Baixar e Usar (Usuário Comum)

Para quem quer apenas usar o programa sem instalar Python:

1. Acesse a aba de [**Releases**](https://github.com/blnkDev/Yt-Downloader/releases).
2. Baixe a versão mais recente do executável (`Rivra.exe` ou `Rivra.zip`).
3. Execute o aplicativo e comece a baixar!

---

## ✨ Funcionalidades

- **Vídeo em Alta Definição (MP4):** Resoluções até 1080p Full HD com áudio integrado (H.264 + AAC).
- **Extração de Áudio (MP3):** Escolha de taxas de bits em 128 kbps, 192 kbps e 320 kbps (alta fidelidade).
- **Pré-visualização Instantânea:** Carrega thumbnail, título, canal e duração assim que o link é inserido.
- **Detecção Automática (Auto-Paste):** Ao focar na janela do app com um link copiado, ele é preenchido e analisado automaticamente.
- **Suporte a Playlists:** Detecta e baixa listas de reprodução completas organizadas em pastas.
- **Metadados e Capas Embutidos:** Injeta capa do álbum e tags ID3 diretamente nos arquivos via FFmpeg.
- **Downloads Acelerados:** Segmentação em até 8 conexões simultâneas para máxima velocidade.
- **Atualização Automática do yt-dlp:** Verifica se há atualizações do motor ao iniciar e permite atualizar em 1 clique.
- **Pasta Memorizada:** Salva sua pasta de destino preferida para as próximas utilizações.

---

## 🌐 Plataformas Suportadas

Compatível com mais de 1.000 sites através do motor `yt-dlp`:

| Plataforma | Vídeo | Áudio |
|---|:---:|:---:|
| **YouTube** (Vídeos, Shorts, Playlists) | Sim | Sim |
| **TikTok** | Sim | Sim |
| **Instagram** (Reels, Posts) | Sim | Sim |
| **X / Twitter** | Sim | Sim |
| **SoundCloud** | — | Sim |
| **Vimeo** | Sim | Sim |
| **Twitch** (Clipes, VODs) | Sim | Sim |
| **Facebook** | Sim | Sim |

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Finalidade |
|---|---|---|
| **Interface Gráfica** | [CustomTkinter](https://customtkinter.tomschimansky.com/) | UI fluida e responsiva em Dark Mode |
| **Motor de Extração** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Parser e download multimídia |
| **Processamento de Mídia** | [FFmpeg](https://ffmpeg.org/) | Muxing de faixas, conversão de áudio e injeção de capas |
| **Manipulação de Imagens** | [Pillow](https://pypi.org/project/Pillow/) | Renderização das capas e miniaturas |
| **Requisições HTTP** | [Requests](https://pypi.org/project/requests/) | Download de capas e verificação de versões |
| **Empacotamento** | [PyInstaller](https://pyinstaller.org/) | Compilação em executável standalone |

---

## 💻 Executando a partir do Código-Fonte

### Pré-requisitos
- Python 3.10 ou superior
- Binários do FFmpeg na pasta `ffmpeg/`

```bash
# 1. Clone o repositório
git clone https://github.com/blnkDev/Yt-Downloader.git
cd Yt-Downloader

# 2. Crie e ative o ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o aplicativo
python baixador.py
```

---

## 🔨 Gerando o Executável (.exe)

Caso queira compilar seu próprio `.exe`:

```bash
pip install pyinstaller
python -m PyInstaller --clean baixador.spec
```

O executável pronto estará em `dist/baixador.exe`.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
