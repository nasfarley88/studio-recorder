import pyaudio
import sys
import wave
import array

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
THRESHOLD = 2000

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE, 
                input=True,
                output=True,
                frames_per_buffer=chunk)

print("* recording")
i = 0
try:
    while True:
        i += 1
        data = array.array('h', stream.read(int(RATE*RECORD_SECONDS)))
        if not is_silent(data):
            print("Recording iteration {} (with a max of {})".format(i, max(data)))
            wf = wave.open("demo{}.wav".format(i), "wb")
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(data)
            wf.close()
        else:
            print("Not recording iteration {}".format(i))
except KeyboardInterrupt:
    print("Interrupted by keyboard")
finally:
    print("* done")

    stream.stop_stream()
    stream.close()
    p.terminate()
