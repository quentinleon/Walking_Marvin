#neural structure visualizer
import matplotlib.pyplot as plt
from matplotlib import animation
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
	def __init__(self, ns):
		self.nodeStruct = ns
		self.topology = generateTopology(self.nodeStruct)
		self.fig = plt.figure(figsize=(12, 12))
		if not self.shown:
			plt.ion()
			plt.show()
			self.shown = True

	def update(self):
		self.fig.clear()
		for nid, n in self.topology.items():
			c = plt.Circle((n.x, n.y), 0.01, color=("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])))
			self.fig.add_artist(c)
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
	max_depths = [-1] * (deepestNode + 1)
	for nid, node in ns.nodemap.items():
		if node.inputVal:
			node_depths[nid] = deepestNode
		max_depths[node_depths[nid]] += 1

	#convert depth and num in depth to (0-1,0-1) positions
	depth_counts = [0] * (deepestNode + 1)
	for nid in sorted(node_depths.keys()):
		x = ((deepestNode) - node_depths[nid]) / float(deepestNode)
		y = depth_counts[node_depths[nid]] / float(max_depths[node_depths[nid]])
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
	