#!/usr/bin/env python3
import neat
import arguments

args = arguments.getArgs()
print (args)

gen = neat.InitGen(20, 24, 4)

while True:
	print("-Starting Generation-")
	scores, evals = neat.RunGen(gen)
	print("-Setting New Generation-")
	neat.SetupNextGen(gen, evals, scores)
	gen.nGen += 1