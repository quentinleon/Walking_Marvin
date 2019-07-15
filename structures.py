from enum import Enum
from typing import Dict, List
import copy
import bisect
import random
import jsonpickle

class Edge:
	start = -1
	end = -1
	def __init__(self, start: int, end: int):
		self.start = start
		self.end = end
	def __copy__(self):
		return Edge(self.start, self.end)

class Link:
	innovation_num = -1
	path = Edge(-1, -1)
	weight = 0.0
	enabled = True
	def __init__(self):
		self.innovation_num = -1
		self.path = Edge(-1, -1)
		self.weight = 0.0
		self.enabled = True
	def __copy__(self):
		l = Link()
		l.innovation_num = self.innovation_num
		l.path = self.path.__copy__()
		l.weight = self.weight
		l.enabled = self.enabled
		return l
	def __str__(self):
		return(f"{self.weight}\n     {self.path.start}\t-> {self.path.end}\n")
	# operator overloads
	def __lt__(self, other):
		return self.innovation_num < other.innovation_num
	def __gt__(self, other):
		return self.innovation_num > other.innovation_num
	def __eq__(self, other):
		return self.innovation_num == other.innovation_num



class NodeType(Enum):
	NONE = 0
	INPUT = 1
	OUTPUT = 2
	BIAS = 3
	HIDDEN = 4

class Node:
	nid = -1
	nodeType = NodeType.NONE
	def __init__(self):
		self.nid = -1
		self.nodeType = NodeType.NONE
	def __copy__(self):
		n = Node()
		n.nid = self.nid
		n.nodeType = self.nodeType
	# operator overloads
	def __lt__(self, other):
		return self.nid < other.nid
	def __eq__(self, other):
		return self.nid == other.nid


class Individual:
	## make sure that these two are sorted by their ID
	nodes = []
	links = []
	def __init__(self):
		self.nodes = []
		self.links = []

	def __copy__(self):
		i = Individual()
		i.nodes = copy.deepcopy(self.nodes)
		i.links = [] #not copying links.
		#i.links = copy.deepcopy(self.links)
		return i

	## use this instead of manually inserting nodes.
	## it does the error checking for you
	def InsertNode(self, node: Node):
		idx = bisect.bisect(self.nodes, node)
		## if duplicate then panic
		if idx != len(self.nodes) and self.nodes[idx] == node:
			raise Exception("duplicate nodes")
		self.nodes.insert(idx, node)

	def InsertLink(self, link: Link):
		idx = bisect.bisect(self.links, link)
		## if duplicate then panic
		if idx != len(self.links) and self.links[idx] == link:
			raise Exception("duplicate links")
		self.links.insert(idx, link)

	def PopLink(self, link: Link):
		idx = bisect.bisect_left(self.links, link)
		if idx == len(self.links) or self.links[idx] != link:
			raise Exception("no link found")
		self.links.pop(idx)

	def IsLinkDuplicate(self, link: Link):
		idx = bisect.bisect_left(self.links, link)
		return idx != len(self.links) and self.links[idx] == link

class Evaluation:
	def __init__(self, indi: Individual, score: float):
		self.individual = indi
		self.score = score
	def __lt__(self, other):
		return self.score < other.score

class Species:
	def __init__(self, repre: Evaluation):
		self.representative = repre.individual
		self.sharedFitness = repre.score
		self.members = [repre]
	def AddMember(self, ev: Evaluation):
		self.sharedFitness += ev.score
		self.members.append(ev)
	def CalcSharedFitness(self):
		self.sharedFitness /= len(self.members)


class Global:
	individuals = []
	innovations = {}
	nInput = 0
	nOutput = 0
	nNodes = 0
	nGen = 1
	env = 0
	def NewNode(self, nodeType: NodeType):
		node = Node()
		node.nid = self.nNodes
		node.nodeType = nodeType
		self.nNodes += 1
		return node
	def GetInnovationNum(self, edge: Edge):
		if not (edge.start, edge.end) in self.innovations:
			self.innovations[(edge.start, edge.end)] = len(self.innovations)
		return self.innovations[(edge.start, edge.end)]
	def Save(self, path):
		data = jsonpickle.encode(self, unpicklable=False)
		f = open(path, "w+")
		f.write(data)
		f.close()
	def Load(self, path):
		f = open(path, "r")
		data = f.read()
		jsonpickle.decode(data)
		f.close()


