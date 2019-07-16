from enum import Enum
from typing import Dict, List
import copy
import bisect
import random
import json
import sys

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
	def __init__(self):
		self.individuals = []
		self.innovations = {}
		self.nInput = 0
		self.nOutput = 0
		self.nNodes = 0
		self.nGen = 1
		self.env = 0
		self.nIndividuals = 0
		self.bestIndi = Individual()

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
		p = Packer()
		tab = 0
		data = p.packGlobal(self)
		f = open(path, "w+")
		f.write(data)
		f.close()

class Packer:
	def writeLine(self, nTab, line):
		out = ""
		for _ in range(nTab):
			out += '\t'
		out += line + '\n'
		return out

	def getline(self, lines):
		if self.i >= len(lines):
			print("invalid file load")
			sys.exit()
		line = lines[self.i]
		self.i += 1
		return line.strip()

	def strToNodeType(self, nodeType):
		if (nodeType == "NodeType.INPUT"):
			return NodeType.INPUT
		elif (nodeType == "NodeType.OUTPUT"):
			return NodeType.OUTPUT
		elif (nodeType == "NodeType.BIAS"):
			return NodeType.BIAS
		elif (nodeType == "NodeType.HIDDEN"):
			return NodeType.HIDDEN
		else:
			print("invalid loading file")
			sys.exit()

	def packGlobal(self, gl: Global):
		out = ""
		tab = 0
		out += self.writeLine(tab, str(len(gl.individuals)))
		tab += 1
		for indi in gl.individuals:
			out += self.writeLine(tab, str(len(indi.nodes)))
			tab += 1
			for node in indi.nodes:
				out += self.writeLine(tab, str(node.nid))
				out += self.writeLine(tab, str(node.nodeType))
			tab -= 1
			out += self.writeLine(tab, str(len(indi.links)))
			tab += 1
			for link in indi.links:
				out += self.writeLine(tab, str(link.innovation_num))
				tab += 1
				out += self.writeLine(tab, str(link.path.start))
				out += self.writeLine(tab, str(link.path.end))
				tab -= 1
				out += self.writeLine(tab, str(link.weight))
				out += self.writeLine(tab, str(link.enabled))
			tab -= 1
		tab -= 1
		out += self.writeLine(tab, str(len(gl.innovations)))
		tab += 1
		for k, v in gl.innovations.items():
			tab += 1
			out += self.writeLine(tab, str(k[0]))
			out += self.writeLine(tab, str(k[1]))
			tab -= 1
			out += self.writeLine(tab, str(v))
		tab -= 1
		out += self.writeLine(tab, str(gl.nInput))
		out += self.writeLine(tab, str(gl.nOutput))
		out += self.writeLine(tab, str(gl.nNodes))
		out += self.writeLine(tab, str(gl.nGen))
		out += self.writeLine(tab, str(gl.nIndividuals))
		#best individual
		tab += 1
		out += self.writeLine(tab, str(len(gl.bestIndi.nodes)))
		tab += 1
		for node in gl.bestIndi.nodes:
			out += self.writeLine(tab, str(node.nid))
			out += self.writeLine(tab, str(node.nodeType))
		tab -= 1
		out += self.writeLine(tab, str(len(gl.bestIndi.links)))
		tab += 1
		for link in gl.bestIndi.links:
			out += self.writeLine(tab, str(link.innovation_num))
			tab += 1
			out += self.writeLine(tab, str(link.path.start))
			out += self.writeLine(tab, str(link.path.end))
			tab -= 1
			out += self.writeLine(tab, str(link.weight))
			out += self.writeLine(tab, str(link.enabled))
		tab -= 1
		tab -= 1
		return out
	
	def unpackGlobal(self, data):
		out = Global()
		self.i = 0
		lines = data.splitlines()
		nIndividuals = int(self.getline(lines))
		for _ in range(nIndividuals):
			indi = Individual()
			nNodes = int(self.getline(lines))
			for _ in range(nNodes):
				node = Node()
				node.nid = int(self.getline(lines))
				node.nodeType = self.strToNodeType(self.getline(lines))
				indi.nodes.append(node)
			nLinks = int(self.getline(lines))
			for _ in range(nLinks):
				link = Link()
				link.innovation_num = int(self.getline(lines))
				link.path = Edge(int(self.getline(lines)), int(self.getline(lines)))
				link.weight = float(self.getline(lines))
				link.enabled = bool(self.getline(lines))
				indi.links.append(link)
			out.individuals.append(indi)
		nInnovations = int(self.getline(lines))
		for _ in range(nInnovations):
			pair = (int(self.getline(lines)), int(self.getline(lines)))
			out.innovations[pair] = int(self.getline(lines))
		out.nInput = int(self.getline(lines))
		out.nOutput = int(self.getline(lines))
		out.nNodes = int(self.getline(lines))
		out.nGen = int(self.getline(lines))
		out.nIndividuals = int(self.getline(lines))
		#best individual
		out.bestIndi = Individual()
		nNodes = int(self.getline(lines))
		for _ in range(nNodes):
			node = Node()
			node.nid = int(self.getline(lines))
			node.nodeType = self.strToNodeType(self.getline(lines))
			out.bestIndi.nodes.append(node)
		nLinks = int(self.getline(lines))
		for _ in range(nLinks):
			link = Link()
			link.innovation_num = int(self.getline(lines))
			link.path = Edge(int(self.getline(lines)), int(self.getline(lines)))
			link.weight = float(self.getline(lines))
			link.enabled = bool(self.getline(lines))
			out.bestIndi.links.append(link)
		return out
