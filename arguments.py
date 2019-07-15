import argparse

def getArgs():
	parser = argparse.ArgumentParser()

	parser.add_argument("-w", "--walk", action="store_true",
						help="display only walking process")
	parser.add_argument("-v", "--visualize", action="store_true",
						help="visualize the neural net structure when walking")
	parser.add_argument("-i", "--individuals", type=int,
						help="specify number of individuals per generation")
	parser.add_argument("-g", "--generations", type=int,
						help="specify number of generations to run")
	parser.add_argument("-l", "--load", type=str,
						help="load weights for Marvin agent from a file. skips training process")
	parser.add_argument("-s", "--save", type=str,
						help="save weights to a file after running the program")

	return parser.parse_args()