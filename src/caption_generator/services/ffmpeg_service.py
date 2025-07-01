"""
FFmpeg service for video processing and subtitle burning.
"""
import subprocess
import asyncio
from pathlib import Path
from typing import Optional

from ..core.config import settings


class FFmpegService:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
    
    def _find_ffmpeg(self) -> str:
        """Find FFmpeg executable path"""
        try:
            result = subprocess.run(
                ["which", "ffmpeg"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            # Try common paths
            common_paths = [
                "/usr/bin/ffmpeg",
                "/usr/local/bin/ffmpeg",
                "ffmpeg"  # Assume it's in PATH
            ]
            
            for path in common_paths:
                try:
                    subprocess.run([path, "-version"], 
                                 capture_output=True, check=True)
                    return path
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            raise FileNotFoundError("FFmpeg not found. Please install FFmpeg.")
    
    async def burn_subtitles(
        self,
        video_path: Path,
        srt_path: Path,
        output_path: Path,
        font_size: int = 24,
        font_color: str = "white",
        position: str = "bottom"
    ) -> Path:
        """Burn subtitles into video using FFmpeg"""
        
        print(f"🎨 Applying subtitle styling:")
        print(f"   Font Size: {font_size}")
        print(f"   Font Color: {font_color}")
        print(f"   Position: {position}")
        
        # Correct alignment values for ASS subtitles
        # 1=left, 2=center, 3=right (horizontal)
        # Combined with vertical: 1=bottom, 5=middle, 9=top
        # So: 2=bottom-center, 6=middle-center, 10=top-center (but 8 is more common for top-center)
        if position.lower() == "bottom":
            alignment = "2"  # Bottom center
            margin_v = "20"  # Margin from bottom edge
        else:  # top
            alignment = "8"  # Top center (correct value)
            margin_v = "20"  # Margin from top edge
        
        # Get proper color hex (BGR format for ASS)
        color_hex = self._color_to_hex(font_color)
        
        # Build the force_style parameter correctly
        force_style = (
            f"FontName=Arial Bold,"
            f"FontSize={font_size},"
            f"PrimaryColour=&H{color_hex},"
            f"OutlineColour=&H000000,"  # Black outline
            f"BackColour=&H80000000,"   # Semi-transparent background
            f"Outline=2,"               # Outline thickness
            f"Shadow=1,"                # Shadow
            f"Alignment={alignment},"   # Position alignment
            f"MarginV={margin_v}"       # Vertical margin
        )
        
        print(f"   FFmpeg force_style: {force_style}")
        
        # Build FFmpeg command with corrected subtitle filter
        cmd = [
            self.ffmpeg_path,
            "-i", str(video_path),
            "-vf", f"subtitles={str(srt_path)}:force_style='{force_style}'",
            "-c:a", "copy",  # Copy audio without re-encoding
            "-c:v", "libx264",  # Re-encode video with subtitles
            "-preset", "medium",  # Balance between speed and quality
            "-crf", "23",  # Good quality
            "-threads", str(settings.ffmpeg.threads),
            "-y",  # Overwrite output file
            str(output_path)
        ]
        
        print(f"   FFmpeg command: {' '.join(cmd)}")
        
        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown FFmpeg error"
            print(f"❌ FFmpeg stderr: {error_msg}")
            raise RuntimeError(f"FFmpeg failed: {error_msg}")
        
        print(f"✅ Successfully created captioned video: {output_path}")
        return output_path
    
    def _color_to_hex(self, color: str) -> str:
        """Convert color name to BGR hex format for ASS subtitles in FFmpeg"""
        # ASS subtitle colors are in BGR format (Blue-Green-Red), not RGB
        # Format: &HBBGGRR
        color_map = {
            "white": "FFFFFF",    # RGB: FF FF FF -> BGR: FF FF FF
            "black": "000000",    # RGB: 00 00 00 -> BGR: 00 00 00
            "red": "0000FF",      # RGB: FF 00 00 -> BGR: 00 00 FF
            "green": "00FF00",    # RGB: 00 FF 00 -> BGR: 00 FF 00
            "blue": "FF0000",     # RGB: 00 00 FF -> BGR: FF 00 00
            "yellow": "00FFFF",   # RGB: FF FF 00 -> BGR: 00 FF FF
            "cyan": "FFFF00",     # RGB: 00 FF FF -> BGR: FF FF 00
            "magenta": "FF00FF",  # RGB: FF 00 FF -> BGR: FF 00 FF
            "orange": "0080FF",   # RGB: FF 80 00 -> BGR: 00 80 FF
            "pink": "FF80FF",     # RGB: FF 80 FF -> BGR: FF 80 FF
            "purple": "800080",   # RGB: 80 00 80 -> BGR: 80 00 80
            "brown": "003366",    # RGB: 66 33 00 -> BGR: 00 33 66
            "gray": "808080",     # RGB: 80 80 80 -> BGR: 80 80 80
            "grey": "808080",     # Same as gray
            "lime": "00FF80",     # RGB: 80 FF 00 -> BGR: 00 FF 80
            "navy": "800000",     # RGB: 00 00 80 -> BGR: 80 00 00
            "silver": "C0C0C0",   # RGB: C0 C0 C0 -> BGR: C0 C0 C0
        }
        
        color_lower = color.lower().strip()
        if color_lower in color_map:
            hex_val = color_map[color_lower]
            print(f"   Color '{color}' -> BGR hex: {hex_val}")
            return hex_val
        
        # If it's already a hex color (with or without #), convert RGB to BGR
        hex_color = color
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]
        
        if len(hex_color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in hex_color):
            # Convert RGB to BGR for ASS subtitles
            r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
            bgr_hex = f"{b}{g}{r}".upper()
            print(f"   Hex color '{color}' (RGB) -> BGR hex: {bgr_hex}")
            return bgr_hex
        
        # Default to white if color not recognized
        print(f"   Unrecognized color '{color}', using white")
        return "FFFFFF"
    
    async def get_video_info(self, video_path: Path) -> dict:
        """Get video information using FFprobe"""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path)
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown FFprobe error"
            raise RuntimeError(f"FFprobe failed: {error_msg}")
        
        import json
        return json.loads(stdout.decode())
