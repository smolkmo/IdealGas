"""
	Simulation idealer Teilchen zur Modellierung idealer Gase
	Moritz Smolka
	
	Programmiert als Zusatzaufgabe fuer Physikalische Chemie
	17.03.2015

	Kern der Simulation: Definition der Teilchen, Schrittweise Simulation, Erhebung von Daten
"""

import math
import random

class Vector:
	def __init__(self,x_=0,y_=0):
		self.x = float(x_)
		self.y = float(y_)

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Vector(self.x * other, self.y * other)

	def __div__(self, other):
		return Vector(self.x / other, self.y / other)

	def length(self):
		return math.sqrt(self.x*self.x + self.y*self.y)

	def normalize(self):
		if self.length() > 0:
			return self / self.length()
		else:
			return Vector()

	def dot(self,other):
		return self.x * other.x + self.y * other.y

	def __str__(self):
		return "[%.2f,%.2f]" % (self.x,self.y) 

class Particle:
	radius = 3 #nm, wird nur benutzt wenn Simulation.particles_interact==True
	mass = 1   #Nur fuer get_energy() relevant

	def __init__(self):
		self.pos = Vector()
		self.vel = Vector()

	def integrate(self,dt):
		self.pos += self.vel * dt

	def get_energy(self):
		return 0.5 * self.mass * self.vel.length()**2

	def get_nn(self,sim): #Nearest Neighbour Distance
		min_dist = float("inf")

		for part in sim.particles:
			if part == self:
				continue

			if (part.pos - self.pos).length() < min_dist:
				min_dist = (part.pos - self.pos).length()

		return min_dist

class Simulation:
	def __init__(self):
		self.particles = []
		self.width = 300 #nm
		self.height = 150 #nm
		self.wall_collisions = 0
		self.particles_interact = False

	def add(self,part):
		self.particles.append(part)

	def step(self,dt):
		for part in self.particles:
			part.integrate(dt)
			self.constrain(part)

		if self.particles_interact:
			for i in range(0,len(self.particles)):
				for j in range(i,len(self.particles)):
					if i == j:
						continue

					self.collide(self.particles[i],self.particles[j])

	def constrain(self,part):
		collided = False

		if part.pos.x > self.width:
			part.pos.x = self.width
			part.vel.x = -abs(part.vel.x)
			collided = True

		if part.pos.x < -self.width:
			part.pos.x = -self.width
			part.vel.x = abs(part.vel.x)
			collided = True

		if part.pos.y > self.height:
			part.pos.y = self.height
			part.vel.y = -abs(part.vel.y)
			collided = True

		if part.pos.y < -self.height:
			part.pos.y = -self.height
			part.vel.y = abs(part.vel.y)
			collided = True

		if collided:
			self.wall_collisions += 1

	def collide(self,a,b): #Partikel-Partikel Kollisionen
		dist = a.pos - b.pos
		if dist.length() == 0 or dist.length() > 2 * a.radius:
			return #Keine Kollision

		un = dist.normalize()
		ut = Vector(-un.y,un.x)

		van = un.dot(a.vel)
		vat_n = ut * ut.dot(a.vel)
		vbn = un.dot(b.vel)
		vbt_n = ut * ut.dot(b.vel)

		van_n = un * vbn
		vbn_n = un * van

		#print("Before",a.energy()+b.energy())

		a.vel = van_n + vat_n
		b.vel = vbn_n + vbt_n

		#print("After",a.energy()+b.energy())

		pen = (2*a.radius) - dist.length()
		a.pos += un * (pen/2)
		b.pos -= un * (pen/2)

		#raw_input()
		#raise SystemExit

	def total_energy(self):
		sum = 0
		for part in self.particles:
			sum += part.get_energy()
		return sum

	def avg_energy(self):
		return self.total_energy() / len(self.particles)

	def pressure(self):
		return (self.wall_collisions)/float(self.width*2+self.height*2)