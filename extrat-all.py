import pysrt
import json
import subprocess
import os

# Dossiers des fichiers d'entrée
sous_titre_dir = "sous-titre"
audio_dir = "audio-mp3"
output_base_dir = "data"  # Tous les fichiers créés iront dans ce dossier

# Fonction pour convertir hh:mm:ss,SSS en secondes
def convert_time_to_seconds(time_str):
    hours, minutes, rest = time_str.split(":")
    seconds, milliseconds = rest.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000

# Créer le dossier data s'il n'existe pas
os.makedirs(output_base_dir, exist_ok=True)

# Lister tous les fichiers .srt dans le dossier sous-titre
srt_files = [f for f in os.listdir(sous_titre_dir) if f.endswith(".srt")]

if not srt_files:
    print("❌ Aucun fichier .srt trouvé dans le dossier 'sous-titre'.")
    exit()

# Traitement de chaque fichier .srt
for srt_file in srt_files:
    srt_path = os.path.join(sous_titre_dir, srt_file)
    
    # Extraire le nom sans extension
    base_name = os.path.splitext(srt_file)[0]
    json_file = f"{base_name}.json"

    # Vérifier si l'audio correspondant existe
    audio_file = os.path.join(audio_dir, f"{base_name}.mp3")
    if not os.path.exists(audio_file):
        print(f"⚠️ Fichier audio non trouvé : {audio_file}, passage au suivant...")
        continue

    # Dossier de sortie spécifique au fichier en cours
    output_folder = os.path.join(output_base_dir, base_name)
    segment_folder = os.path.join(output_folder, "segment")
    os.makedirs(segment_folder, exist_ok=True)

    # Convertir SRT en JSON
    subtitles = pysrt.open(srt_path)
    data = [{"start": str(sub.start), "end": str(sub.end), "text": sub.text} for sub in subtitles]

    json_path = os.path.join(output_folder, json_file)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Conversion terminée : {json_path}")

    # Charger les sous-titres JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        subtitles = json.load(f)

    total_segments = len(subtitles)

    # Extraction des segments audio
    for i, caption in enumerate(subtitles):
        start_time = convert_time_to_seconds(caption['start'])
        end_time = convert_time_to_seconds(caption['end'])

        # Nom du fichier segment
        segment_filename = f"{base_name}_segment_{i+1}.mp3"
        segment_path = os.path.join(segment_folder, segment_filename)

        # Exécution de la commande ffmpeg
        command = [
            'ffmpeg',
            '-i', audio_file,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            segment_path
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Mettre à jour le JSON avec le chemin du segment
        caption['audio_path'] = f"segment/{segment_filename}"

        # Affichage de la progression
        progress = ((i + 1) / total_segments) * 100
        print(f"🔹 Progression {base_name} : {progress:.2f}% ({i+1}/{total_segments})")

    # Sauvegarder le fichier JSON mis à jour
    updated_json_path = os.path.join(output_folder, json_file)
    with open(updated_json_path, 'w', encoding='utf-8') as f:
        json.dump(subtitles, f, indent=4, ensure_ascii=False)

    print(f"🎯 Fichier traité : {base_name} -> {updated_json_path}")

print("✅ Tous les fichiers ont été traités avec succès.")
