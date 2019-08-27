#PBS -l nodes=gpu10
uptime
echo START	
export ROOT_DIR=/vol/gpudata/rs2517/venv1/myApp
export CUDA_HOME=/vol/gpudata/cuda/9.0.176
export PATH=${PATH}:${CUDA_HOME}/bin
export INPUT=${ROOT_DIR}/inputs_revised
export OUTPUT=${ROOT_DIR}/outputs_revised 
export MODEL=${ROOT_DIR}/lib/python2.7/site-packages/magenta/models/melody_rnn

#source ${ROOT_DIR}/bin/activate

. /vol/cuda/9.0.176/setup.sh
#batch size was 128, 23.06.19
python ${MODEL}/melody_rnn_train.py --config=basic_rnn --run_dir=${OUTPUT}/RNN/magenta+galician_rnn/ --sequence_example_file=${INPUT}/sequence_example_test/training_melodies.tfrecord --hparams="batch_size=88,rnn_layer_sizes=[512,512]" --num_training_steps=5000 --num_checkpoints=1000 --eval

echo END
uptime

