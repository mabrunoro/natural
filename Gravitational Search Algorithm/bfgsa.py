#!/usr/bin/env python3

import sys
import math
import random
import math
import copy

def euclidian(a,b):
	s = 0
	for i in range(len(a)):
		s = (a[i] - b[i]) * (a[i] - b[i]) + s
	return math.sqrt(s)

def closest(datav,center,rm = False):
	ret = (datav[0], euclidian(datav[0], center))
	for i in datav[1:]:
		r = euclidian(i, center)
		if(r < ret[1]):
			ret = (i, r)
	if(rm):
		datav.remove(ret[0])
	return ret

class Population:
	# data is the data vector
	# k is the number of clusters (centroids)
	# d is the number of dimensions
	# mn and mx are minimum and maximum values for each direction
	class Agent:
		def __init__(self,data,mn,mx,k=3,d=2):
			# print('Initializing agent')
			# creates centroids with room for data vector
			self.centroids = [ [ [ random.uniform(mn[i],mx[i]) for i in range(d) ] , [] ] for j in range(k) ]
			# # copies data vector
			# indata = data[:]
			# # get closest data from vector to populate all centroids (everyone must have at least one)
			# for i in self.centroids:
			# 	i[1].append(closest(indata,i[0],True)[0])
			# # append the rest of the data to the closest centroid set
			# for i in indata:
			# 	p = (self.centroids[0], euclidian(i, self.centroids[0][0]))
			# 	for j in self.centroids[1:]:
			# 		r = euclidian(i, j[0])
			# 		if(r < p[1]):
			# 			p = (j, r)
			# 	p[0][1].append(i)
			self.clusterize(data)
			self.fitness = 10000000
			self.mass = 0
			self.force = None
			self.k = k
			self.d = d
			self.velocity = [ [ 0 for i in range(self.d) ] for j in range(self.k) ]

		# get the sets
		def clusterize(self,data):
			# copies data vector
			indata = data[:]
			# get closest data from vector to populate all centroids (everyone must have at least one)
			for i in self.centroids:
				i[1] = [closest(indata,i[0],True)[0]]
				# i[1].append(closest(indata,i[0],True)[0])
			# append the rest of the data to the closest centroid set
			for i in indata:
				p = (self.centroids[0], euclidian(i, self.centroids[0][0]))
				for j in self.centroids[1:]:
					r = euclidian(i, j[0])
					if(r < p[1]):
						p = (j, r)
				p[0][1].append(i)

		# objective function
		def objective(self):
			err = 0
			for i in self.centroids:
				siz = len(i[1])
				cen = i[1][0][:]
				t = len(cen)
				for j in i[1][1:]:
					for k in range(t):
						cen[k] = cen[k] + j[k]
				cen = [ k/siz for k in cen ]
				# print('cen:',cen)
				# if(cen[0] > 10):
				# 	print(i)
				# 	sys.exit(0)
				for j in i[1]:
					err = err + euclidian(cen, j)
			# print(err)
			return err

		# generates the agent's mass
		# den is the denominator
		# worst is the worst individuals fitness
		def genmass(self,den,worst):
			self.mass = (self.fitness - worst) / den

		def calcdistance(self, obj):
			s = 0
			for i in range(self.k):
				for j in range(self.d):
					s = s + (self.centroids[i][0][j] - obj.centroids[i][0][j])*(self.centroids[i][0][j] - obj.centroids[i][0][j])
			return math.sqrt(s)

		# calculates the force between two masses
		# obj is the second mass
		# g is the G function based on the gravitational constant
		# ep is the constant to avoid division by zero
		def calcforce(self,obj,g,ep):
			k = g * random.random() * self.mass * obj.mass / (self.calcdistance(obj) + ep)
			f = []
			for i in range(len(self.centroids)):
				f.append([])
				for j in range(self.d):
					f[-1].append((obj.centroids[i][0][j] - self.centroids[i][0][j]) * k )
			return f

		# sets own force (resultant force)
		def setforce(self,rforce):
			self.force = rforce

		def calcacc(self):
			self.acceleration = [ list(map(lambda x: x/(self.mass+0.01),i)) for i in self.force ]

		def calcvel(self):
			self.velocity = [ [ random.random() * self.velocity[i][j] + self.acceleration[i][j] for j in range(self.d) ] for i in range(self.k) ]

		def calcpos(self,data,mn,mx):
			for i in range(self.k):
				for j in range(self.d):
					self.centroids[i][0][j] = self.centroids[i][0][j] + self.velocity[i][j]
					# while(self.centroids[i][0][j] < mn[j]):
					# 	if(self.velocity[i][j] > 0):
					# 		self.centroids[i][0][j] = self.centroids[i][0][j] + self.velocity[i][j]/10
					# 	elif(self.velocity[i][j] < 0):
					# 		self.centroids[i][0][j] = self.centroids[i][0][j] - self.velocity[i][j]/10
					# 	else:
					# 		break
					# while(self.centroids[i][0][j] > mx[j]):
					# 	if(self.velocity[i][j] > 0):
					# 		self.centroids[i][0][j] = self.centroids[i][0][j] - self.velocity[i][j]/10
					# 	elif(self.velocity[i][j] < 0):
					# 		self.centroids[i][0][j] = self.centroids[i][0][j] + self.velocity[i][j]/10
					# 	else:
					# 		break
			self.clusterize(data)

	def __init__(self,data,npop,mn,mx,k,d):
		# print('Creating BFGSA objects')
		self.population = []
		self.size = npop
		for i in range(npop):
			self.population.append(self.Agent(data=data,mn=mn,mx=mx,k=k,d=d))
		self.bindfit = self.population[0].fitness
		self.mn = mn
		self.mx = mx
		# self.extremes()
		# self.calcmasses()

	def calcfits(self):
		for i in self.population:
			i.fitness = i.objective()

	# updates best and worst individuals
	def extremes(self):
		self.wind = self.population[0]
		for i in self.population[1:]:
			if(i.fitness < self.bindfit):
				self.bindfit = i.fitness
			if(i.fitness > self.wind.fitness):
				self.wind = i

	# calculates masses
	def calcmasses(self):
		den = 0
		for i in self.population:
			den = den + (i.fitness - self.wind.fitness)
		for i in self.population:
			i.genmass(den=den,worst=self.wind.fitness)

	# calculates the resultant forces
	# it is the current iteration
	# al is alpha, a constant
	# nit is the total number of iterations
	# go is the gravitational constant
	# ep is constant to avoid division by zero
	def calcforces(self,it,al,nit,go,ep):
		g = go * math.exp(-1 * al * it / nit)
		for i in self.population:
			f = []
			for j in range(i.k):
				f.append([0] * i.d)
			# calculates the force between each object and i
			for j in self.population:
				if(i != j):
					aux = i.calcforce(j,g,ep)
					for k in range(i.k):
						for l in range(i.d):
							f[k][l] = f[k][l] + aux[k][l]
				else:
					continue
			i.setforce(f)

	def calcaccs(self):
		for i in self.population:
			i.calcacc()

	def calcvels(self):
		for i in self.population:
			i.calcvel()

	def calcposs(self,data):
		for i in self.population:
			i.calcpos(data=data,mn=self.mn,mx=self.mx)

	def avoidstagnancy(self):
		for i in self.population:
			distances = [ (i.calcdistance(j),j) for j in self.population if i != j ]
			distances.sort(key=lambda x: x[0], reverse=False)
			r = random.random()*2 - 1
			for j in range(i.k):
				for k in range(i.d):
					for l in range(7):
						i.centroids[j][0][k] = i.centroids[j][0][k] + (r * distances[l][1][j][0][k] / 7)

