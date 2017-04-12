from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import tensorflow as tf

TEXT_SIZE = 140
FEELINGS_SIZE = 10

vocabulary_size = 75000
embedding_size = 128

graph = tf.Graph()
with graph.as_default():
 inputs = tf.placeholder(tf.int32, shape=[1,134])
 state  = tf.placeholder(tf.float32, shape=[1,7,8])
 with tf.device('/cpu:0'):
  embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
  embed = tf.nn.embedding_lookup(embeddings, inputs)
  print(embed.get_shape())
  filter1 = tf.zeros([4,128,128])
  conv1 = tf.nn.conv1d(embed, filter1, 2, 'VALID')
  print(conv1.get_shape())
  conv2 = tf.nn.conv1d(conv1, filter1, 2, 'VALID')
  print(conv2.get_shape())
  dense = tf.layers.dense(conv2, 256, activation=None, use_bias =True,kernel_initializer=None,bias_initializer=tf.zeros_initializer(), kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, trainable=True, name=None, reuse=None)
  print(dense.get_shape())
  filter2 = tf.zeros([8,256,8])
  conv3 = tf.nn.conv1d(dense, filter2, 4, 'VALID')
  print(conv3.get_shape())
  consolidate = tf.concat([conv3,state],1)
  print(consolidate.get_shape())
  dense2 = tf.layers.dense(consolidate, 256, activation=None, use_bias =True,kernel_initializer=None,bias_initializer=tf.zeros_initializer(), kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, trainable=True, name=None, reuse=None)
  print(dense2.get_shape())
  re_dense2 = tf.expand_dims(dense2,1,name=None,dim =None)
  print(re_dense2.get_shape())
  filter3 = tf.zeros([1,4,128,256]) 
  tran1 = tf.nn.conv2d_transpose(value=re_dense2,filter=filter3,output_shape=[1,1,30,128],strides=[1,1,2,1],padding='VALID') 
  print(tran1.get_shape())
  filter3 = tf.zeros([1,4,128,128]) 
  tran2 = tf.nn.conv2d_transpose(value=tran1,filter=filter3,output_shape=[1,1,62,128],strides=[1,1,2,1],padding='VALID')
  print(tran2.get_shape())
  tran3 = tf.nn.conv2d_transpose(value=tran1,filter=filter3,output_shape=[1,1,126,128],strides=[1,1,2,1],padding='VALID')
  print(tran3.get_shape())
  batch_array = tf.squeeze(tran3)
  print(batch_array.get_shape())
  normed_embedding = tf.nn.l2_normalize(embeddings, dim=1)
  normed_array = tf.nn.l2_normalize(batch_array, dim=1)
  cosine_similarity = tf.matmul(normed_array, tf.transpose(normed_embedding, [1, 0]))
  closest_words = tf.argmax(cosine_similarity, 1) # shape [batch_size], type int64
  print(closest_words.get_shape())