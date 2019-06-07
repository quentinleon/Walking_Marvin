import gym
import numpy as np
from structures import Individual, Node, NodeType, Link

class Dependency:
	nid = 0
	weight = 0.0

class LogicalNode:
	preComputed = False
	cachedOutput = 0
	dependencies = []

	def setCache(self, n):
		self.cachedOutput = n
		self.preComputed = True

	def getOutput(self):
		if not self.preComputed:
			self.computeNode()
		return self.cachedOutput

	def computeNode(self):
		sum = 0
		for dep in self.dependencies:
			sum += nodemap[dep.nid].getOutput() * dep.weight
		self.setCache(np.tanh(sum))

nodemap = {}

def ComputeOutputs(indiv: Individual, input):
	#TODO Check that number of input nodes in net matches number of inputs
	outputNids = []

	#read in every node and create a logical node
	for n in indiv.nodes:
		nodemap[n.nid] = LogicalNode()
		#keep track of which nodes are outputs, we'll need to compute them
		if(n.nodeType == NodeType.OUTPUT):
			outputNids.append(n.nid)
		#if it's an input node, set it's value to it's matched input
		elif (n.nodeType == NodeType.INPUT):
			nodemap[n.nid].setCache(input[n.nid])
		#if it's a bias node, set it's value to 1
		elif(n.nodeType == NodeType.BIAS):
			nodemap[n.nid].setCache(1)
		

		
			


