from enum import Enum
class Link:
	innovation_num = -1
	start_node = 0
	end_node = 0
	weight = 0.0
	enabled = True

class NodeType(Enum):
	NONE = 0
	INPUT = 1
	OUTPUT = 2
	BIAS = 3
	HIDDEN = 4

class Node:
	id = 0
	node_type = NodeType.NONE

class Individual:
	nodes = []
	links = []
