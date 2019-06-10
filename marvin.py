#!/usr/bin/env python3
import neat

gen = neat.InitGen(20, 24, 4)

while False:
	print("-Starting Generation-")
	scores = neat.RunGen(gen)
	print("-Setting New Generation-")
	neat.SetupNextGen(gen, scores)
	gen.nGen += 1
