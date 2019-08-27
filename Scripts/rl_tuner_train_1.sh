uptime
echo START	
export ROOT_DIR=/vol/gpudata/rs2517/venv1/myApp
export CUDA_HOME=/vol/gpudata/cuda/9.0.176
export PATH=${PATH}:${CUDA_HOME}/bin
export OUTPUT=${ROOT_DIR}/outputs_revised/RL_TUNER_2/ 
export CHECKPOINT=${ROOT_DIR}/checkpoints_revised
export MODEL=${ROOT_DIR}/lib/python2.7/site-packages/magenta/models/rl_tuner

#source ${ROOT_DIR}/bin/activate

. /vol/cuda/9.0.176/setup.sh

#
#magenta
#

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/no_rl --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="None" --just_generate=True
#zero reward
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/zero_reward --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="zero_reward"
#magenta ruleset
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/original_rule_set --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="music_theory_all"
#new rule set
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/new_rule_set/section_A --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="A" --reward_mode="galician_only"

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/new_rule_set/section_B --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="B" --reward_mode="galician_only"
#both rule sets
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/both_rule_sets/section_A --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="A" --reward_mode="music_theory+galician"

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/magenta/both_rule_sets/section_B --note_rnn_checkpoint_dir=${CHECKPOINT}/magenta --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="B" --reward_mode="music_theory+galician"


#
#GALICIAN
#

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/galician/no_rl --note_rnn_checkpoint_dir=${CHECKPOINT}/galician --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="None" --just_generate=True
#zero reward
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/galician/zero_reward --note_rnn_checkpoint_dir=${CHECKPOINT}/galician --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="zero_reward"
#magenta ruleset
python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/galician/original_rule_set --note_rnn_checkpoint_dir=${CHECKPOINT}/galician --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="music_theory_all"



echo END
uptime
