#!/usr/bin/env python3

import sys
import math
import random
import math
import matplotlib.pyplot as plt

def makeevalerr(inp1, inp2):
	if(len(inp1) != len(inp2)):
		print('different size of training files')
		sys.exit(0)
	else:
		def evalerr(fun):
			t = 0
			for i in range(len(inp1)):
				v = fun(inp1[i])
				t = t + ((v - inp2[i]) * (v - inp2[i]))
			return math.sqrt(t/len(inp1))
		return evalerr

# Fixed number of input and output neurons: 1-n-1
class Particle:
	def __init__(self,fun,nhid=4):
		# In hidden layer: 2 weights for each neuron, one for bias and one for input layer connection
		# In output layer: nhid weights plus one for bias
		self.nhidden = nhid
		self.position = [ [ (random.random(), random.random()) for i in range(self.nhidden) ], [ random.random() for j in range(self.nhidden + 1) ] ]
		self.evaluation = self.makeffn(self.nhidden)
		self.posbest = self.position
		self.fitness = fun(self.evaluation)

	def evaluate(self,fun):
		aux = fun(self.evaluation)
		if(aux < self.fitness):
			self.fitness = aux
			self.posbest = self.position

	def update(self,gbest):
		if(random.random() < 0.5):
			self.position[0] = [ (random.gauss( (gbest[0][j][0] + self.posbest[0][j][0])/2, abs(gbest[0][j][0] - self.posbest[0][j][0]) ), random.gauss( (gbest[0][j][1] + self.posbest[0][j][1])/2, abs(gbest[0][j][1] - self.posbest[0][j][1]) ) ) for j in range(self.nhidden) ]
			self.position[1] = [ random.gauss( (gbest[1][j] + self.posbest[1][j])/2, abs(gbest[1][j] - self.posbest[1][j]) ) for j in range(self.nhidden+1) ]
			self.evaluation = self.makeffn(self.nhidden)
		else:
			self.position = self.posbest

	def makeffn(self,nhid):
		# create a feedforward network
		# receives the input value and calculates the output
		def ffn(ivalue):
			total = 0
			for i in range(nhid):
				# neuron's activation
				hneuron = math.tanh((-1 * self.position[0][i][0]) + (ivalue * self.position[0][i][1]))
				# add the weight to output neuron
				total = total + (hneuron * self.position[1][i])
			return (total - self.position[1][nhid])
		return ffn

# it: number of iterations
# npop: number of particles
# nhid: number of neurons on hidden layer
def bbpso(it,npop,nhid,fun):
	# print('PSO:\n\tpopulation size =',npop)
	# print('\tnumber of iterations =',it)
	pop = []
	for i in range(npop):
		pop.append(Particle(fun,nhid))

	bind = pop[0]
	convergence = [[],[]]

	for i in range(it):
		for j in pop:
			if(j.fitness < bind.fitness):
				bind = j
		convergence[0].append(i)
		convergence[1].append(bind.fitness)
		for j in pop:
			j.update(bind.posbest)
			j.evaluate(fun)
	return (bind,convergence)

def main(filename1,filename2,filename3,nhid,plotall=True):
	with open(filename1) as fil:
		inp1 = list(map(float,fil.read().split()))
	with open(filename2) as fil:
		inp2 = list(map(float,fil.read().split()))
	with open(filename3) as fil:
		inp3 = list(map(float,fil.read().split()))

	gbind = None
	gconvergence = None

	# print( bbpso(10*nhid*len(inp1[0]),3*nhid*len(inp1[0]),nhid,makeevalerr(inp1,inp2)) )
	if(plotall):
		plt.figure()
	for i in range(20):
		(bind,convergence) = bbpso(160,40,nhid,makeevalerr(inp1,inp2))
		if((gbind is None) or (bind.fitness < gbind.fitness)):
			gbind = bind
			gconvergence = convergence
		print( bind.fitness )
		# plt.plot(inp1+inp3,list(map(bind.evaluation,inp1+inp3)),marker='.',markersize=4)
		if(plotall):
			plt.scatter(inp1+inp3,list(map(bind.evaluation,inp1+inp3)),s=1)
	# if(plotall):
		# plt.show()
	plt.figure()
	# plt.scatter(inp1+inp3,list(map(gbind.evaluation,inp1+inp3)),s=1)
	plt.scatter(inp3,list(map(gbind.evaluation,inp3)),s=1)
	# plt.show()

	plt.figure()
	plt.plot(gconvergence[0],gconvergence[1])
	plt.show()

	print(bind.position)


if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./annbbpso x_training y_training x_test hidden_neurons')
		main('x_treinamento.txt','y_treinamento.txt','x_teste.txt',10,False)
	else:
		main(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]))


# import numpy as np
# import random
#
# class FFANN:
# 	class Particle:
# 		def __init__(self,nhid,nout):
# 			self.whidden = [ (random.random(), random.random()) for i in range(nhid) ]
# 			self.woutput = [ (random.random(), random.random()) for i in range(nout) ]
# 			self.fitness = -1
# 	def __init__(self, npop=100, nhid=4):
# 		self.population = [ Particle(nhid,1) for i in range(npop) ]
#
# 	def feedforward(self,input):
# 		;
#
# 	def fitness(self,inp,out):
# 		s = 0
# 		for i in range(len(inp)):
# 			s = s + (out - inp)



# class FeedForwardNetwork:
# 	def __init__(self, nIn, nHidden, nOut):
# 		# learning rate
# 		self.alpha = 0.1
#
# 		# number of neurons in each layer
# 		self.nIn = nIn
# 		self.nHidden = nHidden
# 		self.nOut = nOut
#
# 		# initialize weights randomly (+1 for bias)
# 		self.hWeights = [ [ random.random() for x in range(self.nIn+1) ] for y in range(self.nHidden) ]
# 		self.oWeights = [ [ random.random() for x in range(self.nHidden+1) ] for y in range(self.nOut) ]
#
# 		# activations of neurons (sum of inputs)
# 		self.hActivation = [ [0] * self.nHidden ]
# 		self.oActivation = [ [0] * self.nOut ]
#
# 		# outputs of neurons (after sigmoid function)
# 		self.iOutput = [ [0] * (self.nIn+1) ]      # +1 for bias
# 		self.hOutput = [ [0] * (self.nHidden+1) ]  # +1 for bias
# 		self.oOutput = [ [0] * (self.nOut) ]
#
# 		# deltas for hidden and output layer
# 		self.hDelta = [ [0] * self.nHidden ]
# 		self.oDelta = [ [0] * self.nOut ]
#
# 	def forward(self, input):
# 		# set input as output of first layer (bias neuron = 1.0)
# 		self.iOutput[:-1, 0] = input
# 		self.iOutput[-1:, 0] = 1.0
#
# 		# hidden layer
# 		self.hActivation = dot(self.hWeights, self.iOutput)
# 		self.hOutput[:-1, :] = tanh(self.hActivation)
#
# 		# set bias neuron in hidden layer to 1.0
# 		self.hOutput[-1:, :] = 1.0
#
# 		# output layer
# 		self.oActivation = dot(self.oWeights, self.hOutput)
# 		self.oOutput = tanh(self.oActivation)
#
# 	def evaluate(self, teach):
# 		sum = 0
# 		for i in range(self.n)
