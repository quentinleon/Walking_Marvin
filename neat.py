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

## Inits Links for clean state individuals
## starts with no seed. seed when we need it.
def InitLinks(indi: Individual, gl: Global, linkChance: float = 0.2):
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


## Inits Gen for Generation 1
def InitGen(nIndividuals: int, nInput: int, nOutput: int):
	outGlobal = Global()
	outGlobal.nInput = nInput
	outGlobal.nOutput = nOutput
	outGlobal.nGen = 1
	outGlobal.env = gym.make('Marvin-v0')

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
		if i == 0:
			#ns = NeuralStructure(e)
			#vis = Visualizer(ns)
			#vis.update()
			print("done")
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
			reward += r
			if done:
				#print("Episode finished after {} timesteps".format(t+1))
				break
			t += 1
			#deathLaser += 0.0025
		#print(maxReward)

		scores.append(Evaluation(indi, reward))
		if done and r != -100:
			evaluations.append(Evaluation(indi, reward + 300))
		else:
			evaluations.append(Evaluation(indi, reward))
		i += 1
	return scores, evaluations

def Simulate(gl: Global, indi: Individual):
	#deathLaser = -1.0
	reward = 0
	observed = gl.env.reset()
	neuralStruct = NeuralStructure(indi)
	vis = Visualizer(neuralStruct)
	## Run till the end of the world
	t = 0
	while reward - 0.05 * (t - 50) > -100:
		gl.env.render()
		vis.update()
		action = neuralStruct.ComputeOutputs(observed)
		observed, r, done, info = gl.env.step(action)
		reward += r
		if done:
			break
		t += 1
		#deathLaser += 0.0025

## setup next generation (select, breed, mutate)
def SetupNextGen(gl: Global, evals: List[Evaluation], scores: List[Evaluation]):
	gl.individuals = selection.reproduce(evals, 200)
	scores.sort(reverse = True)
	Simulate(gl, scores[0].individual)
	print(scores[0].score)
	sumVal = 0
	for ev in scores:
		sumVal += ev.score
	print(sumVal / 200)
	for indi in gl.individuals:
		mutate.mutate(indi, gl, 4, 0.2, 0.1, 0.3, 0.4)

