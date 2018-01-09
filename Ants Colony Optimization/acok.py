#!/usr/bin/env python3
import sys
import random
import math

# euclidian distance
# if squared is true, the squared distance is returned
def euclidian(a,b,squared=False):
	s = 0
	for i in range(len(a)):
		s = (a[i] - b[i]) * (a[i] - b[i]) + s
	# print(s,math.sqrt(s))
	if(squared):
		return s
	else:
		return math.sqrt(s)

# creates the kmeans optimizer and objective function for the input data
# k is the number of clusters
# n is the number of attributes
def make(inp,k,n):
	def kcenters(S):
		centers = [ [ 0 for i in range(n) ] for j in range(k) ]
		s = [ 0 for i in range(k) ]
		for i in range(len(S)):
			s[S[i]] = s[S[i]] + 1
			for j in range(n):
				centers[S[i]][j] = centers[S[i]][j] + inp[i][j]
        # divides
		for i in range(k):
			for j in range(n):
				centers[i][j] = centers[i][j]/s[i]
		return centers

    # kmeans function
    # S is an agent's solution string
	def kmeans(S):
		# clusters = [ [] for i in range(k) ]
        # # assign the data to the correspondent cluster for each element in the solution string S
		# for i in range(len(a)):
		# 	clusters[a[i]].append(inp[i])

        # calculate each cluster center
        # sums up
		centers = kcenters(S)

        # move any data element to the closest cluster
		for i in range(len(S)):
			closest = euclidian(inp[i],centers[S[i]])
			for j in range(k):
				if(j != S[i]):
					aux = euclidian(inp[i],centers[j])
					if(aux < closest):
						# print('troca')
						S[i] = j
						centers = kcenters(S)
						closest = aux
		return centers

    # objective function
	def objectivef(S,centers=None):
		s = 0
		if(centers is None):
			centers = kcenters(S)
		for i in range(len(inp)):
			s = s + euclidian(inp[i],centers[S[i]])
		return s

	return (kmeans,objectivef)

def bestagent(agents, objfun):
	bestf = objfun(agents[0])
	besta = 0
	# if(threshold is not None):
	# 	# print(threshold)
	# 	while(bestf < threshold):
	# 		i = i + 1
	# 		bestf = objfun(agents[i])
	# 		besta = i
	for j in range(len(agents)):
		aux = objfun(agents[j])
		if(aux < bestf):
			besta = j
			bestf = aux
		# 	if((threshold is not None) and (aux > threshold)):
		# 		besta = j
		# 		bestf = objfun(agents[besta])
	return (besta,bestf)

def topagents(agents, objfun, ntop):
	aux = []
	for i in agents:
		aux.append(i)

	top = []
	for i in range(ntop):
		b = 0
		for j in range(len(aux)):
			if(objfun(aux[j]) < objfun(aux[b])):
				b = j
		top.append(aux.pop(b))
	return top

pheromone = None

# it is the number of iterations
# R is the population size (number of agents, ants)
# K is the number of clusters
# n is the number of attributes
# N is the dataset size
# objective is the objective function
# kmeans is the kmeans function
# qo is probability to choose the cluster with maximum pheromone concentration
# ls is the percentage of itens to be chosen as top solutions
# pot is persistence of trail
def acok(it,R,K,n,N,objective,kmeans,qo=0.98,ls=0.2,pot=0.1):
	S = []
	bestind = None
    # build each agent's solution string
    # first solution is taken randomly
	for j in range(R):
		S.append( [ random.randrange(K) for i in range(N) ] )
	top = []
    # apply kmeans
	if(ls == 1):
        # to all agents
		for i in S:
			kmeans(i)
		top = S
	else:
		# to top agents
		ntop = math.floor(ls*R)
        # best agent and threshold
		# (bag,th) = bestagent(S, objective)
		# kmeans(S[bag])
		# top.append(S[bag])
		top = topagents(S, objective, ntop)
		for i in range(ntop):
			# (bag,th) = bestagent(S, objective, th)
			kmeans(top[i])
			# top.append(S[bag])

	bestind = S[bestagent(S, objective)[0]]

    # fill pheromone matrix
	for item in top:
		delta = 1/objective(item)
		for i in range(N):
			pheromone[item[i]][i] = pheromone[item[i]][i] + delta

    # start iterations
	for iteration in range(it):
		# print(iteration,it)
		S = []
		for i in range(R):
			aux = []
			for j in range(N):
				if(random.random() < qo):
					bestpath = 0
					for k in range(K):
						if(pheromone[k][j] > pheromone[bestpath][j]):
							bestpath = k
					aux.append(bestpath)
				else:
					normalized = []
					s = 0
					for k in range(K):
						normalized.append(pheromone[k][i])
						s = s + pheromone[k][i]
					for k in range(K):
						normalized[k] = normalized[k]/s
					for k in range(1,K):
						normalized[k] = normalized[k] + normalized[k-1]
					rand = random.random()
					for k in range(K):
						if(k == (K-1)):
							aux.append(k)
							# break
						elif((rand > normalized[k]) and (rand < normalized[k+1])):
							aux.append(k)
							break
			S.append(aux)

		top = []
	    # apply kmeans
		if(ls == 1):
	        # to all agents
			for i in S:
				kmeans(i)
			top = S
		else:
			# to top agents
			ntop = math.floor(ls*R)
	        # best agent and threshold
			# (bag,th) = bestagent(S, objective)
			# kmeans(S[bag])
			# top.append(S[bag])
			top = topagents(S, objective, ntop)
			for i in range(ntop):
				# (bag,th) = bestagent(S, objective, th)
				kmeans(top[i])
				# top.append(S[bag])

		aux = S[bestagent(S, objective)[0]]
		if(objective(aux) < objective(bestind)):
			bestind = aux

        # apply evaporate rate
		for i in range(len(pheromone)):
			for j in range(len(pheromone[0])):
				pheromone[i][j] = pheromone[i][j]*(1-pot)
	    # refill pheromone matrix
		for item in top:
			delta = 1/objective(item)
			for i in range(N):
				pheromone[item[i]][i] = pheromone[item[i]][i] + delta

	return (bestind, objective(bestind))

def main(filename, k):
	inp = []
	with open(filename) as fil:
		for line in fil:
			inp.append([float(x) for x in line.split()])
	(kmeans,objective) = make(inp,k,len(inp[0]))
    # generates N x K pheromones matrix
	global pheromone
	pheromone = [ [ 0 for i in range(len(inp)) ] for j in range(k) ]
	for i in range(20):
		res = acok(it=10*k*len(inp[0]), R=3*k*len(inp[0]), K=k, n=len(inp[0]), N=len(inp), objective=objective, kmeans=kmeans)
		print(str(i+1)+': '+str(res[1]).replace('.',','))

if(__name__ == '__main__'):
	if(len(sys.argv) < 3):
		print('Usage: ./acok datafile number_of_clusters')
	else:
		main(sys.argv[1], int(sys.argv[2]))
