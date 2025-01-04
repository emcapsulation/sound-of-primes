from MidiGenerator import MidiGenerator
from PrimeGenerator import PrimeGenerator


def file_to_midi(filename):
    pg = PrimeGenerator()
    div_list = [pg.get_num_prime_factors(x) for x in range(2, 1001)];

    # Default settings
    track = 0
    channel = 0
    volume = 100
    tempo = 130*2
    default_duration = 1

    # Create MIDI
    mf = MidiGenerator(filename, track, channel, volume, tempo, default_duration)
    for d in div_list:
        mf.write_int(d)

    # Write it to disk
    with open("out/" + filename + ".mid", 'wb') as outf:
        mf.write_file(outf)


file_to_midi("prime_omega");