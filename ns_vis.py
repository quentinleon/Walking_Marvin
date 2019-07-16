#neural structure visualizer
import matplotlib.pyplot as plt
import numpy as np
import random
import time

class Point:
	x = 0.0
	y = 0.0
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return (f"({round(self.x, 2)}, {round(self.y, 2)})")

class Visualizer:
	shown = False
	fig = 0
	def __init__(self, ns):
		self.nodeStruct = ns
		self.topology = generateTopology(self.nodeStruct)
		if not Visualizer.shown:
			Visualizer.fig = plt.figure(figsize=(4, 4))
			plt.ion()
			plt.show()
			Visualizer.shown = True

	def update(self):
		Visualizer.fig.clear()
		
		#draw nodes
		for nid, n in self.topology.items():
			size = 0.01 if self.nodeStruct.nodemap[nid].inputVal else 0.03
			amount = np.tanh(abs(self.nodeStruct.nodemap[nid].cachedOutput))
			colour = (1* amount, 0, 0) if self.nodeStruct.nodemap[nid].cachedOutput < 0 else (0, 1 * amount, 0)
			c = plt.Circle((n.x, n.y), size, color=colour)
			Visualizer.fig.add_artist(c)

		#draw edges
		for tnid, n in self.nodeStruct.nodemap.items():
			for dep in n.dependencies:
				toLoc = self.topology[tnid]
				fromLoc = self.topology[dep.nid]
				c = plt.Line2D([toLoc.x,fromLoc.x], [toLoc.y,fromLoc.y], linewidth=1.1, color="black")
				Visualizer.fig.add_artist(c)

		plt.draw()
		plt.pause(.0001)
		
	def close(self):
		print("close")
		plt.close()

def visualize(ns):
	nodeLocs = generateTopology(ns)
	fig = plt.figure(figsize=(10, 10))

	for nid, n in nodeLocs.items():
		c = plt.Circle((n.x, n.y), 0.01)
		fig.add_artist(c)
	plt.show()

def addMargins(x, y, margin):
	return Point(((x * (1 - (2 * margin))) + margin) , ((y * (1 - (2 * margin))) + margin))

def generateTopology(ns):
	deepestNode = 0
	node_depths = {}
	node_locations = {}

	#get all node depths
	for onode in ns.outputNids:
		getDependentDepths(onode, node_depths, ns.nodemap, 0)

	#get the deepest depth
	for nid in node_depths.keys():
		if node_depths[nid] > deepestNode:
			deepestNode = node_depths[nid]
	
	#set all input nodes to deepest depth and count number of nodes at each depth
	max_depths = [0] * (deepestNode + 3)
	for nid, node in ns.nodemap.items():
		if node.inputVal:
			node_depths[nid] = deepestNode
		max_depths[node_depths[nid]] += 1

	#convert depth and num in depth to (0-1,0-1) positions
	depth_counts = [0] * (deepestNode + 1)
	for nid in sorted(node_depths.keys()):
		x = ((deepestNode) - node_depths[nid]) / float(deepestNode)
		y = (depth_counts[node_depths[nid]] / float(max_depths[node_depths[nid]])) + ((1 / float(max_depths[node_depths[nid]])) / 2)
		depth_counts[node_depths[nid]] += 1
		node_locations[nid] = addMargins(x, y, 0.05)
		#print(f"node {nid} pos: {node_locations[nid]}")

	return node_locations


		
def getDependentDepths(nid, ndepths, nmap, d):
	cur_depth = -1
	if nid in ndepths.keys():
		cur_depth = ndepths[nid]
	if d > cur_depth:
		ndepths[nid] = d
		for nextNode in nmap[nid].dependencies:
			getDependentDepths(nextNode.nid, ndepths, nmap, d + 1)
	