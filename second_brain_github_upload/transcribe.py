import os
from faster_whisper import WhisperModel
import time

# Directory settings
input_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\input\Prof_AI_RAG"
output_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Run on CPU with INT8 precision
model_size = "base" # Using base model for CPU speed. Can be upgraded to small/medium later.
print(f"Loading {model_size} model on CPU...")
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Select the smallest file for testing
target_file = "135_TEORIA_Tecniche di Promp Engineerig - LLM - Multitasking.mp4"
video_path = os.path.join(input_dir, target_file)
txt_path = os.path.join(output_dir, target_file.replace(".mp4", ".txt"))

print(f"Starting transcription of: {target_file}")
start_time = time.time()

segments, info = model.transcribe(video_path, beam_size=5, language="it")

print(f"Detected language '{info.language}' with probability {info.language_probability}")

with open(txt_path, "w", encoding="utf-8") as f:
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")

end_time = time.time()
print(f"\nTranscription finished in {end_time - start_time:.2f} seconds.")
print(f"Output saved to {txt_path}")
