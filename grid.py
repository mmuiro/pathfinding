# Grid class. Most of the underlying logic is in the Graph class.
from graph import Vertex, Graph

class Grid():

	# Grids are initialized as a 2D array of width x height vertices 
	def __init__(self, width, height, origin, vertex_img, color, spriteBatch, spacing=1):
		self.spacing = spacing
		self.origin = origin
		self.img_dims = (vertex_img.width, vertex_img.height)
		self.G = Graph()
		self.width = width
		self.height = height
		self.grid = []
		self.mode = "End"
		self.commands = {"Block": self.block_at, "Unblock": self.unblock_at, "End": self.addEndpoint}
		# Initialize the points
		for r in range(height):
			row = []
			for c in range(width):
				x = origin[0] + c * (self.img_dims[0] + spacing) + self.img_dims[0] // 2
				y = origin[1] + r * (self.img_dims[1] + spacing) + self.img_dims[1] // 2
				v = Vertex(x, y, vertex_img, color, spriteBatch)
				row.append(v)
				self.G.addVertex(v)
			self.grid.append(row)

		# Connect adjacent ones
		for r in range(height):
			for c in range(width):
				for d in (-1,1):
					if self.isValidIndex(r+d,c):
						self.G.addEdge(self.grid[r][c], self.grid[r+d][c]) # addEdge already manages duplicates.
				for d in (-1,1):
					if self.isValidIndex(r,c+d):
						self.G.addEdge(self.grid[r][c], self.grid[r][c+d])

	# Gets the vertex that contains the position (x,y).
	def getVertex(self, x, y):
		rel_x, rel_y = x - self.origin[0], y - self.origin[1]
		r = rel_y // (self.img_dims[1] + self.spacing)
		c = rel_x // (self.img_dims[0] + self.spacing)
		if self.isValidIndex(r,c):
			return self.grid[r][c]
		return None

	# Checks if the given pair (r,c) is within the grid's bounds.
	def isValidIndex(self,r, c):
		return 0 <= r < self.height and 0 <= c < self.width

	# Blocks the vertex at (x,y) if there is one there.
	def block_at(self, x, y):
		v = self.getVertex(x, y)
		self.G.blockv(v)

	# Unblocks the vertex at (x,y) if there is one there.
	def unblock_at(self, x, y):
		v = self.getVertex(x, y)
		self.G.unblockv(v)

	# Uses the graph to clear the blocks.
	def purgeBlocks(self):
		self.G.purgeBlocks()

	# Tells the grid to add an endpoint.
	def addEndpoint(self, x, y):
		v = self.getVertex(x, y)
		if v and not v.blocked:
			self.G.pushEndpoint(v)

	# Tells the graph to perform pathfinding between its endpoints.
	def pathfind(self):
		self.G.pathfindFromEnds()

	# Changes the grid's draw mode.
	def changeMode(self, mode):
		self.mode = mode

	# Returns the method associated with its current mode for drawing.
	def modeFunc(self):
		return self.commands[self.mode]

	# Tells the grid to reset itself.
	def reset(self):
		self.G.resetAll()



