OLD_CHECKPOINT_FILE = "./mag_checkpoint/pre-trained.ckpt"
NEW_CHECKPOINT_FILE = "./rl_tuner_checkpoint/pre-trained.ckpt"

import tensorflow as tf
vars_to_rename = {
    "RNN/MultiRNNCell/Cell1/BasicLSTMCell/Linear/Matrix": "rnn/multi_rnn_cell/cell_1/basic_lstm_cell/kernel",
    "RNN/MultiRNNCell/Cell1/BasicLSTMCell/Linear/Bias": "rnn/multi_rnn_cell/cell_1/basic_lstm_cell/bias",
    "RNN/MultiRNNCell/Cell0/BasicLSTMCell/Linear/Matrix":"rnn/multi_rnn_cell/cell_0/basic_lstm_cell/kernel",
    "RNN/MultiRNNCell/Cell0/BasicLSTMCell/Linear/Bias":"rnn/multi_rnn_cell/cell_0/basic_lstm_cell/bias"
}
new_checkpoint_vars = {}
reader = tf.train.NewCheckpointReader(OLD_CHECKPOINT_FILE)
for old_name in reader.get_variable_to_shape_map():
  print("old name")
  if old_name in vars_to_rename:
    new_name = vars_to_rename[old_name]
  else:
    new_name = old_name
  new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))

init = tf.global_variables_initializer()
saver = tf.train.Saver(new_checkpoint_vars)

with tf.Session() as sess:
  sess.run(init)
  saver.save(sess, NEW_CHECKPOINT_FILE)
  saver = tf.train.import_meta_graph(NEW_CHECKPOINT_FILE+".meta")