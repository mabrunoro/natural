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

class bfgsa():
	def __init__(self):
		print('Creating BFGSA object')

def main():
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
		result = bfgsa()
		if((result[1] < 0) or (result[0] < 0)):
			print('Error: result')
		else:
			print(result[1])
	return 0;

if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./bfgsa datafile number_of_clusters')
	else:
		return main(sys.argv[1],int(sys.argv[2]))

# Define initial parameters.
# Initialize each agent with K random cluster centers
# for Iteration_count=1 to maximum_iterations do
# for all agents i do
# for all pattern Xp in the dataset do
# calculate Euclidean distance of Xp with all cluster centroids;
# assign Xp to the cluster that have nearest centroid to Xp end for
# calculate the fitness function; calculate Gbest and Gworst;
# calculate mass value for all agents
# calculate the acceleration and velocity of agents based on Eq. (29) and Eq.(30);
# calculate the position of each agent
# if stagnant_count > STAGNANT_NUM % check if stagnation has occurred for minimization problem
# call the process of collective response of position change
# End
# end for
# find the global best position
# update the cluster centroids according to velocity updating
# and coordinate updating formula of GSA
# end for
