"""
Utility functions
"""
import json
import logging
from pathlib import Path


def setup_logging(log_file: str = "app.log") -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
    
    Returns:
        Logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def load_config(config_file: str = "config.json") -> dict:
    """
    Load configuration from JSON file
    
    Args:
        config_file: Path to config file
    
    Returns:
        Configuration dictionary
    """
    try:
        if Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
    
    # Return default config
    return {
        "language": "fr",
        "video_quality": "720p",
        "resolution": "1280x720"
    }


def save_config(config: dict, config_file: str = "config.json"):
    """
    Save configuration to JSON file
    
    Args:
        config: Configuration dictionary
        config_file: Path to config file
    """
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")
