import mido
from mido import Message, MidiFile, MidiTrack
import os
import shutil

def separate_tracks(in_dir,out_dir,meta):
	if os.path.isdir(out_dir):
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)

	for i,file in enumerate(sorted(os.listdir(in_dir))):
		try:
			old_mid = MidiFile(in_dir + file)
		except:
			print("bad file")
			#signalling the bad files in the dataset
			meta[i] += ["bad file"]
			continue
		j=0
		for t in old_mid.tracks:
			#Just a reference number to make sure the track is worth taking
			if len([mes for mes in t])>100:
				new_mid = MidiFile()
				new_mid.tracks = [t]		
				new_mid.save(out_dir + file[:-4] + "_" + str(j) + ".mid" )
				j+=1
		#number of tracks
		meta[i] += [str(j)]
		#length in minutes
		meta[i] += [str(old_mid.length)]
	return meta
	
	
