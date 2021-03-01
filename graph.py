# Graph and Vertex classes.
from pyglet.sprite import Sprite
from colordata import colors

class Vertex(Sprite):
	def __init__(self, x, y, img, color, spriteBatch=None, neighbors=[], blocked=False):
		Sprite.__init__(self, x=x, y=y, img=img, batch=spriteBatch)
		self.x = x
		self.y = y
		self.neighbors = neighbors;
		self.visited = False
		self.blocked = blocked
		self.color = color

	# Changes the vertex's status back to unvisited.
	def reset(self):
		self.visited = false

	# Changes this vertex to a block.
	def block(self):
		self.blocked = True

	def unblock(self):
		self.blocked = False

class Graph():

	def __init__(self, V=[], E=[]):
		self.V = V
		self.E = E
		self.endpoints = [] # reserved for pathfinding.
		self.blocked = []

	# Adds a vertex to the graph. Assumes vertex is not already in the graph.
	def addVertex(self, v):
		self.V.append(v)

	# Connects two vertices and creates an edge. Assumes both vertices are in the graph.
	def addEdge(self, v1, v2):
		if v2 not in v1.neighbors and v1 not in v2.neighbors:
			self.E.append((v1,v2))
			v1.neighbors.append(v2)
			v2.neighbors.append(v1)

	# Disconnects two vertices and removes the edge between them.
	def removeEdge(self, v1, v2):
		for i in range(len(self.E)):
			if v1 in self.E[i] and v2 in self.E[i]:
				self.E.pop(i)
				v1.neighbors.remove(v2)
				v2.neighbors.remove(v1)
				return

	# Blocks the vertex if it exists.
	def blockv(self, v):
		if v and v not in self.blocked:
			v.block()
			self.updateColor(v)
			self.blocked.append(v)

	# Unblocks the vertex if it exists.
	def unblockv(self, v):
		if v and v in self.blocked:
			v.unblock()
			self.updateColor(v)
			self.blocked.remove(v)

	# Clears all blocked vertexes, unblocking them.
	def purgeBlocks(self):
		for v in self.blocked[:]:
			self.unblockv(v)
		assert not self.blocked

	# updates the color of the given vertex. Assumes it's in the graph. 
	def updateColor(self, v, current_path=[]):
		if v in self.endpoints:
			v.color = colors['endpoint']
		elif v in current_path:
			v.color = colors['on_path']
		elif v.blocked:
			v.color = colors['block']
		elif v.visited:
			v.color = colors['visited']
		else:
			v.color = colors['open']

	# Returns the resulting path of the A_Star search from v1, v2.
	def AStarSearch(self, v1, v2):
		pass

		