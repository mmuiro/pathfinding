# Graph and Vertex classes.
from pyglet.sprite import Sprite
from colordata import colors
from MaxHeap import MaxHeap
from time import sleep

class Vertex(Sprite):
	def __init__(self, x, y, img, color, spriteBatch=None, blocked=False):
		Sprite.__init__(self, x=x, y=y, img=img, batch=spriteBatch)
		self.x = x
		self.y = y
		self.neighbors = [];
		self.blocked = blocked
		self.color = color
		# for pathfinding
		self.visited = False
		self.cameFrom = None
		self.g = float('inf')
		self.h = 0
		self.f = self.g + self.h 

	# Changes the vertex's status back to pre-pathfinding.
	def reset(self):
		self.visited = False
		self.cameFrom = None
		self.g = float('inf')
		self.h = 0
		self.f = self.g + self.h 

	# Sets this vertex to a block.
	def block(self):
		self.blocked = True

	# Sets this vertex to be open.
	def unblock(self):
		self.blocked = False

	def __repr__(self):
		return str((self.x, self.y))

class Graph():

	def __init__(self):
		self.V = []
		self.E = []
		self.endpoints = [] # reserved for pathfinding.
		self.current_path = [] # reserved for pathfinding.
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

	# Updates the color of the given vertex. Assumes it's in the graph. 
	def updateColor(self, v):
		if self.endpoints and v in self.endpoints:
			v.color = colors['endpoint']
		elif self.current_path and v in self.current_path:
			v.color = colors['on_path']
		elif v.blocked:
			v.color = colors['block']
		elif v.visited:
			v.color = colors['visited']
		else:
			v.color = colors['open']

	# Adds v as an endpoint for pathfinding. Keeps the 2 most recent added endpoints.
	def pushEndpoint(self, v):
		if v not in self.endpoints:
			self.endpoints.append(v)
			if len(self.endpoints) > 2:
				self.updateColor(self.endpoints.pop(0))
			self.updateColor(v)

	# Performs A_Star search from v1 to v2. Updates the graph's current_path.
	def AStarSearch(self, v1, v2):
		self.resetPathfinding()
		comparer = lambda v,w: w.f - v.f
		openQ = MaxHeap(comparator=comparer)
		v1.f, v1.g = 0, 0
		openQ.push(v1)
		while not openQ.is_empty():
			cur = openQ.pop()
			for v in cur.neighbors:
				if v.visited or v.blocked:
					continue
				v.cameFrom = cur
				v.visited = True
				self.updateColor(v)
				if v == v2:
					self.current_path = self.getpath(v1, v2, [])
					for w in self.current_path:
						self.updateColor(w)
					return
				v.g = cur.g
				v.h = self.manhattan_d(v, v2)
				v.f = v.g + v.h
				openQ.push(v)

	# Does AStar pathfinding from the current endpoints of this graph.
	def pathfindFromEnds(self):
		assert len(self.endpoints) == 2, "Needs 2 endpoints"
		self.AStarSearch(self.endpoints[0], self.endpoints[1])

	# Assuming there is a path from e to s from e's parent vertices, returns said path in an array.
	def getpath(self, s, e, arr):
		arr.append(e)
		if s == e:
			arr.reverse()
			return arr
		return self.getpath(s, e.cameFrom, arr)

	# Returns the Manhattan heuristic distance.
	def manhattan_d(self, v1, v2):
		return abs(v1.x - v2.x) + abs(v1.y - v2.y)

	# Resets the entire graph's state to default.
	def resetAll(self):
		self.endpoints = []
		self.resetPathfinding()
		self.purgeBlocks()

	# Resets the graph to pre-pathfinding.
	def resetPathfinding(self):
		self.current_path = []
		for v in self.V:
			v.reset()
			self.updateColor(v)
