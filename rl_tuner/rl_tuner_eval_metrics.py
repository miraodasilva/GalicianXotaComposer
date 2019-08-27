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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.p
# See the License for the specific language governing permissions and
# limitations under the License.

"""Code to evaluate how well an RL Tuner conforms to music theory rules."""

# internal imports
#NEW
import os
#END OF NEW
import numpy as np
import tensorflow as tf
from magenta.models.rl_tuner import rl_tuner_ops
import pickle
#NEW
from magenta.music import melodies_lib as mlib

NOTE_OFF = 1
NO_EVENT = 0

BAR_LENGTH=12
SECTION_N_BARS=8
SECTION_A_1=0
SECTION_A_2=SECTION_N_BARS*BAR_LENGTH
SECTION_B_1=SECTION_N_BARS*BAR_LENGTH*2
SECTION_B_2=SECTION_N_BARS*BAR_LENGTH*3
SECTION_A_3=SECTION_N_BARS*BAR_LENGTH*4
SECTION_A_4=SECTION_N_BARS*BAR_LENGTH*5
#END OF NEW

def compute_composition_stats(rl_tuner,
                              num_compositions=10000,
                              composition_length=32,
                              key=rl_tuner_ops.C_MAJOR_KEY,
                              tonic_note=rl_tuner_ops.C_MAJOR_TONIC):
  """Uses the model to create many compositions, stores statistics about them.

  Args:
    rl_tuner: An RLTuner object.
    num_compositions: The number of compositions to create.
    composition_length: The number of beats in each composition.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
    tonic_note: The tonic/1st note of the desired key.
  Returns:
    A dictionary containing the computed statistics about the compositions.
  """
  stat_dict = initialize_stat_dict()

  for i in range(num_compositions):
    stat_dict = compose_and_evaluate_piece(
        rl_tuner,
        stat_dict,
        composition_length=composition_length,
        key=key,
        tonic_note=tonic_note)
    if i % (num_compositions / 10) == 0:
      stat_dict['num_compositions'] = i
      stat_dict['total_notes'] = i * composition_length

  stat_dict['num_compositions'] = num_compositions
  stat_dict['total_notes'] = num_compositions * composition_length

  tf.logging.info(get_stat_dict_string(stat_dict))
  #NEW
  out_path = os.path.join(rl_tuner.output_dir,"pre_rl_music_theory_stats.txt")
  dictionary_path = os.path.join(rl_tuner.output_dir,"pre_rl_music_theory_stats.pickle")
  if os.path.exists(out_path):
    out_path =  os.path.join(rl_tuner.output_dir,"post_rl_music_theory_stats.txt")
    dictionary_path = os.path.join(rl_tuner.output_dir,"post_rl_music_theory_stats.pickle")
  file = open(out_path,"w")
  file.write(get_stat_dict_string(stat_dict))
  file.close()
  """
  with open(dictionary_path,"wb") as handle:
    pickle.dump(stat_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)

  #sanity check
  with open(dictionary_path,"rb") as handle:
    loaded_dict = pickle.load(handle)

  if stat_dict != loaded_dict:
    tf.logging.fatal('Error! Dictionary was not saved properly')
    print(stat_dict)
    print(loaded_dict)
  """
  #END OF NEW
  return stat_dict

#NEW
def compute_composition_stats_from_midi(rl_tuner,base_dir,
                              key=rl_tuner_ops.C_MAJOR_KEY,
                              tonic_note=rl_tuner_ops.C_MAJOR_TONIC):
  """Uses the model to create many compositions, stores statistics about them.

  Args:
    rl_tuner: An RLTuner object.
    num_compositions: The number of compositions to create.
    composition_length: The number of beats in each composition.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
    tonic_note: The tonic/1st note of the desired key.
  Returns:
    A dictionary containing the computed statistics about the compositions.
  """
  stat_dict = initialize_stat_dict()
  total_notes = 0
  num_compositions = 0
  for file in os.listdir(base_dir):
    if ".mid" not in file:
      continue
    melody = mlib.midi_file_to_melody(base_dir+file)
    piece = melody._events
    piece = rl_tuner_ops.encoder(piece,0)
    print(piece)
    broken_piece = False
    for i in piece:
      if i>37:
        broken_piece=True
        break
    if broken_piece:
      tf.logging.info("continue")
      continue    
    stat_dict = evaluate_piece_from_midi(rl_tuner,
        piece,
        stat_dict,
        key=key,
        tonic_note=tonic_note)
    total_notes += len(piece)
    num_compositions+=1 
  stat_dict['total_notes'] = total_notes
  stat_dict['num_compositions'] = num_compositions
  tf.logging.info(get_stat_dict_string(stat_dict))
  #NEW
  out_path = os.path.join(base_dir,"music_theory_stats.txt")
  file = open(out_path,"w")
  file.write(get_stat_dict_string(stat_dict))
  file.close()
  #END OF NEW
  return stat_dict

