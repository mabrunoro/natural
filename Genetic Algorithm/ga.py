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

class Population:
	class Individual:
		def __init__(self,mn=None,mx=None,k=None,d=None,fun=None,pos=None):
			if(pos is None):
				if(mn is None or mx is None or k is None or d is None):
					print('Error: one or more arguments not provided')
					sys.exit(0)
				self.position = [ [ random.uniform(mn[i],mx[i]) for i in range(d) ] for j in range(k) ]
				self.posbest = self.position
			else:
				self.position = pos
				self.posbest = self.position
			if(fun is not None):
				self.fitness = fun(self.position)
				self.fitbest = fun(self.posbest)
			else:
				print('Error: fitness function not provided')
				sys.exit(0)

		def evaluate(self,fun):
			self.fitness = fun(self.position)
			if(self.fitness < self.fitbest):
				self.fitbest = self.fitness
				self.posbest = self.position

	def fitness(self, obj1, obj2):
		if(obj1.fitbest < obj2.fitbest):
			return obj1
		else:
			return obj2

	def __init__(self,npop,mn,mx,k,d,fun):
		self.population = []
		self.size = npop
		self.minimum = mn
		self.maximum = mx
		for i in range(self.size):
			self.population.append(self.Individual(mn=self.minimum,mx=self.maximum,k=k,d=d,fun=fun))
		self.bind = self.population[0]	# best individual
		for i in range(self.size):
			# if(self.population[i].fitbest < self.bind.fitbest):	# defines if optimization is higher fitness or lower fitness
				# self.bind = self.population[i]
				self.bind = self.fitness(self.population[i], self.bind)

	# ps: probability of selection
	# elitism: if there is elitism
	def selection(self,ps=1,elitism=True):
		if(elitism):	# keep the fittest individual?
			pop = [self.bind]
		else:
			pop = []
		for i in range(self.size - len(pop)):	# add the remaining individuals through selection
			if((ps == 1) or (random.random() < ps)):
				ind1 = random.randint(0,self.size - 1)
				ind2 = random.randint(0,self.size - 1)
				while(ind1 == ind2):
					ind2 = random.randint(0,self.size - 1)
				# if(self.population[ind1].fitbest > self.population[ind2].fitbest):	# best fitness is lowest fitness
					# ind1 = ind2
				# pop.append(self.population[ind1])
				pop.append(self.fitness(self.population[ind1], self.population[ind2]))
			else:
				pop.append(self.population[i])
		self.population = pop
		if(not elitism):
			self.bind = self.population[0]
			for i in self.population:
				# if(i.fitbest < self.bind.fitbest):
					# self.bind = i
				self.bind = self.fitness(i, self.bind)

	# ind1 & ind2: indexes of individuals to cross
	# lbda (lambda): crossover parameter
	# fun: fitness function
	def cross(self,ind1,ind2,lbda,fun):
		c1 = self.population[ind1]
		c2 = self.population[ind2]
		o1 = []
		o2 = []
		for i in range(len(c1.position)):
			o1.append([])
			o2.append([])
			for j in range(len(c1.position[i])):
				o1[i].append(c1.position[i][j]*lbda + (1 - lbda)*c2.position[i][j])
				o2[i].append(c2.position[i][j]*lbda + (1 - lbda)*c1.position[i][j])
		return (self.Individual(pos=o1,fun=fun),self.Individual(pos=o2,fun=fun))

	# pc: probability of crossover
	# lbda (lambda): crossover parameter (if equals 0, a random number will be chosen from U[0,1])
	# fun: fitness function
	def crossover(self,pc=0.5,lbda=0.5,fun=None):
		if(fun is None):
			print('Error: no fitness function provided')
		ncross = int(pc * self.size)	# number of individuals to cross
		icross = []	# individuals to cross
		indlist = []	# list of individuals that wont cross
		newpop = []	# list of new individuals (next population)
		for i in range(self.size):	# get all individuals
			indlist.append(i)
		for i in range(ncross):	# choose randomly (pc * popsize) individuals to cross and remove them from
			j = random.randrange(self.size)
			icross.append(j)
			if j in indlist:
				indlist.remove(j)
		while(len(indlist) != (self.size - ncross)):	# remove extra individuals randomly
			try:
				indlist.remove(random.randrange(len(indlist)))
			except:
				continue
		for i in range(len(indlist)):	# start new population with individuals from previous population
			newpop.append(self.population[indlist[i]])
		for i in range(ncross//2):	# append crossed individuals
			c1 = icross[2*i]
			if(c1 == icross[-1]):
				c2 = icross[random.randrange(ncross)]
			else:
				c2 = icross[2*i + 1]
			(o1,o2) = self.cross(c1,c2,random.random() if lbda == 0 else lbda,fun)
			newpop.append(o1)
			newpop.append(o2)
		if(ncross % 2 == 1):
			(o1,o2) = self.cross(random.randrange(self.size),random.randrange(self.size),random.random() if lbda == 0 else lbda,fun)
			newpop.append(self.fitness(o1,o2))
		if((self.size != len(self.population)) or (self.size != len(newpop))):
			print('Error: length(newpop) =',len(newpop),'; length(population) =',len(self.population))
			print('\tncross =',ncross)
			sys.exit(0)
		self.population = newpop
		for i in self.population:
			# if(i.fitbest < self.bind.fitbest):
			# 	self.bind = i
			self.bind = self.fitness(i, self.bind)

	# pm: probability of mutation
	# sigma: standard deviation
	def mutation(self, pm=0.05, sigma=0.3, fun=None):
		for i in range(self.size):
			if(random.random() <= pm):
				for j in range(len(self.population[i].position)):
					for k in range(len(self.population[i].position[j])):
						self.population[i].position[j][k] = random.gauss(self.population[i].position[j][k], sigma)
				self.population[i].evaluate(fun)
		for i in self.population:
			# if(i.fitbest < self.bind.fitbest):
			# 	self.bind = i
			self.bind = self.fitness(i, self.bind)


# it: number of iterations
# npop: number of particles/individuals
# mn: floor value of particles
# mx: ceil value of particles
# k: number of clusters
# d: number of dimensions
def ga(it,npop=15,mn=-50,mx=50,k=1,d=1,fun=euclidian):
	# print('GA:\n\tpopulation size =',npop)
	# print('\tnumber of iterations =',it)
	pop = Population(npop,mn,mx,k,d,fun)
	for i in range(it):
		pop.selection(ps=0.95)
		pop.crossover(pc=0.5, fun=fun)
		pop.mutation(pm=0.1, fun=fun)
	# return (bpos,bfit)
	return pop.bind.fitbest

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
	# print( bbpso(10*k*len(inp[0]),3*k*len(inp[0]),mn,mx,k,len(inp[0]),make(inp)) )
	print( ga(it=10*k*len(inp[0]),npop=3*k*len(inp[0]),mn=mn,mx=mx,k=k,d=len(inp[0]),fun=make(inp)) )	# bigger population, fewer iterations


if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./bbpso datafile number_of_clusters')
	else:
		main(sys.argv[1],int(sys.argv[2]))
