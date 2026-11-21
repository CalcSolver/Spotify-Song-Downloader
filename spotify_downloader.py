#!/usr/bin/env python3
"""
Interactive Spotify Audio Downloader (SpotDL CLI Wrapper)
Compatible with SpotDL v4.x+
"""

import subprocess
import sys
import os
import shutil

def print_header():
    print("=" * 50)
    print("   SPOTIFY AUDIO STEALER (Python Edition)")
    print("=" * 50)

def get_user_input(prompt, default=""):
    user_input = input(prompt).strip()
    return user_input if user_input else default

def check_spotdl_installed():
    """Checks if spotdl CLI is available."""
    if shutil.which("spotdl") is None:
        print("[ERROR] 'spotdl' command not found.")
        print("Please run: pip install spotdl")
        sys.exit(1)

def run_spotdl_command(url, output_dir, audio_format, bitrate):
    """
    Constructs and runs the spotdl CLI command.
    Uses current SpotDL v4+ syntax.
    """
    # Base command
    cmd = [
        "spotdl",
        "download",
        url,
        "--output", output_dir,
        "--format", audio_format
    ]
    
    # Add bitrate only for lossy formats (SpotDL requires 'k' suffix)
    if audio_format in ["mp3", "m4a", "ogg", "opus"]:
        cmd.extend(["--bitrate", f"{bitrate}k"])

    # Optional: Add --print-errors to see why a track might fail
    cmd.append("--print-errors")

    print(f"\nExecuting: {' '.join(cmd)}\n")
    print("-" * 50)
    
    try:
        # Run the command in the current terminal
        subprocess.run(cmd, check=True)
        print("\n[SUCCESS] Download complete! Check your output folder.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Download failed with code {e.returncode}.")
    except FileNotFoundError:
        print("[ERROR] Could not execute spotdl. Is it installed in your PATH?")

def main():
    print_header()
    
    # Check if spotdl is installed
    check_spotdl_installed()

    # 1. Get URL
    print("\nPaste your Spotify Track, Album, Playlist, or Search URL:")
    url = get_user_input("URL: ")
    if not url:
        print("No URL provided. Exiting.")
        return
        
    # 2. Get Output Directory
    default_dir = os.path.join(os.getcwd(), "downloads")
    print(f"\nDefault download folder: {default_dir}")
    output_dir = get_user_input("Enter output folder (press Enter for default): ", default_dir)
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    # 3. Get Format
    print("\nAvailable formats: mp3, flac, wav, m4a, ogg, opus")
    audio_format = get_user_input("Format (default: mp3): ", "mp3").lower()
    
    valid_formats = ["mp3", "flac", "wav", "m4a", "ogg", "opus"]
    if audio_format not in valid_formats:
        print(f"Invalid format '{audio_format}'. Defaulting to mp3.")
        audio_format = "mp3"

    # 4. Get Bitrate (only if lossy format)
    bitrate = "320"
    if audio_format in ["mp3", "m4a", "ogg", "opus"]:
        print("\nBitrates: 128, 192, 320")
        bitrate = get_user_input("Bitrate (default: 320): ", "320")
        # Sanitize bitrate input
        if bitrate not in ["128", "192", "320"]:
            print("Invalid bitrate. Defaulting to 320.")
            bitrate = "320"

    # 5. Execute
    print(f"\nDownloading to: {output_dir}")
    run_spotdl_command(url, output_dir, audio_format, bitrate)

if __name__ == "__main__":
    main()
