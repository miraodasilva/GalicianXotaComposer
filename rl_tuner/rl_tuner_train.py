# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Code to train a MelodyQ model.

To run this code on your local machine:
$ bazel run magenta/models/rl_tuner:rl_tuner_train -- \
--note_rnn_checkpoint_dir 'path' --midi_primer 'primer.mid' \
--training_data_path 'path.tfrecord'
"""
import os
from os import makedirs
from os.path import exists
# internal imports

import matplotlib
# Need to use 'Agg' option for plotting and saving files from command line.
# Can't use 'Agg' in RL Tuner because it breaks plotting in notebooks.
# pylint: disable=g-import-not-at-top
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # pylint: disable=unused-import
import tensorflow as tf

from magenta.models.rl_tuner import rl_tuner
from magenta.models.rl_tuner import rl_tuner_ops
# pylint: enable=g-import-not-at-top

#NEW
tf.logging.set_verbosity(tf.logging.INFO)
#END OF NEW
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('output_dir', '',
                           'Directory where the model will save its'
                           'compositions and checkpoints (midi files)')
tf.app.flags.DEFINE_string('note_rnn_checkpoint_dir', '',
                           'Path to directory holding checkpoints for note rnn'
                           'melody prediction models. These will be loaded into'
                           'the NoteRNNLoader class object. The directory '
                           'should contain a train subdirectory')
tf.app.flags.DEFINE_string('note_rnn_checkpoint_name', 'note_rnn.ckpt',
                           'Filename of a checkpoint within the '
                           'note_rnn_checkpoint_dir directory.')
tf.app.flags.DEFINE_string('note_rnn_type', 'default',
                           'If `default`, will use the basic LSTM described in '
                           'the research paper. If `basic_rnn`, will assume '
                           'the checkpoint is from a Magenta basic_rnn model.')
tf.app.flags.DEFINE_string('midi_primer', './testdata/primer.mid',
                           'A midi file that can be used to prime the model')
tf.app.flags.DEFINE_integer('training_steps', 1000000,
                            'The number of steps used to train the model')
tf.app.flags.DEFINE_integer('exploration_steps', 500000,
                            'The number of steps over which the models'
                            'probability of taking a random action (exploring)'
                            'will be annealed from 1.0 to its normal'
                            'exploration probability. Typically about half the'
                            'training_steps')
tf.app.flags.DEFINE_string('exploration_mode', 'boltzmann',
                           'Can be either egreedy for epsilon-greedy or '
                           'boltzmann, which will sample from the models'
                           'output distribution to select the next action')
tf.app.flags.DEFINE_integer('output_every_nth', 50000,
                            'The number of steps before the model will evaluate'
                            'itself and store a checkpoint')
tf.app.flags.DEFINE_integer('num_notes_in_melody', 32,
                            'The number of notes in each composition')
tf.app.flags.DEFINE_float('reward_scaler', 0.1,
                          'The weight placed on music theory rewards')
tf.app.flags.DEFINE_string('training_data_path', '',
                           'Directory where the model will get melody training'
                           'examples')
tf.app.flags.DEFINE_string('algorithm', 'q',
                           'The name of the algorithm to use for training the'
                           'model. Can be q, psi, or g')
#NEW
tf.app.flags.DEFINE_boolean('attention'  , False,
                           'Whether the RNN we are using is using Attention '
                           'mechanisms. Only works for basic_rnn.')
tf.app.flags.DEFINE_string('section', 'A', 'which section we want to compose')
tf.app.flags.DEFINE_string('reward_mode', 'MUST_SELECT_REWARD_MODE', 
                           'which reward mode we want to use for the training')
tf.app.flags.DEFINE_boolean('just_generate'  , False,
                           'Whether the Tuner should train or simply generate'
                           'without training.')
#END OF NEW
#EXTRA
#tf.app.flags.DEFINE_integer('eighth_note_reward',10,
#                            'determines the reward for the eighth note in section A,' 
#                            '(used in IRL only).')
#END OF EXTRA

def main(_):
  if(not FLAGS.attention):
    hparams = (rl_tuner_ops.basic_rnn_hparams()
               if FLAGS.note_rnn_type == 'basic_rnn'
               else rl_tuner_ops.default_hparams())
  else:
    hparams = rl_tuner_ops.attention_rnn_hparams()

  dqn_hparams = tf.contrib.training.HParams(random_action_probability=0.1,
                                            store_every_nth=1,
                                            train_every_nth=5,
                                            minibatch_size=32,
                                            discount_rate=0.5,
                                            max_experience=100000,
                                            target_network_update_rate=0.01)

  output_dir = os.path.join(FLAGS.output_dir, FLAGS.algorithm)
  output_ckpt = FLAGS.algorithm + '.ckpt'
  backup_checkpoint_file = os.path.join(FLAGS.note_rnn_checkpoint_dir,
                                        FLAGS.note_rnn_checkpoint_name)

  #NEW
  if not exists(FLAGS.output_dir):
      makedirs(FLAGS.output_dir)
  out_path = os.path.join(FLAGS.output_dir,"params.txt")
  file = open(out_path,"w")
  d = FLAGS.flag_values_dict()
  file.write("FLAGS:\n")
  for i in d:
    file.write(i+":   "+str(d[i])+ "\n")
  file.write("\nHPARAMS:\n")
  d2 = hparams.values()
  for i in d2:
    file.write(i+":   "+str(d2[i])+ "\n")
  file.close()
  #END OF NEW

  rlt = rl_tuner.RLTuner(output_dir,
                         midi_primer=FLAGS.midi_primer,
                         dqn_hparams=dqn_hparams,
                         reward_scaler=FLAGS.reward_scaler,
                         save_name=output_ckpt,
                         output_every_nth=FLAGS.output_every_nth,
                         note_rnn_checkpoint_dir=FLAGS.note_rnn_checkpoint_dir,
                         note_rnn_checkpoint_file=backup_checkpoint_file,
                         note_rnn_type=FLAGS.note_rnn_type,
                         note_rnn_hparams=hparams,
                         num_notes_in_melody=FLAGS.num_notes_in_melody,
                         exploration_mode=FLAGS.exploration_mode,
                         algorithm=FLAGS.algorithm,
                         #NEW
                         reward_mode=FLAGS.reward_mode,
                         attention=FLAGS.attention,
                         section=FLAGS.section,
                         key = rl_tuner_ops.C_MAJOR_KEY,
                         tonic = rl_tuner_ops.C_MAJOR_TONIC,
                         scale = rl_tuner_ops.C_MAJOR_SCALE,
                        
                         )
  rlt.evaluate_music_theory_metrics(num_compositions=1000)
  tf.logging.info('Saving images and melodies to: %s', rlt.output_dir)
  #NEW
  for i in range(100):
    rlt.generate_music_sequence(visualize_probs=True, title='pre_rl'+str(i), prob_image_name="pre_rl"+str(i)+".png")
 
  #END OF NEW
  if not FLAGS.just_generate:
    tf.logging.info('Training...')
    rlt.train(num_steps=FLAGS.training_steps,
              exploration_period=FLAGS.exploration_steps)

    tf.logging.info('Finished training. Saving output figures and composition.')
    rlt.plot_rewards(image_name='Rewards-' + FLAGS.algorithm + '.eps')
    #NEW
    for i in range(100):
      rlt.generate_music_sequence(visualize_probs=True, title=FLAGS.algorithm,
                                  prob_image_name=FLAGS.algorithm + '.png')
    rlt.plot_evaluation()
    #END OF NEW
    rlt.save_model_and_figs(FLAGS.algorithm)

    tf.logging.info('Calculating music theory metric stats for 1000 '
                    'compositions.')
    
    rlt.evaluate_music_theory_metrics(num_compositions=1000,key = rl_tuner_ops.C_MAJOR_KEY,tonic_note = rl_tuner_ops.C_MAJOR_TONIC)
  

def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
  console_entry_point()
