from structures import *
import bisect
import random
from neural_structure import NeuralStructure

## Underscored means non exported function
## Makes a connection between two nodes.
def _mutateConnect(indi: Individual, gl: Global):
	# I don't know the proper way to feedfoward.
	# So I'll check if there's a loop only once.
	# If fails or it's duplicate, no mutation I guess.

	# starting node, everything but outputs
	start = indi.nodes[random.randrange(len(indi.nodes) - gl.nOutput)].nid
	# ending node, everything but starting and bias
	end = indi.nodes[random.randrange(gl.nInput + 1, len(indi.nodes))].nid
	link = Link()
	link.path = Edge(start, end)
	link.innovation_num = gl.GetInnovationNum(link.path)
	link.weight = random.uniform(-1.0, 1.0)
	link.enabled = True
	# if already exists, no mutation.
	if indi.IsLinkDuplicate(link):
		return
	indi.InsertLink(link)
	test = NeuralStructure(indi, True)
	test.resetCache()
	if not test.IsNodeValid(link.path.end):
		indi.PopLink(link)


## Split a connection to form two nodes.
def _mutateSplit(indi: Individual, gl: Global):
	# edge case: if no links, return
	if (len(indi.links) == 0):
		return
	# it's prob better to get the enabled link to be selected
	# get target link
	idx = random.randrange(len(indi.links))
	link = indi.links[idx]
	# disable old link
	indi.links[idx].enabled = False
	# make new node and links
	mediaNode = gl.NewNode(NodeType.HIDDEN)
	indi.InsertNode(mediaNode)
	# prelink keeps all characteristics of target link
	preLink = Link()
	preLink.path = Edge(mediaNode.nid, link.path.end)
	preLink.innovation_num = gl.GetInnovationNum(preLink.path)
	preLink.weight = 1
	preLink.enabled = True
	# postlink is default but has random of 0.8 to 1.2 multiplier
	postLink = Link()
	postLink.path = Edge(link.path.start, mediaNode.nid)
	postLink.innovation_num = gl.GetInnovationNum(postLink.path)
	postLink.weight = link.weight
	postLink.enabled = link.enabled
	# insert both
	indi.InsertLink(preLink)
	indi.InsertLink(postLink)


## Toggle to the enabled
def _mutateToggle(indi: Individual):
	# edge case: if no links, return
	if (len(indi.links) == 0):
		return
	idx = random.randrange(len(indi.links))
	indi.links[idx].enabled = not indi.links[idx].enabled

## Shift weights.
def _mutateShift(indi: Individual):
	# edge case: if no links, return
	if len(indi.links) == 0:
		return
	# target link
	idx = random.randrange(len(indi.links))
	# random action of three. find a better way later.
	action = random.random()
	# multiply between 0.5 to 1.5
	if action < 0.5:
		indi.links[idx].weight *= random.uniform(0.5, 1.5)
	# switch sign
	elif action < 0.7:
		indi.links[idx].weight *= -1
	# add x where abs(x) < 1
	elif action < 1:
		indi.links[idx].weight += random.uniform(-1.0, 1.0)

## mutate n times. Make the sum of rates become 1.
def mutate(indi: Individual, gl: Global, nMutation: int, connectRate: float, splitRate: float, toggleProb: float, shiftProb: float):
	## setup prob array.
	partialSum = []
	sumValue = connectRate
	partialSum.append(sumValue)
	sumValue += splitRate
	partialSum.append(sumValue)
	sumValue += toggleProb
	partialSum.append(sumValue)
	sumValue += shiftProb
	partialSum.append(sumValue)
	## for nMutation times, mutate.
	for i in range(nMutation):
		#find which action to take.
		action = bisect.bisect(partialSum, random.random())
		if action == 0:
			_mutateConnect(indi, gl)
		elif action == 1:
			_mutateSplit(indi, gl)
		elif action == 2:
			_mutateToggle(indi)
		elif action == 3:
			_mutateShift(indi)



