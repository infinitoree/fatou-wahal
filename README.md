# Extraction et Segmentation Audio à partir de Sous-titres

Ce script permet d'extraire des segments audio à partir d'un fichier audio (par exemple, un fichier `.mp3`) en utilisant les horaires définis dans un fichier de transcription au format JSON. Les segments audio extraits sont enregistrés sous forme de fichiers `.wav` et un chemin d'accès au fichier audio est ajouté à chaque entrée de sous-titre dans le fichier JSON.

## Prérequis

- Python 3.x
- Bibliothèques Python suivantes :
  - `json`
  - `subprocess`
  - `os`
- [FFmpeg](https://ffmpeg.org/download.html) installé sur votre machine (utilisé pour l'extraction des segments audio)

## Fonctionnement

1. **Conversion de temps** : Le script commence par convertir les horaires des sous-titres, donnés en format `hh:mm:ss,SSS` (heures, minutes, secondes, millisecondes), en secondes.
2. **Chargement de la transcription** : Le fichier JSON de transcription est chargé et chaque sous-titre est analysé pour en extraire les horaires de début et de fin.
3. **Extraction des segments audio** : Pour chaque sous-titre, le script utilise FFmpeg pour extraire le segment audio correspondant du fichier audio, entre le temps de début et de fin. Chaque segment est sauvegardé en fichier `.wav`.
4. **Mise à jour du fichier JSON** : Le chemin d'accès de chaque segment audio extrait est ajouté au fichier JSON de transcription sous la clé `audio_path`.
5. **Organisation des fichiers** : Les segments audio extraits sont placés dans un sous-dossier du même nom que le fichier JSON, pour mieux organiser les fichiers.

## Installation et Exécution

### 1. Installation de FFmpeg

Assurez-vous que [FFmpeg](https://ffmpeg.org/download.html) est installé sur votre machine et accessible via le terminal ou la ligne de commande.

### 2. Utilisation du Script

1. **Préparez votre fichier JSON de transcription** : Ce fichier doit être au format JSON, avec des objets contenant les clés `start` et `end` représentant les horaires des sous-titres.
2. **Placez le fichier audio** : Assurez-vous que le fichier audio (par exemple, `audio.mp3`) est présent dans le même répertoire que le script ou modifiez le chemin dans le script.
3. **Exécutez le script** :
   ```bash
   python extrat-all.py  
