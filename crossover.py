from structures import *
import copy
from neural_structure import NeuralStructure
import random

def crossover(moreFitter: Individual, lessFitter: Individual):
	#in crossover, more fitter always takes all nodes and links
	#child = Individual()
	#child.nodes = copy.deepcopy(moreFitter.nodes)
	#child.links = copy.deepcopy(moreFitter.links)
	#iterate backwards on lessFitter so that we exclude excess
	#i = len(lessFitter.links)
	#while i > 0 and len(child.links) > 0 and lessFitter.links[i - 1].innovation_num > child.links[-1].innovation_num:
	#	i -= 1
	#for every links in lessFitter that is not excess,
	#for j in range(i):
		#try inserting. if it's disjoint, do a random roll.
	#	child.InsertLinkReplace(lessFitter.links[j].__copy__())
	#for every nodes that is not in fitterone, test if it's necessesary
	#toTest = []
	#for i in range(len(lessFitter.nodes)):
	#	if not child.IsNodeDuplicate(lessFitter.nodes[i]):
	#		child.InsertNode(lessFitter.nodes[i])
	#		toTest.append(lessFitter.nodes[i])

	#solve disconnect problem.
	#test = NeuralStructure(child, True)
	#for i in range(len(toTest)):
	#	if not test.IsNodeValid(toTest[i].nid):
	#		child.PopNode(toTest[i])
	#return child
	## after reading the paper, I found that disjoints and excess are also excluded for less fitter.
	child = Individual()
	child.nodes = copy.deepcopy(moreFitter.nodes)
	child.links = copy.deepcopy(moreFitter.links)
	#counter for child links
	i = 0
	# for every links in less fitter,
	for j in range(len(lessFitter.links)):
		# if they are considered same innovation (ref __eq__), randomly replace
		while i != len(child.links) and lessFitter.links[j] > child.links[i]:
			i += 1
		if i == len(child.links):
			break
		if lessFitter.links[j] == child.links[i]:
			if random.random() < 0.5:
				child.links[i] = copy.deepcopy(lessFitter.links[j])
	return child


