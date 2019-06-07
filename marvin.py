import neat

gen = neat.InitGen(30, 4, 24)
while True:
	scores = neat.RunGen(gen)
	neat.SetupNextGen(gen, scores)
	gen.nGet += 1
