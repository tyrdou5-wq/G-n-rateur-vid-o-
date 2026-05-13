"""
Video Editor - Assemble images, audio into video
"""
import os
import logging
import subprocess
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class VideoEditor:
    """Edit and create videos using FFmpeg"""
    
    def __init__(self, output_dir: str = "output", temp_dir: str = ".temp/video"):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        
        if not self._check_ffmpeg():
            logger.warning("FFmpeg not found")
        logger.info("Initialized Video Editor")
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            logger.info("FFmpeg is available")
            return True
        except FileNotFoundError:
            logger.error("FFmpeg not found")
            return False
    
    def create_image_video(self, image_path: str, duration: float, 
                          output_path: str) -> str:
        """
        Create video from image
        
        Args:
            image_path: Path to image
            duration: Video duration in seconds
            output_path: Path to output video
        
        Returns:
            Path to created video
        """
        try:
            cmd = [
                "ffmpeg",
                "-loop", "1",
                "-i", image_path,
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-y",
                output_path
            ]
            
            subprocess.run(cmd, check=True, 
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            logger.info(f"Created image video: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error creating image video: {e}")
            return ""
    
    def add_audio_to_video(self, video_path: str, audio_path: str,
                          output_path: str) -> str:
        """
        Add audio to video
        
        Args:
            video_path: Path to video
            audio_path: Path to audio
            output_path: Path to output
        
        Returns:
            Path to video with audio
        """
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-y",
                output_path
            ]
            
            subprocess.run(cmd, check=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            logger.info(f"Added audio: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error adding audio: {e}")
            return ""
    
    def concatenate_videos(self, video_list: List[str], output_path: str) -> str:
        """
        Concatenate multiple videos
        
        Args:
            video_list: List of video paths
            output_path: Path to concatenated output
        
        Returns:
            Path to concatenated video
        """
        try:
            concat_file = os.path.join(self.temp_dir, "concat.txt")
            with open(concat_file, 'w') as f:
                for video in video_list:
                    f.write(f"file '{os.path.abspath(video)}'\n")
            
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",
                "-y",
                output_path
            ]
            
            subprocess.run(cmd, check=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            logger.info(f"Concatenated videos: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error concatenating: {e}")
            return ""
