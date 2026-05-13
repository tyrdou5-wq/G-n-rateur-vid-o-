# Video Generator 🎬

Une application intelligente qui génère automatiquement des vidéos professionnelles à partir d'un script texte.

## Fonctionnalités

✨ **Analyse de script** - Parse automatiquement votre texte pour identifier les scènes
🎬 **Recherche multimédia** - Trouve des images et vidéos pertinentes (Unsplash, Pexels)
🎤 **Génération de voix off** - Synthèse vocale automatique en français (Google TTS gratuit)
🎞️ **Montage vidéo** - Assemble tout avec FFmpeg pour une vidéo professionnelle
📤 **Vidéo prête à l'emploi** - Exporte en MP4 haute qualité

## Installation

### Prérequis
- Python 3.8+
- FFmpeg
- pip

### Étapes

```bash
# Cloner le repository
git clone https://github.com/tyrdou5-wq/G-n-rateur-vid-o-.git
cd G-n-rateur-vid-o-

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Installer FFmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
# Windows: choco install ffmpeg
```

## Utilisation

### 1. Créer un script vidéo

Créez un fichier texte dans `scripts/` :

```
[SCÈNE 1 - Introduction]
Narration: "Saviez-vous que le joueur le plus rapide au monde..."
Durée: 5 secondes
Visuels souhaités: Terrain de football, joueurs de foot

[SCÈNE 2]
Narration: "Anthony Elanga avec une vitesse de 36,9km/h..."
Durée: 8 secondes
Visuels souhaités: Anthony Elanga, vitesse, sprint
```

### 2. Lancer la génération

```bash
python main.py --script scripts/mon_script.txt --output ma_video.mp4
```

### 3. Récupérer la vidéo

La vidéo générée sera dans `output/ma_video.mp4`

## Configuration

Modifiez `config.json` pour :
- Langue de la voix off (français par défaut)
- Qualité vidéo (720p, 1080p)
- Durée des transitions
- Vitesse de lecture

## Architecture

```
├── modules/
│   ├── script_parser.py      # Analyse du script
│   ├── search_media.py       # Recherche images/vidéos
│   ├── tts_generator.py      # Synthèse vocale
│   ├── video_editor.py       # Montage avec FFmpeg
│   └── utils.py              # Fonctions utilitaires
├── main.py                   # Point d'entrée principal
├── config.json               # Configuration
└── requirements.txt          # Dépendances
```

## Technologies utilisées

- **gTTS** - Synthèse vocale Google (gratuit)
- **Pillow** - Traitement images
- **requests** - Requêtes HTTP
- **FFmpeg** - Montage vidéo

## Roadmap 🚀

- [ ] Interface GUI (Tkinter/PyQt)
- [ ] Support de plusieurs langues
- [ ] Sous-titres automatiques
- [ ] Export multi-formats
- [ ] Docker support

## Licence

MIT

## Auteur

tyrdou5-wq
