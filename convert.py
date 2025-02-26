# Install necessary libraries (run these commands in a Colab cell)
!pip install -q openai-whisper ffmpeg-python torch
!apt install -q ffmpeg

# Import libraries
import os
import time
import subprocess
from datetime import timedelta

import whisper
from google.colab import drive, auth
from googleapiclient.discovery import build


def extract_audio(mp4_path, mp3_path):
    """
    Extracts audio from an MP4 file and saves it as an MP3 file using ffmpeg.
    """
    print(f"MP3抽出: {mp4_path} to {mp3_path}")
    command = [
        "ffmpeg", "-vn", "-i", mp4_path,
        "-acodec", "libmp3lame", "-b:a", "128k", "-ac", "1",
        mp3_path, "-y"
    ]
    subprocess.run(command)
    print(f"MP3抽出完了: {mp3_path}")

def transcribe_audio(mp3_path, txt_path, mtg_language):
    """
    Transcribes audio from the given MP3 file using the Whisper model and writes the transcript to a text file.
    """
    model = whisper.load_model("medium")
    language_code = "en"
    initial_prompt = ""
    if mtg_language == "Japanese":
        language_code = "ja"
        initial_prompt = "です。ます。でした。"
    elif mtg_language == "English":
        language_code = "en"
        initial_prompt = ""  # Or a suitable English prompt

    print(f"文字起こし開始: {mp3_path} to {txt_path} by {language_code}")
    result = model.transcribe(
        mp3_path,
        language = language_code,
        verbose = True,
        initial_prompt = initial_prompt
    )
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Remove the temporary MP3 file
    os.remove(mp3_path)
    print(f"文字起こし完了！結果を {txt_path} に保存しました。")

def create_google_doc(title, txt_path):
    """
    Creates a Google Document with the provided title and inserts the text from the transcript file.
    """
    service = build("docs", "v1")

    # Create a new Google Document
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]

    # Read the transcript text from file
    with open(txt_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # Insert the transcript text into the document
    requests = [{"insertText": {"location": {"index": 1}, "text": transcript_text}}]
    service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    # Remove the temporary transcript file
    os.remove(txt_path)
    print(f"✅ Google Docs 作成完了: https://docs.google.com/document/d/{doc_id}")

def main():
    # Google Authentication and Drive Mounting
    auth.authenticate_user()
    drive.mount('/content/drive')

    # Specify the path of the MP4 file to be converted
    mtg_language = 'English' #@param ["Japanese", "English"] {allow-input: true}
    mp4_path = "/content/drive/MyDrive/Meet Recordings/Recording" #@param {type:"string"}
    mp3_path = f"{mp4_path}.mp3"
    txt_path = f"{mp4_path}.txt"

    # Record start time
    start_time = time.time()

    # Process: Extract audio, transcribe it, and create a Google Document
    extract_audio(mp4_path, mp3_path)
    transcribe_audio(mp3_path, txt_path, mtg_language)
    file_name = "文字起結果_" + os.path.splitext(os.path.basename(txt_path))[0]
    create_google_doc(file_name, txt_path)

    # Calculate and print execution time
    execution_time = time.time() - start_time
    formatted_time = str(timedelta(seconds=execution_time))
    print(f"処理時間: {formatted_time}")

if __name__ == "__main__":
    main()
