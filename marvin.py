#!/usr/bin/env python3
import neat

gen = neat.InitGen(200, 24, 4)

while True:
	print("-Starting Generation-")
	scores, evals = neat.RunGen(gen)
	print("-Setting New Generation-")
	neat.SetupNextGen(gen, evals, scores)
	gen.nGen += 1
