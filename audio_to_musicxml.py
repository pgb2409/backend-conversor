import librosa
from music21 import stream, note, tempo, meter

def convertir_mp3_a_musicxml(ruta_mp3, ruta_salida):
    y, sr = librosa.load(ruta_mp3)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    bpm = librosa.beat.tempo(y=y, sr=sr)[0]

    partitura = stream.Score()
    parte = stream.Part()
    parte.append(tempo.MetronomeMark(number=bpm))
    parte.append(meter.TimeSignature("4/4"))

    for t in onset_times:
        n = note.Note("C4", quarterLength=0.25)
        n.offset = t
        parte.append(n)

    partitura.append(parte)
    partitura.write("musicxml", fp=ruta_salida)
