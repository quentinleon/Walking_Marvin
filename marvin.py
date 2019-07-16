#!/usr/bin/env python3
import neat
import arguments
import sys
import gym
args = arguments.getArgs()
print(args)
if args.load != None: 
	gen = neat.LoadGen(args.load)
else:
	gen = neat.InitGen(200, 24, 4)
gen.env = gym.make('Marvin-v0')
while True:
	print("-Starting Generation-")
	scores, evals = neat.RunGen(gen)
	print("-Setting New Generation-")
	neat.SetupNextGen(gen, evals, scores)
	gen.nGen += 1
	if args.save != None:
		gen.Save(args.save)

