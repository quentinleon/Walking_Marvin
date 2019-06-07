import numpy as np
from structures import Individual, Node, NodeType, Link

class NeuralStructure:
	nodemap = {}
	outputNids = []

	def __init__(self, indiv):
		self.nodemap = {}
		self.outputNids = []

		#read in every node and create a logical node
		for n in indiv.nodes:
			self.nodemap[n.nid] = LogicalNode()

			#if it's an output node, log it's id
			if(n.nodeType == NodeType.OUTPUT):
				self.outputNids.append(n.nid)
			#if it's a bias node, set it's value to 1
			elif(n.nodeType == NodeType.BIAS):
				self.nodemap[n.nid].setCache(1)
				self.nodemap[n.nid].inputVal = True
			#if it's an input node, mark it as such
			elif(n.nodeType == NodeType.INPUT):
				self.nodemap[n.nid].inputVal = True
			
		#read in every link and create dependencies from them
		for l in indiv.links:
			if l.enabled:
				new_dep = Dependency(l.path.start, l.weight)
				self.nodemap[l.path.end].addDependency(new_dep)

	def ComputeOutputs(self, input):
		#clear the cache
		for _, n in self.nodemap.items():
			n.cached = False

		#load inputs
		for i in range(len(input)):
			self.nodemap[i].setCache(input[i])

		#create outputs
		outputmap = [0] * len(self.outputNids)
		for o in range(len(self.outputNids)):
			outputmap[o] = self.nodemap[self.outputNids[o]].getOutput(self.nodemap)
		
		return outputmap

class Dependency:
	nid = 0
	weight = 0.0
	def __init__(self, i, w):
		self.nid = i
		self.weight = w
	def __str__(self):
		return(f"{self.nid}  {self.weight}")

class LogicalNode:
	inputVal = False
	cached = False
	cachedOutput = 0
	dependencies = []

	def __init__(self):
		self.dependencies = []

	def addDependency(self, d):
		self.dependencies.append(d)

	def setCache(self, n):
		self.cachedOutput = n
		self.cached = True

	def getOutput(self, nodemap):
		if not self.cached and not self.inputVal:
			self.computeNode(nodemap)
		return self.cachedOutput

	def computeNode(self, nodemap):
		sum = 0
		for dep in self.dependencies:
			sum += nodemap[dep.nid].getOutput(nodemap) * dep.weight
		self.setCache(np.tanh(sum))
