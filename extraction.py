import pysrt
import json

def srt_to_json(srt_file, json_file):
    subtitles = pysrt.open(srt_file)
    data = []

    for subtitle in subtitles:
        data.append({
            "start": str(subtitle.start),
            "end": str(subtitle.end),
            "text": subtitle.text
        })

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Conversion terminée ! Résultat enregistré dans {json_file}")

# Utilisation
srt_to_json("muhm-s1-e1-1.srt", "muhm-s1-e1-1.json")