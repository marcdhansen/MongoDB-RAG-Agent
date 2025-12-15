from transformers import pipeline
import torch

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base", dtype=torch.float32)
result = pipe("Recording1.mp3")
print(result["text"])

