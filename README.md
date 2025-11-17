# YouTube Video Downloader CLI

A simple, powerful command-line tool for downloading YouTube videos on macOS.

## Features

- 🎯 **Interactive mode** - Prompts you to select video quality when downloading
- 📥 Download videos in multiple qualities (best, 1080p, 720p, 480p)
- 🎵 Download audio-only as MP3
- 📋 Download entire playlists
- 🔍 List available formats before downloading
- 💾 Downloads automatically save to your Downloads folder
- ⚡ Simple and intuitive command-line interface

## Prerequisites

- macOS
- Homebrew (install from https://brew.sh)
- Python 3 (usually pre-installed on macOS)

## Installation

1. Download the files (`ytdl.py` and `install.sh`)

2. Open Terminal and navigate to the directory containing the files:
   ```bash
   cd /path/to/downloaded/files
   ```

3. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   This will:
   - Install `yt-dlp` and `ffmpeg` via Homebrew
   - Make the tool available as `ytdl` command globally

## Usage

### Interactive Mode (Recommended)

Simply provide the URL and you'll be prompted to select the quality:

```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID"
```

You'll see a menu like this:
```
📺 Select video quality:
  1. Best (highest quality available)
  2. 1080p (Full HD)
  3. 720p (HD)
  4. 480p (SD)
  5. Audio only (MP3)

Enter your choice (1-5):
```

### Command-Line Mode

You can also specify options directly to skip the interactive prompt:

**Download in specific quality:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" -q 720p
```

**Download to specific directory:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" -o ~/Documents
```

**Download audio only (MP3):**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only
```

**Download entire playlist:**
```bash
ytdl "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

**List available formats:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" --list-formats
```

### All Options

```
usage: ytdl [-h] [-q {best,1080p,720p,480p}] [-o OUTPUT_DIR] [-a] [-p] [-l] url

positional arguments:
  url                   YouTube video or playlist URL

options:
  -h, --help            show this help message and exit
  -q, --quality         Video quality: best, 1080p, 720p, 480p (default: prompt user)
  -o, --output-dir      Output directory (default: Downloads folder)
  -a, --audio-only      Download audio only (MP3)
  -p, --playlist        Download entire playlist
  -l, --list-formats    List available formats and exit
```

## Examples

**Interactive download (easiest):**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID"
# Then select quality from the menu
```

**Download music video as MP3 to Music folder:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" -a -o ~/Music
```

**Download playlist in 720p:**
```bash
ytdl "https://www.youtube.com/playlist?list=PLAYLIST_ID" -q 720p -p
```

**Check available formats first:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" -l
```

**Quick 1080p download to Downloads:**
```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID" -q 1080p
```

## Troubleshooting

**Command not found:**
- Make sure you ran the installation script
- Try running: `which ytdl` to see if it's installed
- You may need to restart your terminal

**Download fails:**
- Check your internet connection
- Verify the YouTube URL is correct
- Some videos may be region-restricted or age-restricted

**Dependencies missing:**
- Run: `brew install yt-dlp ffmpeg`

## Uninstallation

```bash
# Remove the command
rm /usr/local/bin/ytdl

# Optionally remove dependencies
brew uninstall yt-dlp ffmpeg
```

## Notes

- **Default location:** Videos are downloaded to your Downloads folder (`~/Downloads`) by default
- **Custom location:** Use `-o` flag to specify a different directory
- **Interactive mode:** When you don't specify `-q`, the tool will prompt you to select quality
- **File names:** Automatically sanitized and based on video titles
- **Terms of service:** The tool respects YouTube's terms of service - only download content you have rights to

## How to run this on Docker

```bash 

docker build -t python-ytdlp .

docker run -it --rm python-ytdlp

docker run --rm -v $(pwd):/app python-ytdlp yt-dlp <video-url>

---

// stop and remove container
docker rm -f <name>

// remove the image
docker rmi <name>


```

## License

Free to use and modify for personal use.
