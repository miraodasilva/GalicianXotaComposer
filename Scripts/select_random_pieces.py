import os
from glob import glob
import random
from shutil import copyfile

N_PIECES = 5


def copy_midi_wav(in_dir, out_dir, path, name):
    in_path = os.path.join(in_dir, path)
    out_path = os.path.join(out_dir, f"{name}.mid")
    print(f"copying from {in_path} to {out_path}")
    copyfile(in_path, out_path)
    wav_path = out_path.replace(".mid", ".wav")
    os.system(f"fluidsynth {out_path} -F {wav_path}")
    return wav_path


def make_samples(sectionA_dir, sectionB_dir, midi_basename="q*.mid", out_dir=None):
    all_sectionA_midis = glob(os.path.join(sectionA_dir, midi_basename))
    sectionA_midis = [os.path.split(x)[1] for x in random.sample(all_sectionA_midis, 4 * N_PIECES)]
    all_sectionB_midis = glob(os.path.join(sectionB_dir, midi_basename))
    sectionB_midis = [os.path.split(x)[1] for x in random.sample(all_sectionB_midis, 2 * N_PIECES)]
    for n in range(N_PIECES):
        piece_out_dir = os.path.join(out_dir, f"piece_{n}")
        os.makedirs(piece_out_dir, exist_ok=True)
        copy_midi_wav(sectionA_dir, piece_out_dir, sectionA_midis[4 * n], "A1")
        copy_midi_wav(sectionA_dir, piece_out_dir, sectionA_midis[4 * n + 1], "A2")
        copy_midi_wav(sectionA_dir, piece_out_dir, sectionA_midis[4 * n + 2], "A3")
        copy_midi_wav(sectionA_dir, piece_out_dir, sectionA_midis[4 * n + 3], "A4")
        copy_midi_wav(sectionB_dir, piece_out_dir, sectionB_midis[2 * n], "B1")
        copy_midi_wav(sectionB_dir, piece_out_dir, sectionB_midis[2 * n + 1], "B2")
        os.system(
            "sox {} {} {} {} {} {} {}".format(
                os.path.join(piece_out_dir, "A1.wav"),
                os.path.join(piece_out_dir, "A2.wav"),
                os.path.join(piece_out_dir, "B1.wav"),
                os.path.join(piece_out_dir, "B2.wav"),
                os.path.join(piece_out_dir, "A3.wav"),
                os.path.join(piece_out_dir, "A4.wav"),
                os.path.join(piece_out_dir, "full_piece.wav"),
            )
        )

def make_samples_no_section(dir, midi_basename="q*.mid", out_dir=None):
    all_midis = glob(os.path.join(dir, midi_basename))
    midis = [os.path.split(x)[1] for x in random.sample(all_midis, 6 * N_PIECES)]
    for n in range(N_PIECES):
        piece_out_dir = os.path.join(out_dir, f"piece_{n}")
        os.makedirs(piece_out_dir, exist_ok=True)
        copy_midi_wav(dir, piece_out_dir, midis[6 * n], "A1")
        copy_midi_wav(dir, piece_out_dir, midis[6 * n + 1], "A2")
        copy_midi_wav(dir, piece_out_dir, midis[6 * n + 2], "A3")
        copy_midi_wav(dir, piece_out_dir, midis[6 * n + 3], "A4")
        copy_midi_wav(dir, piece_out_dir, midis[6 * n + 4], "B1")
        copy_midi_wav(dir, piece_out_dir, midis[6 * n + 5], "B2")
        os.system(
            "sox {} {} {} {} {} {} {}".format(
                os.path.join(piece_out_dir, "A1.wav"),
                os.path.join(piece_out_dir, "A2.wav"),
                os.path.join(piece_out_dir, "B1.wav"),
                os.path.join(piece_out_dir, "B2.wav"),
                os.path.join(piece_out_dir, "A3.wav"),
                os.path.join(piece_out_dir, "A4.wav"),
                os.path.join(piece_out_dir, "full_piece.wav"),
            )
        )

def main():
    in_dir = "../Results/galician"
    out_dir = "../MIDI_Pieces_for_Evaluation/galician"
    make_samples(
        os.path.join(in_dir, "both_rule_sets/section_A/q"),
        os.path.join(in_dir, "both_rule_sets/section_B/q"),
        out_dir=os.path.join(out_dir, "both_rule_sets"),
    )
    make_samples(
        os.path.join(in_dir, "new_rule_set/section_A/q"),
        os.path.join(in_dir, "new_rule_set/section_B/q"),
        out_dir=os.path.join(out_dir, "new_rule_set"),
    )
    make_samples_no_section(
        os.path.join(in_dir, "original_rule_set/q"),
        out_dir=os.path.join(out_dir, "original_rule_set"),
    )
    make_samples_no_section(
        os.path.join(in_dir, "no_rl/q"),
        out_dir=os.path.join(out_dir, "no_rl"),
        midi_basename="pre_rl*.mid",
    )


if __name__ == "__main__":
    main()