#Make sure to add the following lines to the end of function restore_vars_from_checkpoint(self, checkpoint_dir) from rl_tuner/note_rnn_loader.py
#tf.logging.info("saved it")
#file_name = "/home/miraodasilva/Desktop/rl_tuner_save.ckpt"

#if self.scope == 'q_network':
#  saver_2.save(self.session, "/home/miraodasilva/Desktop/rl_tuner_save.ckpt")

export OUTPUT=/home/miraodasilva/Desktop/post_thesis/outputs 
export CHECKPOINT=/home/miraodasilva/Desktop/post_thesis/checkpoints
export MODEL=~/anaconda2/envs/magenta/lib/python2.7/site-packages/magenta/models/rl_tuner

source activate magenta

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/RL/whatever/ --note_rnn_checkpoint_dir=/home/miraodasilva/Desktop/RL_RNN_Composer_CLEAN/Checkpoints/auxiliary_code/rl_tuner_checkpoint --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="None" --just_generate=True

