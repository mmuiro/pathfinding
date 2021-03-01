# Main file.

import pyglet
from pyglet.window import mouse, key
from pyglet.sprite import Sprite
from colordata import colors
from grid import Grid

# SETUP

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

window = pyglet.window.Window(1080, 900)
vertex_img = pyglet.resource.image("vertex.png")
vertex_img.anchor_x = vertex_img.width // 2
vertex_img.anchor_y = vertex_img.height // 2
spriteBatch = pyglet.graphics.Batch()

labels = []
labels.append(pyglet.text.Label('A-star Pathfinding Visualization', font_name='Courier New', font_size=14, x=window.width // 2, y=window.height - 20, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('Click/Drag to draw', font_name='Courier New', font_size=12, x=window.width // 2, y=180, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('Press Q to switch to drawing walls', font_name='Courier New', font_size=12, x=window.width // 2, y=160, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('W to switch to erasing walls', font_name='Courier New', font_size=12, x=window.width // 2, y=140, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('E to place points to pathfind between', font_name='Courier New', font_size=12, x=window.width // 2, y=120, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('P to perform A-star', font_name='Courier New', font_size=12, x=window.width // 2, y=100, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('O to remove all walls', font_name='Courier New', font_size=12, x=window.width // 2, y=80, anchor_x='center', anchor_y='center'))
labels.append(pyglet.text.Label('R to reset the entire board', font_name='Courier New', font_size=12, x=window.width // 2, y=60, anchor_x='center', anchor_y='center'))

wall_icon = Sprite(x=350, y=160, img=vertex_img, batch=spriteBatch)
wall_icon.update(rotation=45.0)
wall_icon.color = colors['block']

op_icon = Sprite(x=380, y=140, img=vertex_img, batch=spriteBatch)
op_icon.update(rotation=45.0)
op_icon.color = colors['open']

ep_icon = Sprite(x=330, y=120, img=vertex_img, batch=spriteBatch)
ep_icon.update(rotation=45.0)
ep_icon.color = colors['endpoint']

pf_icon = Sprite(x=430, y=100, img=vertex_img, batch=spriteBatch)
pf_icon.update(rotation=45.0)
pf_icon.color = colors['on_path']









gameGrid = Grid(50, 50, (215, 215), vertex_img, colors['open'], spriteBatch)

# EVENT HANDLERS

@window.event
def on_draw():
	window.clear()
	spriteBatch.draw()
	for label in labels:
		label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		gameGrid.modeFunc()(x, y)

@ window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	if buttons & mouse.LEFT:
		gameGrid.modeFunc()(x, y)

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.Q:
		gameGrid.changeMode("Block")
	elif symbol == key.W:
		gameGrid.changeMode("Unblock")
	elif symbol == key.E:
		gameGrid.changeMode("End")
	elif symbol == key.R:
		gameGrid.reset()
	elif symbol == key.O:
		gameGrid.purgeBlocks()
	elif symbol == key.P:
		gameGrid.pathfind()

# RUN

pyglet.app.run()

