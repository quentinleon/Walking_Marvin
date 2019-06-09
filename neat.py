from structures import *
from neural_structure import NeuralStructure
import random
import gym
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
		outGlobal.individuals.append(e)
	return outGlobal

## runs the Generation and get the scores
def RunGen(gl: Global):
	scores = []
	i = 0
	for indi in gl.individuals:
		reward = 0
		maxReward = -999.0
		deathLaser = -5.0
		observed = gl.env.reset()
		neuralStruct = NeuralStructure(indi)

		## Run till the end of the world
		t = 0
		while deathLaser < reward:
			#gl.env.render()
			action = neuralStruct.ComputeOutputs(observed)
			#print (action)
			if reward > maxReward:
				maxReward = reward
			observed, reward, done, info = gl.env.step(action)
			if done:
				#print("Episode finished after {} timesteps".format(t+1))
				break
			t += 1
			deathLaser += 0.03
		print(maxReward)
		scores.append(Evaluation(i, maxReward))
		i += 1
	return scores

## setup next generation (select, breed, mutate)
def SetupNextGen(gl: Global, scores: List[Evaluation]):
	# pick only top 2 and make them fuck
	scores.sort(reverse = True)
	#print (scores[0])
	#print (scores[1])
	nextIndi = []
	for i in range(20):
		more = random.randrange(0, 3)
		less = random.randrange(more, 5)
		top1 = gl.individuals[scores[more].idx]
		top2 = gl.individuals[scores[less].idx]
		nextIndi.append(crossover.crossover(top1, top2))
	gl.individuals = nextIndi
	for indi in gl.individuals:
		mutate.mutate(indi, gl, 7, 0.25, 0.25, 0.25, 0.25)

