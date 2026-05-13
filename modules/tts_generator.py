"""
Text-to-Speech Generator - Create voiceover audio
"""
import os
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class TTSGenerator:
    """Generate text-to-speech audio using Google's service"""
    
    def __init__(self, output_dir: str = ".temp/audio", language: str = "fr"):
        self.output_dir = output_dir
        self.language = language
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            from gtts import gTTS
            self.gTTS = gTTS
            logger.info(f"Initialized TTS with language: {language}")
        except ImportError:
            logger.error("gTTS not installed")
            self.gTTS = None
    
    def generate_audio(self, text: str, filename: str) -> str:
        """
        Generate audio from text
        
        Args:
            text: Text to convert
            filename: Output filename (without extension)
        
        Returns:
            Path to generated audio file
        """
        if not self.gTTS:
            logger.error("gTTS is not available")
            return ""
        
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return ""
        
        try:
            tts = self.gTTS(text=text, lang=self.language)
            output_path = os.path.join(self.output_dir, f"{filename}.mp3")
            tts.save(output_path)
            logger.info(f"Generated audio: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return ""
    
    def generate_audio_batch(self, texts: List[str], prefix: str = "audio") -> List[str]:
        """Generate multiple audio files"""
        audio_files = []
        for idx, text in enumerate(texts, 1):
            filename = f"{prefix}_{idx}"
            audio_path = self.generate_audio(text, filename)
            if audio_path:
                audio_files.append(audio_path)
        logger.info(f"Generated {len(audio_files)} audio files")
        return audio_files
