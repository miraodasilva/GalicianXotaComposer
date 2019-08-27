uptime
echo START	
export ROOT_DIR=/vol/gpudata/rs2517/venv1/myApp
export CUDA_HOME=/vol/gpudata/cuda/9.0.176
export PATH=${PATH}:${CUDA_HOME}/bin
export OUTPUT=${ROOT_DIR}/outputs_revised/ACC_COMPARISON/ 
export CHECKPOINT=${ROOT_DIR}/checkpoints_revised
export MODEL=${ROOT_DIR}/lib/python2.7/site-packages/magenta/models/rl_tuner

. /vol/cuda/9.0.176/setup.sh

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/normal/ --note_rnn_checkpoint_dir=${CHECKPOINT}/galician --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="None" --just_generate=True

python ${MODEL}/rl_tuner_train.py --output_dir=${OUTPUT}/overfit/ --note_rnn_checkpoint_dir=${CHECKPOINT}/galician_overfit --note_rnn_type="basic_rnn"  --reward_scaler=2.0 --midi_primer=None --exploration_mode="egreedy" --algorithm="q" --attention=False --num_notes_in_melody=96 --section="None" --reward_mode="None" --just_generate=True

echo END
uptime