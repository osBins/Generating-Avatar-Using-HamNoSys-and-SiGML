from dict import dict
import Ham2SIGML
import time
import os
import videototext as vt

from sentimentAnalysis import sentimentFinder

def transcribeText(videoName):
    vt.convert_video_to_text(os.path.join("static", videoName), os.path.join("static", "audios", "audio-from-video.wav"))

def convert(videoName):
    transcribeText(videoName)
    
    with open('result.txt') as file:
        data = file.read().split()
        sentimentFinder(data)
        print(data)

    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>\t
<sigml>""")
    
    from sentiments import sentiments
    for word in data:
        if word not in dict:
            print(word, "is not in dictionary, continuing...")
            continue

        # handling HamNoSys encoding-decoding via Unicode characters
        res = ''.join(r'\u{:04x}'.format(ord(chr)) for chr in dict[word])
        hamList = [res.encode().decode('unicode_escape')]
        
        Ham2SIGML.readInput(hamList, word, sentiments[word])
        
        time.sleep(0.1)
    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "a") as f:
        f.write("""\n</sigml>""")

    print("SiGML written out.")
