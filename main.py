import json
import os
import base64
import requests
from openai import OpenAI
from datetime import datetime

api_key = open("key.txt", "r").read().strip()
client = OpenAI(api_key=api_key)


def get_transcription(encoded_string: str):
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe the literal words of what is in the recording if possible. So if it is spoken words, write the words down otherwise do not transcribe, just put down 'Cannot transcribe'."
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": "wav"
                        }
                    }
                ]
            },
        ]
    )

    return completion.choices[0].message.audio


def process_audio_files(data_folder: str, output_file: str):
    results = []
    for filename in os.listdir(data_folder):
        if filename.endswith('.wav'):
            file_path = os.path.join(data_folder, filename)
            print(f"Processing {file_path}")
            with open(file_path, 'rb') as f:
                wav_data = f.read()
            encoded_string = base64.b64encode(wav_data).decode('utf-8')
            transcription = get_transcription(encoded_string)
            results.append({
                "filename": filename,
                "transcription": transcription.transcript
            })

    # Create results dir if it does not exist
    if not os.path.exists('results'):
        os.makedirs('results')

    # Write results to output file and concat file name with timestamp
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(
        'results', f"transcriptions_{timestamp}.json")

    print(f"Writing results to {output_file}")
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")


if __name__ == "__main__":
    process_audio_files('data/perturbed_1_255', 'transcriptions.json')
