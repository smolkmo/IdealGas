"""
	Simulation idealer Teilchen zur Modellierung idealer Gase
	Moritz Smolka
	
	Programmiert als Zusatzaufgabe fuer Physikalische Chemie
	17.03.2015

	Graphische Darstellung der Simulation
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from igsim import *

sim = Simulation()
sim.particles_interact = True

for i in range(0,150):
	part = Particle()
	part.pos = Vector(2*(random.random()-0.5)*sim.width,2*(random.random()-0.5)*sim.height)
	part.vel = Vector(2*(random.random()-0.5),2*(random.random()-0.5)).normalize() * 3000
	sim.add( part )

#a = Particle()
#a.pos = Vector(-30,-25)
#a.vel = Vector(50,50)

#b=Particle()
#sim.add(a)
#sim.add(b)


from Tkinter import *

root = Tk()

canv = Canvas(root, width=2*sim.width, height=2*sim.height)
canv.pack()

step_dt = 0.001

i=0
def update():
	global i

	canv.delete("all")

	sim.step(step_dt)
	
	"""sim.step(0.001)
	i+=1
	if i % 100 == 0:
		pressure = (sim.wall_collisions)/float(sim.width*2+sim.height*2)
		print(pressure,sim.width,pressure*(sim.width*sim.height))
		sim.wall_collisions = 0

	if i % 500 == 0:
		if sim.width > 100:
			sim.width -= 100
			print("")"""

	for part in sim.particles:
		xo = sim.width
		yo = sim.height
		canv.create_oval(xo+part.pos.x-part.radius,yo+part.pos.y-part.radius,xo+part.pos.x+part.radius,yo+part.pos.y+part.radius,fill="red")
		canv.create_line(xo+part.pos.x,yo+part.pos.y,xo+part.pos.x+part.vel.x*step_dt*10,yo+part.pos.y+part.vel.y*step_dt*10)

	#print(sim.temperature())
	root.after(1,update)

root.after(1,update)
root.mainloop()