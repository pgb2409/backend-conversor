import sys
import os
import librosa
import music21
import numpy as np
import soundfile as sf

def convert_to_musicxml(audio_path):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join('outputs', base_name + '.musicxml')

    y, sr = librosa.load(audio_path, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    score = music21.stream.Score()
    part = music21.stream.Part()
    part.append(music21.tempo.MetronomeMark(number=int(tempo)))

    for t in beat_times:
        dur = music21.duration.Duration(1)
        note = music21.note.Note('C4', duration=dur)
        part.append(note)

    score.append(part)
    score.write('musicxml', fp=output_path)
    print(f'Archivo generado: {output_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python audio_to_musicxml.py archivo.mp3')
        sys.exit(1)

    audio_file = sys.argv[1]
    convert_to_musicxml(audio_file)
