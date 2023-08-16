from dict import dict
import Ham2SIGML
import socket
import time
import os
import videototext as vt

def transcribeText(videoName):
    vt.convert_video_to_text(os.path.join("static", videoName), os.path.join("static", "audios", "audio-from-video.wav"))

def convert(videoName):
    transcribeText(videoName)
    
    with open('result.txt') as file:
        data = file.read().split()
        print(data)

    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>\t
<sigml>""")
        
    for i in data:
        # handling HamNoSys encoding-decoding via Unicode characters
        if i not in dict:
            print(i, "is not in dictionary, continuing...")
            continue

        res = ''.join(r'\u{:04x}'.format(ord(chr)) for chr in dict[i])
        hamList = [res.encode().decode('unicode_escape')]

        print(hamList)
        
        Ham2SIGML.readInput(hamList, i)
        
        time.sleep(0.5)
    with open(os.path.join("static", "sigml", "SiGML-output.sigml"), "a") as f:
        f.write("""\n</sigml>""")

    print("SiGML written out.")
