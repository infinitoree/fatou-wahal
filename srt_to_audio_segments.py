import json
import subprocess
import os

# Fonction pour convertir le format hh:mm:ss,SSS en secondes
def convert_time_to_seconds(time_str):
    hours, minutes, rest = time_str.split(":")
    seconds, milliseconds = rest.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000

# Charger les sous-titres à partir du fichier JSON
transcription_file = 'muhm-s1-e1-1.json'
with open(transcription_file, 'r', encoding='utf-8') as f:
    subtitles = json.load(f)

# Chemin vers votre fichier audio
audio_file = "audio.mp3"

# Extraire le nom du fichier de transcription sans l'extension
folder_name = os.path.splitext(os.path.basename(transcription_file))[0]

# Créer un sous-dossier pour les segments audio
os.makedirs(folder_name, exist_ok=True)

# Parcourir les sous-titres et extraire les segments
for i, caption in enumerate(subtitles):
    start_time = convert_time_to_seconds(caption['start'])  # Convertir en secondes
    end_time = convert_time_to_seconds(caption['end'])
    
    # Nom du fichier de sortie dans le sous-dossier
    output_filename = os.path.join(folder_name, f"segment_{i+1}_{start_time}_{end_time}.wav")
    
    # Commande ffmpeg pour extraire le segment audio
    command = [
        'ffmpeg',
        '-i', audio_file,
        '-ss', str(start_time),  # Temps de début
        '-to', str(end_time),    # Temps de fin
        '-c', 'copy',            # Copier sans réencodage
        output_filename
    ]
    
    # Exécution de la commande ffmpeg
    subprocess.run(command)
    
    # Ajouter le chemin du fichier audio dans le JSON
    caption['audio_path'] = output_filename
    print(f"Segment {i+1} extrait : {output_filename}")

# Sauvegarder le fichier JSON mis à jour avec le chemin des fichiers audio
with open(transcription_file, 'w', encoding='utf-8') as f:
    json.dump(subtitles, f, indent=4, ensure_ascii=False)

print(f"Les segments audio ont été extraits et les chemins ajoutés au fichier {transcription_file}")
