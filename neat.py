from structures import *
from neural_structure import NeuralStructure
import random
import gym

## Inits Links for clean state individuals
## starts with no seed. seed when we need it.
def InitLinks(indi: Individual, gl: Global, linkChance: float = 0.2):
	random.seed()
	edge = Edge()
	edge.start = 0
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
				indi.links.append(link)
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
		elem.nodes.append(outGlobal.NewNode(NodeType.INPUT))
	#1 bias node
	elem.nodes.append(outGlobal.NewNode(NodeType.BIAS))
	#4 output nodes
	for i in range(nOutput):
		elem.nodes.append(outGlobal.NewNode(NodeType.OUTPUT))

	## randomly link them
	for i in range(nIndividuals):
		e = elem.__copy__()
		InitLinks(e, outGlobal)
		outGlobal.individuals.append(e)
	return outGlobal

## runs the Generation and get the scores
def RunGen(gl: Global):
	scores = []
	for indi in gl.individuals:
		## just get the high score for now
		maxScore = -999.0
		observed = gl.env.reset()

		neuralStruct = NeuralStructure(indi)

		## Run till the end of the world
		t = 0
		#print(len(indi.links))
		while True:
			t += 1
			gl.env.render()
			action = neuralStruct.ComputeOutputs(observed)
#			print (action)
			#gl.env.action_space.sample()

			observed, reward, done, info = gl.env.step(action)
			if reward > maxScore:
				maxScore = reward
			if done:
				print("Episode finished after {} timesteps".format(t+1))
				break
		scores.append(maxScore)
	return scores

## setup next generation (select, breed, mutate)
def SetupNextGen(gl: Global, scores: List[float]):
	return gl
