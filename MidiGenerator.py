from midiutil.MidiFile import MIDIFile
import math

class MidiGenerator:
    def __init__(self, filename, track, channel, volume, tempo, default_duration):
        self.filename = filename
        self.track = track
        self.channel = channel
        self.volume = volume
        self.tempo = tempo
        self.default_duration = default_duration

        # Create MIDI object with one track
        self.mf = MIDIFile(1)

        # The first track
        self.time = 0
        self.mf.addTrackName(self.track, self.time, self.filename)
        self.mf.addTempo(self.track, self.time, self.tempo)

        # Eb major pentatonic
        self.notes = [0+48, 3+48, 5+48, 7+48, 10+48]


    def write_int(self, i):
        note = self.notes[i%len(self.notes)] + 12*math.floor(i/len(self.notes))
        self.mf.addNote(self.track, self.channel, note, self.time, self.default_duration+0.5, self.volume)
        self.time += self.default_duration


    def write_file(self, outf):
        self.mf.writeFile(outf)