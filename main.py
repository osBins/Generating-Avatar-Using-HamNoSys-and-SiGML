from dict import dict
import Ham2SIGML
# import socket
import time
import os
import videototext as vt

from sentimentAnalysis import sentimentFinder

# import string
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer

# Utility function to convert to sov format
def english_to_sov(english_text):
    # Split the English text into words
    words = english_text.split()
    
    # Rearrange the words to follow the SOV structure
    if len(words) >= 3:
        subject = words[0]
        verb = words[-1]
        object_ = " ".join(words[1:-1])
        sov_sentence = f"{subject} {object_} {verb}"
    else:
        # If the sentence is too short to rearrange, use the original sentence
        sov_sentence = " ".join(words)
    
    return sov_sentence

def transcribeText(videoName):
    vt.convert_video_to_text(os.path.join("static", videoName), os.path.join("static", "audios", "audio-from-video.wav"))

def convert(videoName):
    transcribeText(videoName)
    
    with open('result.txt') as file:
        data = file.read().split()
        sentimentFinder(data)
        print(data)

    # BASIC TEXT PREPROCESSING
    # # Tokenization
    # words = word_tokenize(data)

    # # Remove punctuation and convert to lowercase
    # words = [word.lower() for word in words if word.isalnum()]

    # # Remove stop words
    # stop_words = set(stopwords.words('english'))
    # filtered_words = [word for word in words if word not in stop_words]

    # # Lemmatization
    # lemmatizer = WordNetLemmatizer()
    # lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # # Print the preprocessed text
    # preprocessed_text = " ".join(lemmatized_words)
    # print(preprocessed_text)

    # sov_text = english_to_sov(preprocessed_text)
    # data = sov_text

    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>\t
<sigml>""")

    # CLEAR THE FILE BEFORE WRITING ANYTHING
    with open(os.path.join('static', 'sigml', 'hamnosys-generated'), "w", encoding='utf-8', errors='replace') as f:
        f.write("")
        
    from sentiments import sentiments
    for i in data:
        # handling HamNoSys encoding-decoding via Unicode characters
        if i not in dict:
            print(i, "is not in dictionary, continuing...")
            continue

        res = ''.join(r'\u{:04x}'.format(ord(chr)) for chr in dict[i])
        hamList = [res.encode().decode('unicode_escape')]

        print(hamList)
        
        # CORRESPONDING HAMNOSYS
        with open(os.path.join('static', 'sigml', 'hamnosys-generated'), "a", encoding='utf-8', errors='replace') as f:
            f.write(res + "-" + i);
            f.write("\n")
        
        Ham2SIGML.readInput(hamList, i, sentiments[i])
        
        time.sleep(0.05)
    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "a") as f:
        f.write("""\n</sigml>""")

    print("SiGML written out.")