def compute_composition_stats_from_sequence(rl_tuner,piece,
                              key=rl_tuner_ops.C_MAJOR_KEY,
                              tonic_note=rl_tuner_ops.C_MAJOR_TONIC):
  """Uses the model to create many compositions, stores statistics about them.

  Args:
    rl_tuner: An RLTuner object.
    num_compositions: The number of compositions to create.
    composition_length: The number of beats in each composition.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
    tonic_note: The tonic/1st note of the desired key.
  Returns:
    A dictionary containing the computed statistics about the compositions.
  """
  stat_dict = initialize_stat_dict()
  total_notes = 0
  num_compositions = 0  
  stat_dict = evaluate_piece_from_midi(rl_tuner,
      piece,
      stat_dict,
      key=key,
      tonic_note=tonic_note)
  total_notes += len(piece)
  num_compositions=1 
  stat_dict['total_notes'] = total_notes
  stat_dict['num_compositions'] = num_compositions
  tf.logging.info(get_stat_dict_string(stat_dict))
  #NEW
  out_path = os.path.join("./","music_theory_stats.txt")
  file = open(out_path,"w")
  file.write(get_stat_dict_string(stat_dict))
  file.close()
  #END OF NEW
  return stat_dict
#END OF NEW

# The following functions compute evaluation metrics to test whether the model
# trained successfully.
def get_stat_dict_string(stat_dict, print_interval_stats=True):
  """Makes string of interesting statistics from a composition stat_dict.

  Args:
    stat_dict: A dictionary storing statistics about a series of compositions.
    print_interval_stats: If True, print additional stats about the number of
      different intervals types.
  Returns:
    String containing several lines of formatted stats.
  """
  tot_notes = float(stat_dict['total_notes'])
  tot_comps = float(stat_dict['num_compositions'])

  return_str = 'Total compositions: ' + str(tot_comps) + '\n'
  return_str += 'Total notes:' + str(tot_notes) + '\n'

  return_str += '\tCompositions starting with tonic: '
  return_str += str(float(stat_dict['num_starting_tonic'])) + '\n'
  return_str += '\tCompositions with unique highest note:'
  return_str += str(float(stat_dict['num_high_unique'])) + '\n'
  return_str += '\tCompositions with unique lowest note:'
  return_str += str(float(stat_dict['num_low_unique'])) + '\n'
  return_str += '\tNumber of resolved leaps:'
  return_str += str(float(stat_dict['num_resolved_leaps'])) + '\n'
  return_str += '\tNumber of double leaps:'
  return_str += str(float(stat_dict['num_leap_twice'])) + '\n'
  return_str += '\tNotes not in key:' + str(float(
      stat_dict['notes_not_in_key'])) + '\n'
  return_str += '\tNotes in motif:' + str(float(
      stat_dict['notes_in_motif'])) + '\n'
  return_str += '\tNotes in repeated motif:'
  return_str += str(float(stat_dict['notes_in_repeated_motif'])) + '\n'
  return_str += '\tNotes excessively repeated:'
  return_str += str(float(stat_dict['num_repeated_notes'])) + '\n'
  return_str += '\n'

  num_resolved = float(stat_dict['num_resolved_leaps'])
  total_leaps = (float(stat_dict['num_leap_twice']) + num_resolved)
  if total_leaps > 0:
    percent_leaps_resolved = num_resolved / total_leaps
  else:
    percent_leaps_resolved = np.nan
  return_str += '\tPercent compositions starting with tonic:'
  return_str += str(stat_dict['num_starting_tonic'] / tot_comps) + '\n'
  return_str += '\tPercent compositions with unique highest note:'
  return_str += str(float(stat_dict['num_high_unique']) / tot_comps) + '\n'
  return_str += '\tPercent compositions with unique lowest note:'
  return_str += str(float(stat_dict['num_low_unique']) / tot_comps) + '\n'
  return_str += '\tPercent of leaps resolved:'
  return_str += str(percent_leaps_resolved) + '\n'
  return_str += '\tPercent notes not in key:'
  return_str += str(float(stat_dict['notes_not_in_key']) / tot_notes) + '\n'
  return_str += '\tPercent notes in motif:'
  return_str += str(float(stat_dict['notes_in_motif']) / tot_notes) + '\n'
  return_str += '\tPercent notes in repeated motif:'
  return_str += str(stat_dict['notes_in_repeated_motif'] / tot_notes) + '\n'
  return_str += '\tPercent notes excessively repeated:'
  return_str += str(stat_dict['num_repeated_notes'] / tot_notes) + '\n'
  return_str += '\n'

  for lag in [1, 2, 3]:
    avg_autocorr = np.nanmean(stat_dict['autocorrelation' + str(lag)])
    return_str += '\tAverage autocorrelation of lag' + str(lag) + ':'
    return_str += str(avg_autocorr) + '\n'

  if print_interval_stats:
    return_str += '\n'
    return_str += '\tAvg. num octave jumps per composition:'
    return_str += str(float(stat_dict['num_octave_jumps']) / tot_comps) + '\n'
    return_str += '\tAvg. num sevenths per composition:'
    return_str += str(float(stat_dict['num_sevenths']) / tot_comps) + '\n'
    return_str += '\tAvg. num fifths per composition:'
    return_str += str(float(stat_dict['num_fifths']) / tot_comps) + '\n'
    return_str += '\tAvg. num sixths per composition:'
    return_str += str(float(stat_dict['num_sixths']) / tot_comps) + '\n'
    return_str += '\tAvg. num fourths per composition:'
    return_str += str(float(stat_dict['num_fourths']) / tot_comps) + '\n'
    return_str += '\tAvg. num rest intervals per composition:'
    return_str += str(float(stat_dict['num_rest_intervals']) / tot_comps)
    return_str += '\n'
    return_str += '\tAvg. num seconds per composition:'
    return_str += str(float(stat_dict['num_seconds']) / tot_comps) + '\n'
    return_str += '\tAvg. num thirds per composition:'
    return_str += str(float(stat_dict['num_thirds']) / tot_comps) + '\n'
    #NEW
    return_str += '\tAvg. num same note intervals per composition:'
    return_str += str(float(stat_dict['num_same_note_intervals']) / tot_comps) + '\n'
    return_str += '\tAvg. num minor seconds per composition:'
    return_str += str(float(stat_dict['num_minor_seconds']) / tot_comps) + '\n'
    return_str += '\tAvg. num minor thirds per composition:'
    return_str += str(float(stat_dict['num_minor_thirds']) / tot_comps) + '\n'
    return_str += '\tAvg. num diminished fifths per composition:'
    return_str += str(float(stat_dict['num_diminished_fifths']) / tot_comps) + '\n'
    return_str += '\tAvg. num minor sixths per composition:'
    return_str += str(float(stat_dict['num_minor_sixths']) / tot_comps) + '\n'
    return_str += '\tAvg. num minor sevenths per composition:'
    return_str += str(float(stat_dict['num_minor_sevenths']) / tot_comps) + '\n'
    return_str += '\tAvg. num in key fifths per composition:'
    return_str += str(float(stat_dict['num_in_key_fifths']) / tot_comps) + '\n'
    return_str += '\tAvg. num in key thirds per composition:'
    return_str += str(float(stat_dict['num_in_key_thirds']) / tot_comps) + '\n'

    #END OF NEW
    #return_str += '\tAvg. num in key preferred intervals per composition:'
    #return_str += str(
    #    float(stat_dict['num_in_key_preferred_intervals']) / tot_comps) + '\n'
    return_str += '\tAvg. num special rest intervals per composition:'
    return_str += str(
        float(stat_dict['num_special_rest_intervals']) / tot_comps) + '\n'
    return_str += '\n'
  #NEW
  return_str += '\n'
  return_str += '\tavg. num of correlated intervals in first section: '
  return_str += str(float(stat_dict['num_correlated_intervals'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of larger notes in composition: '
  return_str += str(float(stat_dict['num_larger_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of whole notes in composition: '
  return_str += str(float(stat_dict['num_whole_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of half notes in composition: '
  return_str += str(float(stat_dict['num_half_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of quarter notes in composition: '
  return_str += str(float(stat_dict['num_quarter_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of octave notes in composition: '
  return_str += str(float(stat_dict['num_octave_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of sixteenth notes in composition: '
  return_str += str(float(stat_dict['num_sixteenth_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of early pauses in composition: '
  return_str += str(float(stat_dict['num_early_pauses'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of late quarter notes in composition: '
  return_str += str(float(stat_dict['num_late_quarter_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of late pauses in composition: '
  return_str += str(float(stat_dict['num_late_pauses'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of late note off events in composition: '
  return_str += str(float(stat_dict['num_late_note_off_events'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of last quarter notes in composition: '
  return_str += str(float(stat_dict['num_last_quarter_notes'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of late tonics in composition: '
  return_str += str(float(stat_dict['num_late_tonics'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of sub tonics followed by tonics in composition: '
  return_str += str(float(stat_dict['num_sub_tonics'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tpercentage of sub tonics followed by tonics in composition: '
  return_str += str(float(stat_dict['num_sub_tonics'])/(float(stat_dict['num_sub_tonics'])+float(stat_dict['num_non_sub_tonics']))) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of opposite seconds in composition: '
  return_str += str(float(stat_dict['num_opposite_seconds'])/tot_comps) + '\n'
  return_str += '\n'
  return_str += '\tavg. num of direction changes in composition: '
  return_str += str(float(stat_dict['num_direction_changes'])/tot_comps) + '\n'
  
  #END OF NEW

  return return_str

def compose_and_evaluate_piece(rl_tuner,
                               stat_dict,
                               composition_length=32,
                               key=None,
                               tonic_note=rl_tuner_ops.C_MAJOR_TONIC,
                               sample_next_obs=True):
  """Composes a piece using the model, stores statistics about it in a dict.

  Args:
    rl_tuner: An RLTuner object.
    stat_dict: A dictionary storing statistics about a series of compositions.
    composition_length: The number of beats in the composition.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
    tonic_note: The tonic/1st note of the desired key.
    sample_next_obs: If True, each note will be sampled from the model's
      output distribution. If False, each note will be the one with maximum
      value according to the model.
  Returns:
    A dictionary updated to include statistics about the composition just
    created.
  """
  last_observation = rl_tuner.prime_internal_models()
  rl_tuner.reset_composition()

  for _ in range(composition_length):
    if sample_next_obs:
      action, new_observation, _ = rl_tuner.action(
          last_observation,
          0,
          enable_random=False,
          sample_next_obs=sample_next_obs)
    else:
      action, _ = rl_tuner.action(
          last_observation,
          0,
          enable_random=False,
          sample_next_obs=sample_next_obs)
      new_observation = action

    obs_note = np.argmax(new_observation)

    stat_dict = add_all_stats(rl_tuner,new_observation,obs_note,stat_dict,key,tonic_note)

    rl_tuner.composition.append(np.argmax(new_observation))
    rl_tuner.beat += 1
    last_observation = new_observation

  for lag in [1, 2, 3]:
    stat_dict['autocorrelation' + str(lag)].append(
        rl_tuner_ops.autocorrelate(rl_tuner.composition, lag))

  add_high_low_unique_stats(rl_tuner, stat_dict)

  return stat_dict

#NEW
def evaluate_piece_from_midi(rl_tuner,piece,
                               stat_dict,
                               key=None,
                               tonic_note=rl_tuner_ops.C_MAJOR_TONIC):
  """Composes a piece using the model, stores statistics about it in a dict.

  Args:
    rl_tuner: An RLTuner object.
    stat_dict: A dictionary storing statistics about a series of compositions.
    composition_length: The number of beats in the composition.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
    tonic_note: The tonic/1st note of the desired key.
    sample_next_obs: If True, each note will be sampled from the model's
      output distribution. If False, each note will be the one with maximum
      value according to the model.
  Returns:
    A dictionary updated to include statistics about the composition just
    created.
  """
  rl_tuner.num_notes_in_melody = len(piece)
  for note in piece :
    new_observation = np.zeros(rl_tuner_ops.NUM_CLASSES)
    new_observation[note]=1
    obs_note = np.argmax(new_observation)
    stat_dict = add_all_stats(rl_tuner,new_observation,obs_note,stat_dict,key,tonic_note)
    rl_tuner.composition.append(np.argmax(new_observation))
    rl_tuner.beat += 1

  for lag in [1, 2, 3]:
    stat_dict['autocorrelation' + str(lag)].append(
        rl_tuner_ops.autocorrelate(rl_tuner.composition, lag))

  add_high_low_unique_stats(rl_tuner, stat_dict)

  return stat_dict


def add_all_stats(rl_tuner,new_observation,obs_note,stat_dict,key,tonic_note):
  # Compute note by note stats as it composes.
  stat_dict = add_interval_stat(rl_tuner, new_observation, stat_dict, key=key)
  stat_dict = add_in_key_stat(obs_note, stat_dict, key=key)
  stat_dict = add_tonic_start_stat(
      rl_tuner, obs_note, stat_dict, tonic_note=tonic_note)
  stat_dict = add_repeating_note_stat(rl_tuner, obs_note, stat_dict)
  stat_dict = add_motif_stat(rl_tuner, new_observation, stat_dict)
  stat_dict = add_repeated_motif_stat(rl_tuner, new_observation, stat_dict)
  stat_dict = add_leap_stats(rl_tuner, new_observation, stat_dict)
  #NEW
  stat_dict = add_intra_section_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_larger_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_whole_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_half_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_quarter_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_octave_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_sixteenth_note_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_early_pause_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_late_bar_stats(rl_tuner,obs_note,stat_dict)
  stat_dict = add_melody_stats(rl_tuner,obs_note,tonic_note,stat_dict)
  stat_dict = add_galician_leap_stats(rl_tuner, obs_note, key, stat_dict)
  stat_dict = add_last_quarter_note_stat(rl_tuner,obs_note,stat_dict)
  return stat_dict
#END OF NEW


def initialize_stat_dict():
  """Initializes a dictionary which will hold statistics about compositions.

  Returns:
    A dictionary containing the appropriate fields initialized to 0 or an
    empty list.
  """
  stat_dict = dict()

  for lag in [1, 2, 3]:
    stat_dict['autocorrelation' + str(lag)] = []

  stat_dict['notes_not_in_key'] = 0
  stat_dict['notes_in_motif'] = 0
  stat_dict['notes_in_repeated_motif'] = 0
  stat_dict['num_starting_tonic'] = 0
  stat_dict['num_repeated_notes'] = 0
  stat_dict['num_octave_jumps'] = 0
  stat_dict['num_fifths'] = 0
  stat_dict['num_thirds'] = 0
  stat_dict['num_sixths'] = 0
  stat_dict['num_seconds'] = 0
  stat_dict['num_fourths'] = 0
  stat_dict['num_sevenths'] = 0
  #NEW
  stat_dict['num_in_key_fifths'] = 0
  stat_dict['num_in_key_thirds'] = 0
  stat_dict['num_minor_seconds'] = 0
  stat_dict['num_minor_thirds'] = 0
  stat_dict['num_diminished_fifths'] = 0
  stat_dict['num_minor_sixths'] = 0
  stat_dict['num_minor_sevenths'] = 0
  stat_dict['num_same_note_intervals'] = 0
  #END OF NEW
  stat_dict['num_rest_intervals'] = 0
  stat_dict['num_special_rest_intervals'] = 0
  stat_dict['num_in_key_preferred_intervals'] = 0
  stat_dict['num_resolved_leaps'] = 0
  stat_dict['num_leap_twice'] = 0
  stat_dict['num_high_unique'] = 0
  stat_dict['num_low_unique'] = 0
  #NEW
  stat_dict['num_correlated_intervals'] = 0
  stat_dict['num_larger_notes'] = 0
  stat_dict['num_whole_notes'] = 0
  stat_dict['num_half_notes'] = 0
  stat_dict['num_quarter_notes'] = 0
  stat_dict['num_octave_notes'] = 0
  stat_dict['num_sixteenth_notes'] = 0
  stat_dict['num_early_pauses'] = 0
  stat_dict['num_late_quarter_notes'] = 0
  stat_dict['num_late_pauses'] = 0
  stat_dict['num_late_note_off_events'] = 0
  stat_dict['num_late_tonics'] = 0
  stat_dict['num_sub_tonics'] = 0
  stat_dict['num_non_sub_tonics'] = 0
  stat_dict['num_opposite_seconds'] = 0
  stat_dict['num_direction_changes'] = 0
  stat_dict['num_last_quarter_notes'] = 0
  stat_dict['non_sub_tonics'] = 0
  #END OF NEW

  return stat_dict


def add_interval_stat(rl_tuner, action, stat_dict, key=None):
  """Computes the melodic interval just played and adds it to a stat dict.

  Args:
    rl_tuner: An RLTuner object.
    action: One-hot encoding of the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
  Returns:
    A dictionary of composition statistics with fields updated to include new
    intervals.
  """
  interval, _, _ = rl_tuner.detect_sequential_interval(action, key)

  if interval == 0:
    return stat_dict

  if interval == rl_tuner_ops.REST_INTERVAL:
    stat_dict['num_rest_intervals'] += 1
  elif interval == rl_tuner_ops.REST_INTERVAL_AFTER_THIRD_OR_FIFTH:
    stat_dict['num_special_rest_intervals'] += 1
  elif interval > rl_tuner_ops.OCTAVE:
    stat_dict['num_octave_jumps'] += 1
  #elif (interval == rl_tuner_ops.IN_KEY_FIFTH) or (interval == rl_tuner_ops.IN_KEY_THIRD):
  #  stat_dict['num_in_key_preferred_intervals'] += 1
  #NEW
  elif interval == rl_tuner_ops.IN_KEY_FIFTH:
    stat_dict['num_in_key_fifths'] += 1
  elif interval == rl_tuner_ops.IN_KEY_THIRD:
    stat_dict['num_in_key_thirds'] += 1
  #END OF NEW
  elif interval == rl_tuner_ops.FIFTH:
    stat_dict['num_fifths'] += 1
  elif interval == rl_tuner_ops.THIRD:
    stat_dict['num_thirds'] += 1
  elif interval == rl_tuner_ops.SIXTH:
    stat_dict['num_sixths'] += 1
  elif interval == rl_tuner_ops.SECOND:
    stat_dict['num_seconds'] += 1
  elif interval == rl_tuner_ops.FOURTH:
    stat_dict['num_fourths'] += 1
  elif interval == rl_tuner_ops.SEVENTH:
    stat_dict['num_sevenths'] += 1
  #NEW
  elif interval == rl_tuner_ops.MINOR_SECOND:
    stat_dict['num_minor_seconds'] += 1
  elif interval == rl_tuner_ops.MINOR_THIRD:
    stat_dict['num_minor_thirds'] += 1
  elif interval == rl_tuner_ops.DIMINISHED_FIFTH:
    stat_dict['num_diminished_fifths'] += 1
  elif interval == rl_tuner_ops.MINOR_SIXTH:
    stat_dict['num_minor_sixths'] += 1
  elif interval == rl_tuner_ops.MINOR_SEVENTH:
    stat_dict['num_minor_sevenths'] += 1
  elif interval == 0:
    stat_dict['num_same_note_intervals'] += 1
  #END OF NEW

  return stat_dict


def add_in_key_stat(action_note, stat_dict, key=None):
  """Determines whether the note played was in key, and updates a stat dict.

  Args:
    action_note: An integer representing the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
    key: The numeric values of notes belonging to this key. Defaults to
      C-major if not provided.
  Returns:
    A dictionary of composition statistics with 'notes_not_in_key' field
    updated.
  """
  if key is None:
    key = rl_tuner_ops.C_MAJOR_KEY

  if action_note not in key:
    stat_dict['notes_not_in_key'] += 1

  return stat_dict


def add_tonic_start_stat(rl_tuner,
                         action_note,
                         stat_dict,
                         tonic_note=rl_tuner_ops.C_MAJOR_TONIC):
  """Updates stat dict based on whether composition started with the tonic.

  Args:
    rl_tuner: An RLTuner object.
    action_note: An integer representing the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
    tonic_note: The tonic/1st note of the desired key.
  Returns:
    A dictionary of composition statistics with 'num_starting_tonic' field
    updated.
  """
  if rl_tuner.beat == 0 and action_note in tonic_note:
    stat_dict['num_starting_tonic'] += 1
  return stat_dict


def add_repeating_note_stat(rl_tuner, action_note, stat_dict):
  """Updates stat dict if an excessively repeated note was played.

  Args:
    rl_tuner: An RLTuner object.
    action_note: An integer representing the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
  Returns:
    A dictionary of composition statistics with 'num_repeated_notes' field
    updated.
  """
  if rl_tuner.detect_repeating_notes(action_note):
    stat_dict['num_repeated_notes'] += 1
  return stat_dict


def add_motif_stat(rl_tuner, action, stat_dict):
  """Updates stat dict if a motif was just played.

  Args:
    rl_tuner: An RLTuner object.
    action: One-hot encoding of the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
  Returns:
    A dictionary of composition statistics with 'notes_in_motif' field
    updated.
  """
  composition = rl_tuner.composition + [np.argmax(action)]
  motif, _ = rl_tuner.detect_last_motif(composition=composition)
  if motif is not None:
    stat_dict['notes_in_motif'] += 1
  return stat_dict


def add_repeated_motif_stat(rl_tuner, action, stat_dict):
  """Updates stat dict if a repeated motif was just played.

  Args:
    rl_tuner: An RLTuner object.
    action: One-hot encoding of the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
  Returns:
    A dictionary of composition statistics with 'notes_in_repeated_motif'
    field updated.
  """
  is_repeated, _ = rl_tuner.detect_repeated_motif(action)
  if is_repeated:
    stat_dict['notes_in_repeated_motif'] += 1
  return stat_dict


def add_leap_stats(rl_tuner, action, stat_dict):
  """Updates stat dict if a melodic leap was just made or resolved.

  Args:
    rl_tuner: An RLTuner object.
    action: One-hot encoding of the chosen action.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
  Returns:
    A dictionary of composition statistics with leap-related fields updated.
  """
  leap_outcome = rl_tuner.detect_leap_up_back(action)
  if leap_outcome == rl_tuner_ops.LEAP_RESOLVED:
    stat_dict['num_resolved_leaps'] += 1
  elif leap_outcome == rl_tuner_ops.LEAP_DOUBLED:
    stat_dict['num_leap_twice'] += 1
  return stat_dict


def add_high_low_unique_stats(rl_tuner, stat_dict):
  """Updates stat dict if rl_tuner.composition has unique extrema notes.

  Args:
    rl_tuner: An RLTuner object.
    stat_dict: A dictionary containing fields for statistics about
      compositions.
  Returns:
    A dictionary of composition statistics with 'notes_in_repeated_motif'
    field updated.
  """
  if rl_tuner.detect_high_unique(rl_tuner.composition):
    stat_dict['num_high_unique'] += 1
  if rl_tuner.detect_low_unique(rl_tuner.composition):
    stat_dict['num_low_unique'] += 1

  return stat_dict

#NEW
def add_intra_section_stats(rl_tuner,action_note,stat_dict):
  if rl_tuner.reward_intra_section_similarity(action_note):
    stat_dict['num_correlated_intervals']+=1
  return stat_dict

def add_larger_note_stats(rl_tuner,action_note,stat_dict):
  composition = rl_tuner.composition
  if(len(composition)>=16):
    if(composition[-16]!=NO_EVENT and all(note==NO_EVENT for note in composition[-15:]) and action_note==NO_EVENT):
      stat_dict['num_larger_notes']+=1
  return stat_dict

def add_whole_note_stats(rl_tuner,action_note,stat_dict):
  composition = rl_tuner.composition
  if(len(composition)>=16):
    if(composition[-16]!=NO_EVENT and all(note==NO_EVENT for note in composition[-15:]) and action_note!=NO_EVENT) or \
     (composition[-15]!=NO_EVENT and all(note==NO_EVENT for note in  composition[-14:]) and action_note==NO_EVENT and len(composition)==rl_tuner.num_notes_in_melody-1):
      stat_dict['num_whole_notes']+=1
  return stat_dict

def add_half_note_stats(rl_tuner,action_note,stat_dict):
  composition = rl_tuner.composition
  if(len(composition)>=8):
    if(composition[-8]!=NO_EVENT and all(note==NO_EVENT for note in  composition[-7:]) and action_note!=NO_EVENT) or \
     (composition[-7]!=NO_EVENT and all(note==NO_EVENT for note in  composition[-6:]) and action_note==NO_EVENT and len(composition)==rl_tuner.num_notes_in_melody-1):
      stat_dict['num_half_notes']+=1
  return stat_dict


def add_quarter_note_stats(rl_tuner,action_note,stat_dict):
  if rl_tuner.detect_quarter_note(action_note):  
    stat_dict['num_quarter_notes']+=1
  return stat_dict

def add_octave_note_stats(rl_tuner,action_note,stat_dict):
  if rl_tuner.detect_eighth_note(action_note):
    stat_dict['num_octave_notes']+=1
  return stat_dict

def add_sixteenth_note_stats(rl_tuner,action_note,stat_dict):
  if rl_tuner.detect_sixteenth_note(action_note):
    stat_dict['num_sixteenth_notes']+=1
  return stat_dict

def add_early_pause_stats(rl_tuner,action_note,stat_dict):
  composition = rl_tuner.composition
  if (len(composition)==4 and (all(note == NO_EVENT for note in composition) and action_note!=NO_EVENT)):
    stat_dict['num_early_pauses']+=1
  return stat_dict

def add_late_bar_stats(rl_tuner,action_note,stat_dict):
  composition = rl_tuner.composition
  if len(composition)==BAR_LENGTH*SECTION_N_BARS-BAR_LENGTH+4 and composition[-4]!= NO_EVENT and all(note==NO_EVENT for note in composition[-3:]) and action_note!=NO_EVENT:
    stat_dict['num_late_quarter_notes'] += 1
  #Ending with two quarter note pauses
  if len(composition)==BAR_LENGTH*SECTION_N_BARS-BAR_LENGTH+8 and composition[-4]== NOTE_OFF and all(note==NO_EVENT for note in composition[-3:]) and action_note!=NO_EVENT:
    stat_dict['num_late_pauses'] +=1
  if len(composition)==BAR_LENGTH*SECTION_N_BARS and composition[-4]== NOTE_OFF and all(note==NO_EVENT for note in composition[-3:]):
    stat_dict['num_late_pauses'] +=1
  if len(composition)==BAR_LENGTH*SECTION_N_BARS and composition[-8]== NOTE_OFF and all(note==NO_EVENT for note in composition[-7:]):
    stat_dict['num_late_pauses'] +=2
  if len(composition)>=BAR_LENGTH*SECTION_N_BARS-BAR_LENGTH+4 and action_note==NOTE_OFF:
    stat_dict['num_late_note_off_events'] +=1
  return stat_dict

def add_melody_stats(rl_tuner,action_note, tonic, stat_dict):
  if rl_tuner.detect_late_tonic(action_note,tonic):
    stat_dict['num_late_tonics']+=1
  if rl_tuner.detect_sub_tonic(action_note,tonic):
    stat_dict['num_sub_tonics']+=1
  if rl_tuner.detect_non_sub_tonic(action_note,tonic):
    stat_dict['num_non_sub_tonics']+=1
  return stat_dict

def add_galician_leap_stats(rl_tuner,action_note,key,stat_dict):
  if rl_tuner.reward_opposite_second(action_note,key):
    stat_dict['num_opposite_seconds']+=1

  if rl_tuner.reward_direction_change(action_note):
    stat_dict['num_direction_changes']+=1
  return stat_dict

def add_last_quarter_note_stat(rl_tuner,action_note,stat_dict):
  if rl_tuner.reward_last_quarter_note(action_note):
    stat_dict['num_last_quarter_notes']+=1
  return stat_dict
