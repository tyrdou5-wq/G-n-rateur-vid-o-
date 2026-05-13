"""
Media Search - Find images and videos for scenes
"""
import os
import logging
import requests
from typing import List, Dict
from pathlib import Path
from urllib.parse import quote

logger = logging.getLogger(__name__)


class MediaSearcher:
    """Search for images and videos based on keywords"""
    
    def __init__(self, temp_dir: str = ".temp/media"):
        self.temp_dir = temp_dir
        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        logger.info("Initialized Media Searcher")
    
    def search_images(self, keywords: List[str], max_results: int = 5,
                     sources: List[str] = None) -> List[str]:
        """
        Search for images from multiple sources
        
        Args:
            keywords: List of search keywords
            max_results: Maximum number of images to fetch
            sources: List of image sources ['unsplash', 'pexels']
        
        Returns:
            List of image URLs
        """
        if sources is None:
            sources = ['unsplash', 'pexels']
        
        all_images = []
        
        for source in sources:
            if source.lower() == 'unsplash':
                images = self._search_unsplash(keywords, max_results)
                all_images.extend(images)
            elif source.lower() == 'pexels':
                images = self._search_pexels(keywords, max_results)
                all_images.extend(images)
        
        return all_images[:max_results]
    
    def _search_unsplash(self, keywords: List[str], max_results: int) -> List[str]:
        """Search Unsplash API (free)"""
        try:
            if not keywords:
                return []
            
            search_query = keywords[0]
            url = f"https://api.unsplash.com/search/photos?query={quote(search_query)}&per_page={max_results}"
            
            headers = {'User-Agent': 'VideoGenerator/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                images = [img['urls']['regular'] for img in data.get('results', [])]
                logger.info(f"Found {len(images)} images on Unsplash")
                return images
            return []
        except Exception as e:
            logger.error(f"Error searching Unsplash: {e}")
            return []
    
    def _search_pexels(self, keywords: List[str], max_results: int) -> List[str]:
        """Search Pexels API (free)"""
        try:
            if not keywords:
                return []
            
            search_query = keywords[0]
            url = f"https://www.pexels.com/api/v2/search?query={quote(search_query)}&per_page={max_results}"
            
            headers = {'User-Agent': 'VideoGenerator/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                images = [photo['src']['original'] for photo in data.get('photos', [])]
                logger.info(f"Found {len(images)} images on Pexels")
                return images
            return []
        except Exception as e:
            logger.error(f"Error searching Pexels: {e}")
            return []
    
    def download_image(self, url: str, output_name: str) -> str:
        """
        Download image from URL
        
        Args:
            url: Image URL
            output_name: Name for downloaded file
        
        Returns:
            Path to downloaded file
        """
        try:
            output_path = os.path.join(self.temp_dir, output_name)
            response = requests.get(url, timeout=10, stream=True)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info(f"Downloaded: {output_path}")
                return output_path
            return ""
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return ""
    
    def download_images_batch(self, image_urls: List[str], 
                             prefix: str = "image") -> List[str]:
        """Download multiple images"""
        downloaded = []
        for idx, url in enumerate(image_urls, 1):
            filename = f"{prefix}_{idx}.jpg"
            path = self.download_image(url, filename)
            if path:
                downloaded.append(path)
        return downloaded
    
    def get_placeholder_image(self, size: tuple = (1280, 720)) -> str:
        """Generate placeholder image"""
        try:
            from PIL import Image
            img = Image.new('RGB', size, '#333333')
            output_path = os.path.join(self.temp_dir, "placeholder.png")
            img.save(output_path)
            logger.info(f"Generated placeholder: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating placeholder: {e}")
            return ""
