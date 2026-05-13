#!/usr/bin/env python3
"""
Video Generator - Main Application

Generate professional videos from scripts automatically.
"""

import sys
import logging
import argparse
from pathlib import Path

from modules import (
    ScriptParser,
    MediaSearcher,
    TTSGenerator,
    VideoEditor,
    setup_logging,
    load_config
)

# Setup logging
logger = setup_logging()


class VideoGenerator:
    """Main application class"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = load_config(config_file)
        self.parser = ScriptParser()
        self.media_searcher = MediaSearcher()
        self.tts = TTSGenerator(language=self.config.get('language', 'fr'))
        self.editor = VideoEditor()
        logger.info("Initialized VideoGenerator")
    
    def generate(self, script_file: str, output_file: str = None):
        """
        Generate video from script
        
        Args:
            script_file: Path to script file
            output_file: Path to output video (optional)
        """
        logger.info(f"Starting video generation from {script_file}")
        
        # Step 1: Parse script
        scenes = self.parser.parse_file(script_file)
        if not scenes:
            logger.error("No scenes found in script")
            return False
        
        logger.info(f"Parsed {len(scenes)} scenes")
        self.parser.print_scenes()
        
        # Step 2: Generate audio for each scene
        logger.info("Generating voiceover audio...")
        audio_files = []
        for idx, scene in enumerate(scenes, 1):
            narration = scene.get('narration', '')
            if narration:
                audio_file = self.tts.generate_audio(narration, f"scene_{idx}")
                if audio_file:
                    audio_files.append(audio_file)
        
        if not audio_files:
            logger.error("Failed to generate audio")
            return False
        
        logger.info(f"Generated {len(audio_files)} audio files")
        
        # Step 3: Search for media for each scene
        logger.info("Searching for media...")
        media_files = []
        for idx, scene in enumerate(scenes, 1):
            keywords = scene.get('keywords', [])
            if not keywords:
                keywords = [scene.get('title', 'scene')]
            
            # Search images
            image_urls = self.media_searcher.search_images(keywords, max_results=2)
            
            if image_urls:
                # Download images
                downloaded = self.media_searcher.download_images_batch(
                    image_urls, 
                    prefix=f"scene_{idx}"
                )
                media_files.extend(downloaded)
            else:
                # Use placeholder if no images found
                placeholder = self.media_searcher.get_placeholder_image()
                if placeholder:
                    media_files.append(placeholder)
        
        logger.info(f"Found {len(media_files)} media files")
        
        # Step 4: Create video from media
        logger.info("Creating video clips...")
        video_clips = []
        for idx, (scene, media_file) in enumerate(zip(scenes, media_files), 1):
            duration = scene.get('duration', 5)
            output_clip = f".temp/video/clip_{idx}.mp4"
            
            clip = self.editor.create_image_video(media_file, duration, output_clip)
            if clip:
                video_clips.append(clip)
        
        if not video_clips:
            logger.error("Failed to create video clips")
            return False
        
        logger.info(f"Created {len(video_clips)} video clips")
        
        # Step 5: Add audio to each clip
        logger.info("Adding audio to video clips...")
        final_clips = []
        for idx, (video_clip, audio_file) in enumerate(zip(video_clips, audio_files), 1):
            output_with_audio = f".temp/video/final_clip_{idx}.mp4"
            final_clip = self.editor.add_audio_to_video(
                video_clip,
                audio_file,
                output_with_audio
            )
            if final_clip:
                final_clips.append(final_clip)
        
        if not final_clips:
            logger.error("Failed to add audio to clips")
            return False
        
        # Step 6: Concatenate all clips
        logger.info("Concatenating video clips...")
        if output_file is None:
            output_file = "output/video_output.mp4"
        
        final_video = self.editor.concatenate_videos(final_clips, output_file)
        
        if final_video:
            logger.info(f"✅ Video generated successfully: {final_video}")
            print(f"\n✅ Video saved to: {final_video}")
            return True
        else:
            logger.error("Failed to concatenate videos")
            return False


def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description="Generate videos from scripts automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python main.py --script scripts/my_video.txt --output video.mp4
        """
    )
    
    parser.add_argument(
        '--script', '-s',
        required=True,
        help='Path to video script file'
    )
    parser.add_argument(
        '--output', '-o',
        default='output/generated_video.mp4',
        help='Output video file path (default: output/generated_video.mp4)'
    )
    parser.add_argument(
        '--config', '-c',
        default='config.json',
        help='Configuration file path (default: config.json)'
    )
    
    args = parser.parse_args()
    
    # Check if script file exists
    if not Path(args.script).exists():
        logger.error(f"Script file not found: {args.script}")
        sys.exit(1)
    
    # Generate video
    generator = VideoGenerator(config_file=args.config)
    success = generator.generate(args.script, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
