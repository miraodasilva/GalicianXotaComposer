import subprocess
import shutil
import os


def create_tf_record(in_dir,out_dir):
	if os.path.isdir(out_dir):
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)
	tfrecord_command = "convert_dir_to_note_sequences --input_dir=%s --output_file=%s --recursive" % (in_dir,out_dir + "dataset.tfrecord")
	process = subprocess.Popen(tfrecord_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

def create_sequence_examples(in_file,out_dir):
	if os.path.isdir(out_dir):
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)
	seq_ex_command = "melody_rnn_create_dataset \
	--config=basic_rnn \
	--input=%s \
	--output_dir=%s \
	--eval_ratio=0.00" % (in_file,out_dir)
	process = subprocess.Popen(seq_ex_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
