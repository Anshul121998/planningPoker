"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restplus import Resource
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .security import require_auth
from . import api_rest


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/secure-getTest/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def get(self, resource_id):
        Brain1 = AIBrain()
        return Brain1.globalTest

@api_rest.route('/secure-declareAIbrain/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        Brain1.declaration(int(request.json['inputLayer']), list(request.json['hiddenLayer']), list(request.json['output']))
        return "Model created, ready to run!"

@api_rest.route('/secure-createWB/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        Brain1.generateWB(int(request.json['curr_gen']))
        return "Weights and biases created"

@api_rest.route('/secure-testModel/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        return Brain1.test(list(request.json['inputs']))

@api_rest.route('/secure-trainModel/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        Brain1.train(best_output_index=request.json['index'], curr_gen=request.json['curr_gen'], curr_run=request.json['curr_run'], suggested_output=request.json['suggested_output'], inputs=request.json['inputs'], score=request.json['score'])
        return "not too dumb now, am I"

@api_rest.route('/secure-getValues/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def get(self, resource_id):
        return Brain1.commit_csv()


# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
class AIBrain:
    def __init__(self):
        self.globalTest = "testhello"

    def declaration(self, numberOfInputs, hiddenLayer, outputLayer, MutationRate=5, LearningRate=0.1):
        self.LearningRate = LearningRate
        self.numberOfInputs = numberOfInputs
        self.hiddenLayer = hiddenLayer
        self.outputLayer = outputLayer
        self.MutationRate = MutationRate

    # GENERATE WEIGHTS AND BIASES
    # --------------------------------------------------------------------------------------------------------------

    def geneticWB(self):
        w1 = np.array(self.dataFrame.weights[0])[0]
        b1 = np.array(self.dataFrame.biases[0])[0]
        w2 = np.array(self.dataFrame.weights[0])[1]
        b2 = np.array(self.dataFrame.biases[0])[1]
        for i in range(0, len(w1)):
            for j in range(0, len(w1[i])):
                for k in range(0, len(w1[i][j])):
                    n = random.random()
                    if n < 0.05:
                        w1[i][j][k] = random.random()
                    else:
                        m = random.random()
                        if m < 0.5:
                            w1[i][j][k] = w2[i][j][k]

        # print("Updated W1 -", w1,"\n__________________\n")

        # print("B1 -", b1,"\n__________________\n")

        for i in range(0, len(b1)):
            for j in range(0, len(b1[i])):
                n = random.random()
                if n < 0.05:
                    b1[i][j] = random.random()
                else:
                    m = random.random()
                    if m < 0.5:
                        b1[i][j] = b2[i][j]

        # print("Updated B1 -", b1,"\n__________________\n")
        self.weights = w1
        self.biases = b1

    def first_generateWB(self):
        # code for generating weights
        w = []
        l = []
        for i in range(0, self.hiddenLayer[0]):
            c = []
            for j in range(0, self.numberOfInputs):
                c.append(random.random())
            l.append(c)
        w.append(np.matrix(l))
        for i in range(0, len(self.hiddenLayer) - 1):
            l = []
            for j in range(0, self.hiddenLayer[i + 1]):
                c = []
                for k in range(0, self.hiddenLayer[i]):
                    c.append(random.random())
                # c = np.matrix(c)
                l.append(c)
            w.append(np.matrix(l))
        l = []
        for i in range(0, len(self.outputLayer)):
            c = []
            for j in range(0, self.hiddenLayer[-1]):
                c.append(random.random())
            l.append(c)
        w.append(np.matrix(l))
        # print("Weights -", w,"\n__________________\n")
        # code for generating biases
        b = []
        for i in range(0, len(self.hiddenLayer)):
            l = []
            for j in range(0, self.hiddenLayer[i]):
                l.append(random.random() - 0.5)
            b.append(np.matrix(l).T)

        l = []
        for j in range(0, len(self.outputLayer)):
            l.append(random.random() - 0.5)
        b.append(np.matrix(l).T)

        # print("Biases -", b,"\n__________________\n")
        self.weights = w
        self.biases = b

    def generateWB(self, curr_gen):
        if curr_gen == 0:
            return AIBrain.first_generateWB(self)
        else:
            return AIBrain.geneticWB(self)

    # TEST FUNCTION
    # --------------------------------------------------------------------------------------------------------------

    def reLU(x):
        # print("X-men : ",x)
        for i in range(0, len(x)):
            if (x[i] < 0):
                x[i] = 0
        return x

    def reducedims(curr_layer, m):
        curr_layer = np.array(curr_layer)
        m = float(m)
        while (m > 1):
            m = m / 10
            curr_layer = curr_layer / 10
        return curr_layer

    def test(self, inputs):
        layers = []
        inputs = AIBrain.reducedims(inputs, max(inputs))
        inputs = np.matrix(inputs).T
        layers.append(inputs)

        mk = AIBrain.reLU((self.weights[0] * inputs) + self.biases[0]).T
        curr_lay = AIBrain.reducedims(mk.tolist()[0], max(mk.tolist()[0]))
        layers.append(np.matrix(curr_lay).T)

        for i in range(0, len(self.hiddenLayer) - 1):
            mk = AIBrain.reLU((self.weights[i + 1] * layers[i + 1]) + self.biases[i + 1]).T
            curr_lay = AIBrain.reducedims(mk.tolist()[0], max(mk.tolist()[0]))
            layers.append(np.matrix(curr_lay).T)

        mk = AIBrain.reLU((self.weights[-1] * layers[-1]) + self.biases[-1]).T
        curr_lay = AIBrain.reducedims(mk.tolist()[0], max(mk.tolist()[0]))
        layers.append(np.matrix(curr_lay).T)

        ans = np.where(layers[-1] == max(layers[-1]))
        # print("Layers -", layers,"\n__________________\n")
        # print("Suggested Output -", self.outputLayer[ans[0][0]],"\n__________________\n")
        # print("Suggested Output Index -", ans[0][0],"\n__________________\n")
        self.layers = layers
        return self.outputLayer[ans[0][0]]

    # SAVE FUNCTION
    # --------------------------------------------------------------------------------------------------------------

    def save_final_WB(self, curr_gen, curr_run, inputs, suggested_output, fitness_output, score):
        if (curr_gen == 0 and curr_run == 0):
            self.dataFrame = pd.DataFrame(
                {"curr_gen": curr_gen, "curr_run": curr_run, "inputs": [inputs], "weights": [self.weights],
                 "biases": [self.biases], "layer": [self.layers], "suggested_output": suggested_output,
                 "fitness_output": fitness_output, "score": score})
        else:
            m = pd.DataFrame({"curr_gen": curr_gen, "curr_run": curr_run, "inputs": [inputs], "weights": [self.weights],
                              "biases": [self.biases], "layer": [self.layers], "suggested_output": suggested_output,
                              "fitness_output": fitness_output, "score": score})
            self.dataFrame = pd.concat([self.dataFrame, m])
            self.dataFrame = self.dataFrame.sort_values(by=['score', 'curr_gen', 'curr_run'], ascending=False)

    def commit_csv(self):
        # self.dataFrame.to_csv(name, encoding='utf-8', index=False)
        # self.dataFrame.sort_values(by=['curr_gen', 'curr_run'], inplace=True)
        return self.dataFrame.to_json(orient='records')

    def create_figure(self):
        self.dataFrame.sort_values(by=['curr_gen', 'curr_run'], inplace=True)
        x = []
        y = []
        for i in range(0, len(self.dataFrame)):
            x.append(int(str(np.array(self.dataFrame.curr_gen)[i]) + str(np.array(self.dataFrame.curr_run)[i])))
            y.append(int(np.array(self.dataFrame.score)[i]))
        fig = plt.figure()
        plt.plot(x, y, marker='*')
        fig.suptitle('Score against each gen + run')
        plt.xlabel('gen + run')
        plt.ylabel('score')
        return fig
    # TRAIN FUNCTION
    # --------------------------------------------------------------------------------------------------------------

    def backprop_till_root(y, y_e, w, b):
        del_y = y_e - y
        w_inv = np.linalg.pinv(w)
        h = w_inv * (del_y - b)
        return h

    def set_weights(i, h, a, he):
        del_h = he - h
        m = i + a
        m_inv = np.linalg.pinv(m)
        w = del_h * m_inv
        b = w * a
        return w, b, del_h

    def create_a(a, size):
        n = []
        m = []
        m.append(a)
        for i in range(0, size):
            n.append(m)
        return n

    def set_weights_last(i, h, a, he):
        del_h = he - h
        m = i + a
        m_inv = np.linalg.pinv(m)
        w = del_h * m_inv
        b = w * a
        return w, b

    def train(self, best_output_index, curr_gen, curr_run, inputs, suggested_output, score):
        new_w = []
        new_b = []
        ye = []
        for i in range(0, len(self.layers[-1])):
            if (best_output_index == i):
                ye.append([1])
            else:
                ye.append([0])
        ye = np.matrix(ye)
        temp_ye = ye[:]
        ie = self.layers[0]
        for i in range(0, len(self.layers) - 1):
            ye = temp_ye[:]
            for j in range(len(self.layers) - 1, i + 1, -1):
                ye = AIBrain.backprop_till_root(self.layers[j], ye, self.weights[j - 1], self.biases[j - 1])
            a = np.matrix(AIBrain.create_a(self.LearningRate, len(self.layers[i])))
            if (i == len(self.layers) - 2):
                w_temp, b_temp = AIBrain.set_weights_last(ie, self.layers[-1], a, temp_ye)
                new_w.append(w_temp + self.weights[i])
                new_b.append(b_temp + self.biases[i])
            else:
                w_temp, b_temp, ie = AIBrain.set_weights(ie, self.layers[i + 1], a, ye)
                new_w.append(w_temp + self.weights[i])
                new_b.append(b_temp + self.biases[i])
        # print("new_w w -", new_w,"\n__________________\n")
        # print("new_b b -", new_b,"\n__________________\n")
        self.save_final_WB(curr_gen, curr_run, inputs, suggested_output, self.outputLayer[best_output_index], score)
        self.weights = new_w
        self.biases = new_b
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
Brain1 = AIBrain()
