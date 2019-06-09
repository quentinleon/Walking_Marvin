#!/usr/bin/env python3
import neat

gen = neat.InitGen(30, 24, 4)

while True:
	scores = neat.RunGen(gen)
	neat.SetupNextGen(gen, scores)
	gen.nGen += 1
