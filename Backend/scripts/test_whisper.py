from app.speech.service import SpeechService

speech = SpeechService()

text = speech.transcribe(
    "sample.wav"
)

print(text)
