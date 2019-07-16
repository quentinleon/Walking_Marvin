from structures import Global, Individual, Evaluation, Species
import bisect
from typing import List
import math
import random
import crossover

def reproduce(evaluations: List[Evaluation], nIndividual: int):
	#remap fitness
	minFitness = evaluations[0].score
	maxFitness = evaluations[0].score
	for ev in evaluations:
		if ev.score < minFitness:
			minFitness = ev.score
		if ev.score > maxFitness:
			maxFitness = ev.score
	for ev in evaluations:
		ev.score = (ev.score - minFitness) / (maxFitness - minFitness)
	#speciate
	speciesPool = speciate(evaluations, 13)
	#cull
	cullRate = 0.8
	for species in speciesPool:
		cullNumber = math.floor(len(species.members) * cullRate)
		species.members.sort(reverse = True)
		species.members = species.members[:len(species.members) - cullNumber]
	#loop backwards and get rid of species lower than 2 individual
	for i in range(len(speciesPool) - 1, -1, -1):
		if (len(speciesPool[i].members) < 2):
			speciesPool.pop(i)
	#make babies
	offsprings = []
	totalFitness = 0.0
	for species in speciesPool:
		totalFitness += species.sharedFitness
	for species in speciesPool:
		offspringCount = int(species.sharedFitness / totalFitness * nIndividual)
		for i in range(offspringCount):
			parents = random.sample(species.members, 2)
			if parents[0].score > parents[1].score:
				offsprings.append(crossover.crossover(parents[0].individual, parents[1].individual))
			else:
				offsprings.append(crossover.crossover(parents[1].individual, parents[0].individual))
	return offsprings

def speciate(evaluations, threash: float):
	speciesPool = []
	#for every individuals, compare with every genepool
	for ev in evaluations:
		i = 0
		while i != len(speciesPool):
			distance = geneticDistance(ev.individual, speciesPool[i].representative)
			#print(f"{i} and {distance}")
			if distance < threash:
				speciesPool[i].AddMember(ev)
				break
			i += 1
		if i == len(speciesPool):
			speciesPool.append(Species(ev))
	for species in speciesPool:
		species.CalcSharedFitness()
	print("Number of species in pool: " + str(len(speciesPool)))
	return speciesPool

def geneticDistance(a: Individual, b: Individual):
	#coefficient. let's start with c1, c2 as same cuz that's easier. c3 is for weights
	c = 1.0
	c3 = 0.4
	n = max(len(a.links), len(b.links))
	#compensate for lower n.
	#if (n < 20):
	#	n = 1
	linkDifference = 0
	weightDifference = 0.0
	count = 0
	for i in range(len(b.links)):
		if not a.IsLinkDuplicate(b.links[i]):
			linkDifference += 1
		else:
			count += 1
			weightDifference += abs(b.links[i].weight - a.links[bisect.bisect_left(a.links, b.links[i])].weight)
	if count > 0:
		weightDifference /= float(count)
	#print(n)
	#print(c)
	#print(linkDifference)
	out = c * float(linkDifference) + c3 * weightDifference
	#print(out)
	#git the genetic distance (see resource below)
	return out


#def cull():
	#kill x% from the population
#	return


#two different distance functions:
# https://sharpneat.sourceforge.io/research/speciation-canonical-neat.html
