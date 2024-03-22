import speech_recognition as sr
import moviepy.editor as mp
import numpy as np
import wave
import os 
from pocketsphinx import *

def convert_audio_to_text(input_video_path):     
    output_audio_path = "output.wav"
    
    clip = mp.VideoFileClip(input_video_path)
    audio = clip.audio
    audio.write_audiofile(output_audio_path)
    
    r = sr.Recognizer()
    with sr.AudioFile(output_audio_path) as source:
        audio_data = r.record(source)
    
    try:
        text = r.recognize_google(audio_data)
        words = text.split()
        timestamps = []
    
        for word in words:
            if hasattr(r, 'recognize_timestamps'):
                timestamps += r.recognize_timestamps(audio_data, word)
            else:
                with wave.open("output.wav", "rb") as wav_file:
                    audio_frames = wav_file.getnframes()
                    sample_width = wav_file.getsampwidth()
                    channels = wav_file.getnchannels()
    
        duration = audio_frames / 44100
        average_word_duration = duration / len(words)
    
        start_time = 0
        for _ in range(len(timestamps), len(words)):
            timestamps.append(start_time)
            start_time += average_word_duration
    
        output_text = ""
        for i, word in enumerate(words):
            output_text += f"{timestamps[i]:.2f} - {word}\n"
    
        with open("output.txt", "w") as f:
            f.write(output_text)
    
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    print("Audio converted to text with timestamps successfully!")

def search_word_in_transcript(word, transcript_file):
    with open(transcript_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if word.lower() in line.lower():
            timestamp, found_word = line.split(' - ')
            return timestamp.strip()
            
def extract_all_words_from_file(file_path):         
            with open(file_path, 'r') as file:        
                content = file.read()
                words = content.split()
                return words
               

if __name__ == "__main__":
        transcript_file_path = "output.txt" 
        file_path = 'uploads\\keyword.txt'
        input_video_path="uploads/demo.mp4"
        output_audio_path="output.wav"
        convert_audio_to_text(input_video_path)
        search_word = extract_all_words_from_file(file_path) 
        timestamp_value = search_word_in_transcript(search_word[0], transcript_file_path)
        print(f"Timestamp value: {timestamp_value}")
    