# it: number of iterations
# npop: number of masses
# mn: floor value of masses
# mx: ceil value of masses
# k: number of clusters
# d: number of dimensions
def bfgsa(datav,it=100,npop=15,mn=-1,mx=1,k=1,d=1):
	
	# Step 1
	alg = Population(data=datav,npop=npop,mn=mn,mx=mx,k=k,d=d)

	stagnant = 0
	prevbfit = alg.bindfit

	for i in range(it):

		# Step 2
		alg.calcfits()
		alg.extremes()

		# Step 3
		alg.calcmasses()

		# Step 4
		alg.calcforces(it=i,al=0.05,nit=it,go=10,ep=0.01)
		alg.calcaccs()

		# Step 5
		alg.calcvels()
		alg.calcposs(datav)

		# Step 6
		if(prevbfit == alg.bindfit):
			stagnant = stagnant + 1
		else:
			stagnant = 0
		if(stagnant >= 4):
			alg.avoidstagnancy()
			stagnant = 0

	return alg.bindfit

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

	result = bfgsa(datav=inp,it=10*k*len(inp[0]),npop=3*k*len(inp[0]),mn=mn,mx=mx,k=k,d=len(inp[0]))
	print(result)

	return 0

if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./bfgsa datafile number_of_clusters')
	else:
		main(sys.argv[1],int(sys.argv[2]))
