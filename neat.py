from structures import *
from neural_structure import NeuralStructure
from ns_vis import Visualizer
import random
import gym
import time
import bisect
import mutate
import selection
import crossover
import arguments

## Inits Links for clean state individuals
## starts with no seed. seed when we need it.
def InitLinks(indi: Individual, gl: Global, linkChance: float = 0.07):
	#random.seed()
	edge = Edge(0, gl.nInput + 1)
	while edge.start < gl.nInput:
		# iterate through output nodes and link by chance.
		edge.end = gl.nInput + 1
		while edge.end < gl.nInput + 1 + gl.nOutput:
			if random.random() < linkChance:
				link = Link()
				link.innovation_num = gl.GetInnovationNum(edge)
				link.path = edge.__copy__()
				link.weight = random.uniform(-2.0, 2.0)
				link.enabled = True
				indi.InsertLink(link)
			edge.end += 1
		edge.start += 1

def LoadGen(path):
	p = Packer()
	f = open(path, "r")
	data = f.read()
	outGlobal = p.unpackGlobal(data)
	f.close()
	return outGlobal


## Inits Gen for Generation 1
def InitGen(nIndividuals: int, nInput: int, nOutput: int):
	outGlobal = Global()
	outGlobal.nInput = nInput
	outGlobal.nOutput = nOutput
	outGlobal.nGen = 1
	outGlobal.nIndividuals = nIndividuals

	## Set up for Nodes with defaults	.
	elem = Individual()
	#24 input nodes
	for i in range(nInput):
		elem.InsertNode(outGlobal.NewNode(NodeType.INPUT))
	#1 bias node
	elem.InsertNode(outGlobal.NewNode(NodeType.BIAS))
	#4 output nodes
	for i in range(nOutput):
		elem.InsertNode(outGlobal.NewNode(NodeType.OUTPUT))

	## randomly link them
	for i in range(nIndividuals):
		e = elem.__copy__()
		InitLinks(e, outGlobal)
		outGlobal.individuals.append(e)
	return outGlobal

## runs the Generation and get the scores
def RunGen(gl: Global):
	evaluations = []
	scores = []
	i = 0
	for indi in gl.individuals:
		print(i)
		reward = 0
		r = 0
		#deathLaser = -1.0
		observed = gl.env.reset()
		neuralStruct = NeuralStructure(indi)

		## Run till the end of the world
		t = 0
		while reward - 0.05 * (t - 50) > -100:
			#gl.env.render()
			action = neuralStruct.ComputeOutputs(observed)
			#print (action)
			observed, r, done, info = gl.env.step(action)
			if done:
				#print("Episode finished after {} timesteps".format(t+1))
				break
			reward += r
			t += 1
			#deathLaser += 0.0025
		#print(maxReward)

		scores.append(Evaluation(indi, reward + r))
		evaluations.append(Evaluation(indi, reward))
		i += 1
	return scores, evaluations

def Simulate(gl: Global, indi: Individual):
	#deathLaser = -1.0
	reward = 0
	observed = gl.env.reset()
	neuralStruct = NeuralStructure(indi)
	args = arguments.getArgs()
	if args.visualize:
		vis = Visualizer(neuralStruct)
	## Run till the end of the world
	r = 0
	t = 0
	while reward - 0.05 * (t - 50) > -100:
		gl.env.render()
		if args.visualize:
			vis.update()
		action = neuralStruct.ComputeOutputs(observed)
		observed, r, done, info = gl.env.step(action)
		reward += r
		#print(reward)
		if done:
			break
		t += 1
		#deathLaser += 0.0025

## setup next generation (select, breed, mutate)
def SetupNextGen(gl: Global, evals: List[Evaluation], scores: List[Evaluation], args):
	gl.individuals = selection.reproduce(evals, gl.nIndividuals)
	scores.sort(reverse = True)
	if args.walk:
		Simulate(gl, scores[0].individual)
	print(scores[0].score)
	sumVal = 0
	for ev in scores:
		sumVal += ev.score
	print(sumVal / gl.nIndividuals)
	for indi in gl.individuals:
		mutate.mutate(indi, gl, 4, 0.2, 0.2, 0.3, 0.3)

