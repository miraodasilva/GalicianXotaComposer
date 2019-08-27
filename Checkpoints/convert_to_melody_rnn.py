OLD_CHECKPOINT_FILE = "./saved_from_rl_tuner/rl_tuner_save.ckpt"
NEW_CHECKPOINT_FILE = "./melody_rnn_checkpoint/pre-trained.ckpt"

import tensorflow as tf

new_checkpoint_vars = {}
reader = tf.train.NewCheckpointReader(OLD_CHECKPOINT_FILE)
for old_name in reader.get_variable_to_shape_map():
  new_name = old_name
  new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))


new_checkpoint_vars["beta1_power"] = tf.Variable(tf.random_normal([]))
new_checkpoint_vars["beta2_power"] = tf.Variable(tf.random_normal([]))
new_checkpoint_vars["global_step"] = tf.Variable(tf.zeros([],tf.int64))
"""
new_checkpoint_vars["fully_connected/biases/Adam"] = tf.Variable(tf.random_normal([38]))
new_checkpoint_vars["fully_connected/biases/Adam_1"] = tf.Variable(tf.random_normal([38]))
new_checkpoint_vars["fully_connected/weights/Adam"] = tf.Variable(tf.random_normal([512,38]))
new_checkpoint_vars["fully_connected/weights/Adam_1"] = tf.Variable(tf.random_normal([512,38]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_0/basic_lstm_cell/bias/Adam"] = tf.Variable(tf.random_normal([2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_0/basic_lstm_cell/bias/Adam_1"] = tf.Variable(tf.random_normal([2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_0/basic_lstm_cell/kernel/Adam"] = tf.Variable(tf.random_normal([550,2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_0/basic_lstm_cell/kernel/Adam_1"] = tf.Variable(tf.random_normal([550,2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_1/basic_lstm_cell/bias/Adam"] = tf.Variable(tf.random_normal([2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_1/basic_lstm_cell/bias/Adam_1"] = tf.Variable(tf.random_normal([2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_1/basic_lstm_cell/kernel/Adam"] = tf.Variable(tf.random_normal([1024,2048]))
new_checkpoint_vars["rnn/multi_rnn_cell/cell_1/basic_lstm_cell/kernel/Adam_1"] = tf.Variable(tf.random_normal([1024,2048]))
"""

init = tf.global_variables_initializer()

saver = tf.train.Saver(new_checkpoint_vars)


with tf.Session() as sess:
  sess.run(init)
  saver.save(sess, NEW_CHECKPOINT_FILE)
  saver = tf.train.import_meta_graph(NEW_CHECKPOINT_FILE + '.meta')
