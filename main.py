# Main file.

import pyglet
from pyglet.window import mouse, key
from colordata import colors
from grid import Grid

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

window = pyglet.window.Window(1080, 720)
vertex_img = pyglet.resource.image("vertex.png")
vertex_img.anchor_x = vertex_img.width // 2
vertex_img.anchor_y = vertex_img.height // 2
spriteBatch = pyglet.graphics.Batch()

gameGrid = Grid(50, 50, (215, 35), vertex_img, colors['open'], spriteBatch)

@window.event
def on_draw():
	window.clear()
	spriteBatch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		gameGrid.block_at(x, y)
	elif button == mouse.RIGHT:
		gameGrid.unblock_at(x, y)

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.R:
		gameGrid.purgeBlocks()

pyglet.app.run()

