from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.optimizers import sgd, adam, rmsprop, adagrad, adadelta
from keras.regularizers import l2, l1, l1_l2

from sklearn.preprocessing import StandardScaler

import numpy as np

class FeedForwardModel(object):
    def __init__(self, in_size, out_sizes, drop_out = None, normalize = False, verbose = False):
        self.verbose = verbose
        self.normalize = normalize
        self.scaler = StandardScaler()
        model = Sequential()
        model.add(Dense(units=out_sizes[0], input_dim=in_size, activation=('tanh' if len(out_sizes) > 1 else 'linear')))
        if len(out_sizes) > 1 and drop_out != None:
            model.add(Dropout(drop_out))
        for i in range(1, len(out_sizes)):
            model.add(Dense(units=out_sizes[i], activation=('tanh' if i < len(out_sizes) - 1 else 'linear')))

        print(model.summary())
        print(model.get_config())
        # model.compile(sgd(lr=10e-4), "mse")
        # model.compile(adam(lr=10e-4), "mse")
        model.compile(adagrad(), "mse")
        self._model = model

    def fit_features(self, observations):
        if observations.ndim == 1:
            observations = observations.reshape((observations.shape[0], 1))

        if self.normalize:
            self.scaler.fit(observations)

    def predict(self, s):
        if self.verbose:
            print("predict X: %s" % s)
        s = np.atleast_2d([s])
        if self.normalize:
            s = self.scaler.transform(s)

        res = np.squeeze(self._model.predict(s))
        if self.verbose:
            print("predict Y: %s" % res)
        return res

    def update(self, s, a, y):
        s = np.atleast_2d([s])
        y = np.atleast_2d([y])
        if self.normalize:
            s = self.scaler.transform(s)

        if self.verbose:
            print("update s; y: %s; %s" % (s, y))

        loss = self._model.train_on_batch(s, y)
        if self.verbose:
            print("Loss: %f" % loss)
        # for layer in self._model.layers:
        #     weights = np.array(layer.get_weights())
        #     print(weights[0].mean())
        #     print(weights[1].mean())
        #     print()