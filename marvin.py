#!/usr/bin/env python3
import neat
import arguments
import sys
import gym

args = arguments.getArgs()
print(args)

individuals = 50
if args.individuals != None:
	individuals = args.individuals

generations = 10
if args.generations != None:
	generations = args.generations

if args.load != None: 
	gen = neat.LoadGen(args.load)
else:
	gen = neat.InitGen(individuals, 24, 4)

gen.env = gym.make('Marvin-v0')
if args.load != None and args.walk:
	neat.Simulate(gen, gen.bestIndi)
	sys.exit()

while True:
	print("-Starting Generation-")
	scores, evals = neat.RunGen(gen)
	print("-Setting New Generation-")
	neat.SetupNextGen(gen, evals, scores, args)
	gen.nGen += 1
	if args.save != None:
		gen.Save(args.save)
	if args.walk:
		break

