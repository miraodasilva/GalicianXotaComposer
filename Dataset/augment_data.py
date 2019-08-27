from magenta.music import melodies_lib as mlib
from magenta.music import midi_io
import os
import shutil

def augment_data(in_dir,out_dir):
	if os.path.isdir(out_dir):
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)
	for i,file in enumerate(os.listdir(in_dir)):
		for step in range(-12,13):
			try:
				melody = mlib.midi_file_to_melody(in_dir + file)
			except:
				print("error parsing melody")
				continue
			melody.transpose(i)
			seq = melody.to_sequence()
			file_name = out_dir  + file[:-4] + "_" + str(step) + ".mid"
			midi_io.sequence_proto_to_midi_file(seq,file_name)
