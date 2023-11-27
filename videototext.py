# import speech_recognition as sr
import whisper
import moviepy.editor as mp
from whisper.utils import get_writer

model = whisper.load_model("base")

def convert_video_to_text(video_path, audio_path):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

# Transcribe audio using OpenAI Whisper
    result = model.transcribe("static/audios/audio-from-video.wav")
    
    output_dir = "./static/"
    vtt_writer = get_writer("vtt", output_dir)
    vtt_writer(result, "static/audios/audio-from-video.wav")

    resultFile = open('result.txt', 'w')
    resultFile.write(result['text'].lower().replace(',', '').replace('.', ''))
    resultFile.close()

# # Transcribe using Python Speech Recognition Library
# r = sr.Recognizer()
# with sr.AudioFile('/audios/audio-from-video.wav') as source:
#     r.adjust_for_ambient_noise(source)
#     audio_text = r.record(source)
#     try:
#         text = r.recognize_sphinx(audio_text)
#         print('Converting audio transcripts into text...')
#         print('text - ')
#         print(text)
#         print(' end ')
#     except sr.UnknownValueError:
#         print("Sorry, speech recognition could not understand audio")
#     except sr.RequestError as e:
#         print(f"Request error occurred: {e}")