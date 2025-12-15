import whisper
model = whisper.load_model("base")
audio_path = "Recording1.mp3"
result = model.transcribe(audio_path, fp16=False)
print(result["text"])
