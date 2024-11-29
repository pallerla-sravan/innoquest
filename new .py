import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

# Function to transcribe large audio files
def transcribe_audio(file_path, chunk_size_ms=60000):
    recognizer = sr.Recognizer()

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Load the large audio file
    print("Loading audio file...")
    audio = AudioSegment.from_file(file_path)

    # Split the audio into chunks
    chunks = make_chunks(audio, chunk_size_ms)
    print(f"Audio split into {len(chunks)} chunks of {chunk_size_ms / 1000} seconds each.")

    # Prepare to store the transcribed text
    all_text = []

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")  # Export chunk as WAV file

        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        try:
            # Load the chunk for transcription
            with sr.AudioFile(chunk_filename) as source:
                audio_data = recognizer.record(source)
                # Use Google Speech Recognition
                text = recognizer.recognize_google(audio_data)
                all_text.append(text)
                print(f"Chunk {i + 1} transcribed successfully.")
        except sr.UnknownValueError:
            print(f"Chunk {i + 1}: Could not understand audio.")
        except sr.RequestError as e:
            print(f"Chunk {i + 1}: API error - {e}")
        except Exception as e:
            print(f"Chunk {i + 1}: Error - {e}")

        # Clean up temporary chunk file
        os.remove(chunk_filename)

    # Combine all transcriptions into one string
    final_transcription = " ".join(all_text)
    return final_transcription

# Main Execution
if __name__ == "__main__":
    # Specify the path to your audio file
    file_path = "ddd.wav"  # Replace with your file name or path

    print("Starting transcription...")
    try:
        transcription = transcribe_audio(file_path, chunk_size_ms=60000)  # Chunk size = 60 seconds
        if transcription:
            print("\nComplete Transcription:")
            print(transcription)
        else:
            print("No transcription was generated.")
    except Exception as e:
        print(f"An error occurred: {e}")
