#!/usr/bin/env python3
"""
YouTube Video Downloader - A simple CLI tool for downloading YouTube videos
Requires: yt-dlp and ffmpeg
"""

import argparse
import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    # Check for yt-dlp
    try:
        subprocess.run(['yt-dlp', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append('yt-dlp')
    
    # Check for ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append('ffmpeg')
    
    if missing:
        print("❌ Missing dependencies:", ', '.join(missing))
        print("\nInstall them with:")
        print("  brew install yt-dlp ffmpeg")
        sys.exit(1)

def download_video(url, quality='best', output_dir=os.path.expanduser('~/Downloads'), audio_only=False, playlist=False):
    """Download video from YouTube"""
    
    cmd = ['yt-dlp']
    
    if audio_only:
        # Download audio only in best quality
        cmd.extend([
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--audio-quality', '0',
            '-o', f'{output_dir}/%(title)s.%(ext)s'
        ])
    else:
        # Download video
        if quality == 'best':
            cmd.extend(['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'])
        elif quality == '1080p':
            cmd.extend(['-f', 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'])
        elif quality == '720p':
            cmd.extend(['-f', 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'])
        elif quality == '480p':
            cmd.extend(['-f', 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]'])
        
        cmd.extend(['-o', f'{output_dir}/%(title)s.%(ext)s'])
    
    # Playlist handling
    if not playlist:
        cmd.append('--no-playlist')
    
    # Add the URL
    cmd.append(url)
    
    print(f"📥 Downloading from: {url}")
    if audio_only:
        print("🎵 Mode: Audio only (MP3)")
    else:
        print(f"🎬 Quality: {quality}")
    print(f"📁 Output directory: {os.path.abspath(output_dir)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Download complete!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed: {e}")
        sys.exit(1)

def list_formats(url):
    """List available formats for a video"""
    cmd = ['yt-dlp', '-F', url]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to list formats: {e}")
        sys.exit(1)

def prompt_quality_selection():
    """Prompt user to select video quality"""
    print("\n📺 Select video quality:")
    print("  1. Best (highest quality available)")
    print("  2. 1080p (Full HD)")
    print("  3. 720p (HD)")
    print("  4. 480p (SD)")
    print("  5. Audio only (MP3)")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                return 'best', False
            elif choice == '2':
                return '1080p', False
            elif choice == '3':
                return '720p', False
            elif choice == '4':
                return '480p', False
            elif choice == '5':
                return 'best', True  # audio_only=True
            else:
                print("❌ Invalid choice. Please enter a number between 1-5.")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=VIDEO_ID"
  %(prog)s "URL" -q 720p -o ~/Downloads
  %(prog)s "URL" --audio-only
  %(prog)s "URL" --list-formats
  %(prog)s "PLAYLIST_URL" --playlist
        """
    )
    
    parser.add_argument('url', help='YouTube video or playlist URL')
    parser.add_argument('-q', '--quality', 
                       choices=['best', '1080p', '720p', '480p'],
                       default=None,
                       help='Video quality (default: prompt user)')
    parser.add_argument('-o', '--output-dir',
                       default=os.path.expanduser('~/Downloads'),
                       help='Output directory (default: Downloads folder)')
    parser.add_argument('-a', '--audio-only',
                       action='store_true',
                       help='Download audio only (MP3)')
    parser.add_argument('-p', '--playlist',
                       action='store_true',
                       help='Download entire playlist')
    parser.add_argument('-l', '--list-formats',
                       action='store_true',
                       help='List available formats and exit')
    
    args = parser.parse_args()
    
    # Check dependencies first
    check_dependencies()
    
    # List formats if requested
    if args.list_formats:
        list_formats(args.url)
        return
    
    # Interactive quality selection
    if args.quality is None and not args.audio_only:
        quality, audio_only = prompt_quality_selection()
    else:
        quality = args.quality if args.quality else 'best'
        audio_only = args.audio_only
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Download the video
    download_video(
        args.url,
        quality=quality,
        output_dir=args.output_dir,
        audio_only=audio_only,
        playlist=args.playlist
    )

if __name__ == '__main__':
    main()
