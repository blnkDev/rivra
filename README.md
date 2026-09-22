<div align="center">

  <img src="docs/logo.png" alt="Rivra Logo" width="140" />

  # Rivra

  **Baixador multimídia moderno e veloz para Windows**  
  Construído com Python, CustomTkinter e o poder do [yt-dlp](https://github.com/yt-dlp/yt-dlp).

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=flat-square" alt="CustomTkinter" />
    <img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=flat-square" alt="yt-dlp" />
    <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License MIT" />
  </p>

</div>

---

## Visão Geral

O **Rivra** é um aplicativo desktop projetado para proporcionar uma experiência fluida, rápida e elegante ao baixar vídeos e músicas da internet. Com interface moderna em Dark Mode, dispensa qualquer uso de terminal e oferece controle total sobre qualidade, formatos e metadados.

---

## Funcionalidades

- **Download de Vídeo (MP4):** Suporte a resoluções até 1080p Full HD com áudio integrado (H.264 + AAC).
- **Download de Áudio (MP3):** Extração com taxas de bits selecionáveis (128 kbps, 192 kbps e 320 kbps).
- **Pré-visualização em Tempo Real:** Carregamento automático de miniatura, título, canal e duração ao inserir um link.
- **Detecção Automática (Auto-Paste):** Ao focar na janela do app com um link copiado na área de transferência, ele é colado e analisado automaticamente.
- **Suporte a Playlists:** Identificação e download de playlists completas com organização automática em pastas.
- **Injeção de Metadados e Capas:** Gravação automática de tags ID3 e capa nos arquivos de áudio e vídeo via FFmpeg.
- **Downloads Concorrentes Acelerados:** Segmentação de download em até 8 fragmentos simultâneos.
- **Atualização Automática do yt-dlp:** Checagem silenciosa de novas versões do motor com opção de atualização em um clique direto na interface.
- **Pasta de Destino Persistente:** O aplicativo memoriza sua pasta preferida entre inicializações.

---

## Plataformas Suportadas

Graças ao motor `yt-dlp`, o Rivra oferece suporte a mais de 1.000 serviços, incluindo:

| Plataforma | Suporte a Vídeo | Suporte a Áudio |
|---|:---:|:---:|
| YouTube (Vídeos, Shorts, Playlists) | Sim | Sim |
| TikTok | Sim | Sim |
| Instagram (Reels, Vídeos) | Sim | Sim |
| X / Twitter | Sim | Sim |
| SoundCloud | — | Sim |
| Vimeo | Sim | Sim |
| Twitch (Clipes, VODs) | Sim | Sim |
| Facebook | Sim | Sim |

---

## Estrutura e Tecnologias

| Componente | Tecnologia | Finalidade |
|---|---|---|
| **Interface Gráfica** | [CustomTkinter](https://customtkinter.tomschimansky.com/) | Design Dark Mode moderno e responsivo |
| **Motor de Extração** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Parser e downloader multiplataforma |
| **Processamento de Mídia** | [FFmpeg](https://ffmpeg.org/) | Muxing de faixas, conversão para MP3 e injeção de capas |
| **Manipulação de Imagens** | [Pillow](https://pypi.org/project/Pillow/) | Redimensionamento e renderização de thumbnails |
| **Comunicação Web** | [Requests](https://pypi.org/project/requests/) | Requisição de thumbnails e verificação de atualizações |
| **Empacotamento** | [PyInstaller](https://pyinstaller.org/) | Compilação em executável único para Windows |

---

## Como Executar

### Pré-requisitos

1. **Python 3.10 ou superior** instalado.
2. Binários do **FFmpeg** (`ffmpeg.exe` e `ffprobe.exe`) presentes na pasta `ffmpeg/`.

### Executando via código-fonte

```bash
# Clone o repositório
git clone https://github.com/blnkDev/Yt-Downloader.git
cd Yt-Downloader

# Crie e ative um ambiente virtual (opcional, recomendado)
python -m venv venv
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o aplicativo
python baixador.py
```

---

## Compilação do Executável (.exe)

Para gerar o binário independente:

```bash
pip install pyinstaller
python -m PyInstaller --clean baixador.spec
```

O arquivo final será gerado em `dist/baixador.exe`.

---

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informações.
