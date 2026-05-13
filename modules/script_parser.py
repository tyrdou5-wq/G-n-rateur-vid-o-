"""
Script Parser - Parse and analyze video scripts
"""
import re
import logging
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ScriptParser:
    """Parse video scripts and extract scenes"""
    
    def __init__(self):
        self.scenes = []
        logger.info("Initialized Script Parser")
    
    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a script file
        
        Args:
            filepath: Path to script file
        
        Returns:
            List of scene dictionaries
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.scenes = self._parse_content(content)
            logger.info(f"Parsed {len(self.scenes)} scenes from {filepath}")
            return self.scenes
        
        except FileNotFoundError:
            logger.error(f"Script file not found: {filepath}")
            return []
        except Exception as e:
            logger.error(f"Error parsing script: {e}")
            return []
    
    def _parse_content(self, content: str) -> List[Dict]:
        """
        Parse script content into scenes
        
        Args:
            content: Raw script content
        
        Returns:
            List of scene dictionaries
        """
        scenes = []
        
        # Split by scene markers [SCÈNE ...] or [SCENE ...]
        scene_pattern = r'\[(SCÈNE|SCENE)\s+\d+\s*-?\s*([^\]]+)\]'
        scene_matches = list(re.finditer(scene_pattern, content, re.IGNORECASE))
        
        if not scene_matches:
            # If no scene markers, treat whole content as one scene
            scene = self._extract_scene_info(content, "Scène 1")
            return [scene] if scene else []
        
        for idx, match in enumerate(scene_matches):
            scene_title = match.group(2).strip()
            
            # Get text between this scene and next scene
            start_pos = match.end()
            end_pos = scene_matches[idx + 1].start() if idx + 1 < len(scene_matches) else len(content)
            
            scene_text = content[start_pos:end_pos]
            scene = self._extract_scene_info(scene_text, scene_title)
            
            if scene:
                scenes.append(scene)
        
        return scenes
    
    def _extract_scene_info(self, scene_text: str, title: str) -> Optional[Dict]:
        """
        Extract information from scene text
        
        Args:
            scene_text: Text content of scene
            title: Scene title
        
        Returns:
            Dictionary with scene information
        """
        scene = {
            'title': title,
            'narration': '',
            'duration': 5,  # Default duration
            'keywords': [],
            'visuals': ''
        }
        
        # Extract narration
        narration_match = re.search(
            r'[Nn]arration\s*:\s*["\']([^"\']*)["\'']',
            scene_text
        )
        if narration_match:
            scene['narration'] = narration_match.group(1).strip()
        else:
            # If no explicit narration field, use all text
            scene['narration'] = scene_text.strip()
        
        # Extract duration
        duration_match = re.search(
            r'[Dd]ur[ée]e\s*:\s*(\d+(?:\.\d+)?)\s*(?:secondes?|s)?',
            scene_text
        )
        if duration_match:
            scene['duration'] = float(duration_match.group(1))
        
        # Extract visuals/keywords
        visuals_match = re.search(
            r'[Vv]isuels?\s*(?:souhait[ée]s?)?\s*:\s*([^\n]+)',
            scene_text
        )
        if visuals_match:
            visuals_str = visuals_match.group(1).strip()
            scene['visuals'] = visuals_str
            scene['keywords'] = [k.strip() for k in visuals_str.split(',')]
        
        # If no keywords found, extract from narration
        if not scene['keywords']:
            scene['keywords'] = self._extract_keywords(scene['narration'])
        
        return scene if scene['narration'] else None
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Text to extract keywords from
        
        Returns:
            List of keywords
        """
        # Remove common words
        stop_words = {
            'le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'mais', 'donc',
            'car', 'parce', 'que', 'qui', 'quel', 'quoi', 'où', 'quand', 'comment',
            'pourquoi', 'avec', 'sans', 'pour', 'par', 'de', 'du', 'dans', 'sur',
            'à', 'au', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        
        # Extract words (minimum 3 characters)
        words = re.findall(r'\b[a-zA-Zàâäçèéêëîïôùûüœæ]{3,}\b', text.lower())
        
        # Filter stop words and duplicates
        keywords = list(set(
            word for word in words 
            if word not in stop_words and len(word) > 2
        ))
        
        return keywords[:5]  # Return top 5 keywords
    
    def get_scenes(self) -> List[Dict]:
        """
        Get parsed scenes
        
        Returns:
            List of scene dictionaries
        """
        return self.scenes
    
    def get_total_duration(self) -> float:
        """
        Get total video duration
        
        Returns:
            Total duration in seconds
        """
        return sum(scene['duration'] for scene in self.scenes)
    
    def print_scenes(self):
        """
        Print scenes for debugging
        """
        for idx, scene in enumerate(self.scenes, 1):
            print(f"\n--- Scène {idx}: {scene['title']} ---")
            print(f"Narration: {scene['narration'][:100]}...")
            print(f"Durée: {scene['duration']}s")
            print(f"Mots-clés: {', '.join(scene['keywords'])}")


# Example usage
if __name__ == "__main__":
    parser = ScriptParser()
    
    # Example script
    script = """
    [SCÈNE 1 - Introduction]
    Narration: "Saviez-vous que le joueur le plus rapide au monde peut comparer sa vitesse à celle d'une Ferrari?"
    Durée: 5 secondes
    Visuels souhaités: Terrain de football, vitesse, Ferrari
    
    [SCÈNE 2]
    Narration: "Anthony Elanga avec une vitesse modérée de 36,9km/h."
    Durée: 8 secondes
    Visuels souhaités: Anthony Elanga, vitesse, sprint
    """
    
    scenes = parser._parse_content(script)
    for scene in scenes:
        print(scene)
