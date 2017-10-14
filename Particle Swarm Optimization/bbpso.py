#!/usr/bin/env python3

import sys
import math
import random
import math

def euclidian(a,b):
	s = 0
	for i in range(len(a)):
		s = (a[i] - b[i]) * (a[i] - b[i]) + s
	return math.sqrt(s)

def make(inp):
	def cluster(a):
		t = 0
		for i in inp:
			s = euclidian(i,a[0])
			for j in a[1:]:
				aux = euclidian(i,j)
				if(aux < s):
					s = aux
			t = t + s
		return t
	return cluster

def f6(i):
	[x,y] = i
	aux = x*x + y*y
	a = math.sin(math.sqrt(aux))*math.sin(math.sqrt(aux)) - 0.5
	b = (1.0+0.01*aux)*(1.0+0.01*aux)
	return a/b

class Particle:
	def __init__(self,mn,mx,k=1,d=1,fun=euclidian):
		self.position = [ [ random.uniform(mn[i],mx[i]) for i in range(d) ] for j in range(k) ]
		self.posbest = self.position
		self.fit = fun(self.posbest)

	def evaluate(self,fun):
		aux = fun(self.position)
		if(aux < self.fit):
			self.fit = aux
			self.posbest = self.position

	def update(self,gbest):
		if(random.random() < 0.5):
			self.position = [ [ random.gauss((gbest[i][j]+self.posbest[i][j])/2, abs(gbest[i][j]-self.posbest[i][j])) for j in range(len(gbest[0]))] for i in range(len(gbest)) ]
		else:
			self.position = self.posbest

# it: number of iterations
# npop: number of particles
# mn: floor value of particles
# mx: ceil value of particles
# k: number of clusters
# d: number of dimensions
def bbpso(it,npop=15,mn=-50,mx=50,k=1,d=1,fun=euclidian):
	print('PSO:\n\tpopulation size =',npop)
	print('\tnumber of iterations =',it)
	pop = []
	for i in range(npop):
		pop.append(Particle(mn,mx,k,d,fun))

	bfit = pop[0].fit
	bpos = pop[0].posbest

	for i in range(it):
		for j in pop:
			if(j.fit < bfit):
				bpos = j.posbest
				bfit = j.fit
		# print('Best fit:',bfit,'at:',bpos)
		for j in pop:
			j.update(bpos)
			# j.update(pop[random.randrange(npop)].posbest)
			j.evaluate(fun)
	# return (bpos,bfit)
	return bfit

def main(filename,k):
	inp = []
	with open(filename) as fil:
		# lines = fil.readlines()
		for line in fil:
			inp.append([float(x) for x in line.split()])
	mn = inp[0]
	mx = inp[0]
	for it in inp:
		mn = [ it[j] if it[j] < mn[j] else mn[j] for j in range(len(inp[0])) ]
		mx = [ it[j] if it[j] > mn[j] else mn[j] for j in range(len(inp[0])) ]
	# print(mn,mx)
	print( bbpso(10*k*len(inp[0]),3*k*len(inp[0]),mn,mx,k,len(inp[0]),make(inp)) )


if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./bbpso datafile number_of_clusters')
	else:
		main(sys.argv[1],int(sys.argv[2]))
