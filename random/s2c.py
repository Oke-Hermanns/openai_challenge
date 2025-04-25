import openai
import pyaudio
import wave
import os

openai.api_key = ("sk-proj-Gp2IHNfvHXgUW3ImLVVY296-XKHzZWggCOta_z3WcV7tfMashaqZ8YyU8SbgeoVLTrASylrJ"
                  "irT3BlbkFJdLwl79HnERH3EuxZRwwzlRvugXc7eRYoBLKxu9xgeGhmAjLIDm6pdtj5h_hPr_Eel-w6TxvegA")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
RECORD_SECONDS = 5
AUDIO_FILE = "live_audio.wav"


def record_audio(file_path):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


def transcribe_audio(file_path):
    """Transcribes an audio file using OpenAI's Whisper API (new format)."""
    with open(file_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"
        )
    return response.text


def extract_commands(text):
    """Uses GPT to extract relevant robot commands from transcribed text."""
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Extract action commands for a robot. Only return verbs and relevant objects."},
            {"role": "user", "content": f"Extract commands from: {text}"}
        ]
    )
    return response.choices[0].message.content


while True:
    record_audio(AUDIO_FILE)  # Capture live audio
    transcribed_text = transcribe_audio(AUDIO_FILE)  # Transcribe
    print("Transcribed Text:", transcribed_text)

    commands = extract_commands(transcribed_text)  # Extract commands
    print("Extracted Commands:", commands)

    with open("transcription_log.txt", "a") as log_file:
        log_file.write(f"Text: {transcribed_text}\nCommands: {commands}\n\n")
