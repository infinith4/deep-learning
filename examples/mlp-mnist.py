#!/usr/bin/python
# coding: utf-8

import theano
import theano.tensor as T
import numpy
from DL.models.MLP import MLP
from DL.optimizers.sgd import sgd
from DL.utils import *
import cPickle as pickle
import time

# hide warnings
import warnings
warnings.simplefilter("ignore")


print "An MLP on MNIST."
print "loading MNIST"
f = open('../datasets/mnist.pkl', 'rb')
mnist = pickle.load(f)
f.close()

print "loading data to the GPU"
dataset = load_data(mnist)

print "creating the MLP"
x = T.matrix('x')  # input
t = T.ivector('t')  # targets
inputs = [x, t]
rng = numpy.random.RandomState(int(time.time())) # random number generator

# construct the MLP class
mlp = MLP(
    rng=rng,
    input=x,
    n_in=28 * 28,
    n_hidden=500,
    n_out=10
)

# regularization
L1_reg=0.00
L2_reg=0.0001

# cost function
cost = (
    mlp.loss(t)
    + L1_reg * mlp.L1
    + L2_reg * mlp.L2_sqr
)

errors = mlp.errors(t)
params = flatten(mlp.params)

print "training the MLP with sgd"
sgd(dataset=dataset,
    inputs=inputs,
    cost=cost,
    params=params,
    errors=errors,
    learning_rate=0.01,
    momentum=0.2,
    n_epochs=1000,
    batch_size=20,
    patience=10000,
    patience_increase=2,
    improvement_threshold=0.995)

print "compiling the prediction function"
predict = theano.function(inputs=[x], outputs=mlp.pred)

print "predicting the first 10 samples of the test dataset"
print "predict:", predict(mnist[2][0][0:10])
print "answer: ", mnist[2][1][0:10]