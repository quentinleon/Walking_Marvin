from structures import *
import random
import copy
import gym

## Inits Links for clean state individuals
## starts with no seed. seed when we need it.
def InitLinks(indi: Individual, gl: Global, linkChance: float = 0.5):
	edge = Edge()
	edge.start = 0
	while edge.start < gl.nInput:
		# iterate through output nodes and link by chance.
		edge.end = gl.nInput + 1
		while edge.end < gl.nInput + 1 + gl.nOutput:
			if random.random() < linkChance:
				link = Link()
				link.innovation_num = gl.GetInnovationNum(edge)
				link.path = copy.copy(edge)
				link.weight = random.uniform(-2.0, 2.0)
				link.enabled = True
				indi.links.append(link)
			edge.end += 1
		edge.start += 1
	edge = Edge()

## Inits Gen for Generation 1
def InitGen(nIndividuals: int, nInput: int, nOutput: int):
	outGlobal = Global()
	outGlobal.nInput = nInput
	outGlobal.nOutput = nOutput
	outGlobal.nGen = 1
	outGlobal.env = gym.make('Marvin-v0')

	print("Action space info")
	print(outGlobal.env.action_space)
	print(outGlobal.env.action_space.high)
	print(outGlobal.env.action_space.low)

	print()
	print("Observation space info")
	print(outGlobal.env.observation_space)
	print(outGlobal.env.observation_space.high)
	print(outGlobal.env.observation_space.low)

	for i in range(nIndividuals):
		## Set up for Nodes
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
		InitLinks(elem, outGlobal)
		## Push to list of individuals
		outGlobal.individuals.append(elem)
	return outGlobal

## runs the Generation and get the scores
def RunGen(gl: Global):
	scores = []
	for indi in gl.individuals:
		## just get the high score for now
		maxScore = -999.0
		observed = gl.env.reset()
		## Run till the end of the world
		t = 0
		while True:
			t += 1
			gl.env.render()
			#get action here
			action = gl.env.action_space.sample()
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
