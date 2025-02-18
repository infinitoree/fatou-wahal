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
3. **Vérification du fichier audio** : Le fichier audio doit porter le même nom que le fichier JSON (en remplaçant `.json` par `.mp3`). Si aucun fichier audio correspondant n'est trouvé, le script ne pourra pas traiter les sous-titres.
4. **Extraction des segments audio** : Pour chaque sous-titre, le script utilise FFmpeg pour extraire le segment audio correspondant du fichier audio, entre le temps de début et de fin. Chaque segment est sauvegardé en fichier `.wav`.
5. **Mise à jour du fichier JSON** : Le chemin d'accès de chaque segment audio extrait est ajouté au fichier JSON de transcription sous la clé `audio_path`.
6. **Organisation des fichiers** : Les segments audio extraits sont placés dans un sous-dossier du même nom que le fichier JSON, pour mieux organiser les fichiers.

## Structure des fichiers d'entrée et nomenclature

### 1. Fichier de transcription JSON

Le fichier de transcription doit être au format JSON et contenir une liste d'objets avec les clés suivantes :

- `start` : L'heure de début du sous-titre au format `hh:mm:ss,SSS` (par exemple, `00:00:01,000`).
- `end` : L'heure de fin du sous-titre au format `hh:mm:ss,SSS` (par exemple, `00:00:10,000`).
- `text` : Le texte du sous-titre.

**Exemple de fichier JSON :**

```json
[
    {
        "start": "00:00:01,000",
        "end": "00:00:10,000",
        "text": "Bonjour, bienvenue à ce tutoriel."
    },
    {
        "start": "00:00:12,000",
        "end": "00:00:20,000",
        "text": "Dans cette vidéo, nous allons apprendre à utiliser Python."
    }
]

 3. **Exécutez le script** :
   ```bash
   python extrat-all.py  
