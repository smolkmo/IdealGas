"""
	Simulation idealer Teilchen zur Modellierung idealer Gase
	Moritz Smolka
	
	Programmiert als Zusatzaufgabe fuer Physikalische Chemie
	17.03.2015

	Überprüfung der Vorhersagen der Simulation
"""

from igsim import *
import math
import csv

def testFirstLaw():
	print("Testing first law...")
	sim = Simulation()
	sim.width = 500
	sim.height = 500

	Particle.radius = 1

	t = 60
	dt = 0.001
	for i in range(0,1000):
		part = Particle()
		part.pos = Vector(2*(random.random()-0.5)*sim.width,2*(random.random()-0.5)*sim.height)
		part.vel = Vector(2*(random.random()-0.5)*3000,2*(random.random()-0.5)*3000)
		sim.add(part)

	initial_energy = sim.total_energy()

	for i in range(int(math.ceil(t/dt))):
		sim.step(t)
		print("#%d of %d: sum(e)=%f, delta(sum(e))=%f" % (i,t/dt,sim.total_energy(),abs(sim.total_energy()-initial_energy)))

def calculatePressure(v,n=1000,t=1,dt=0.001):
	sim = Simulation()
	sim.width = math.sqrt(v)
	sim.height = math.sqrt(v)

	for i in range(0,n):
		part = Particle()
		part.pos = Vector(2*(random.random()-0.5)*sim.width,2*(random.random()-0.5)*sim.height)
		part.vel = Vector(2*(random.random()-0.5)*1000,2*(random.random()-0.5)*1000)
		sim.add(part)

	for i in range(int(math.ceil(t/dt))):
		sim.step(dt)
		#print("#%d of %d: wall_collisions=%d" % (i,t/dt,sim.wall_collisions))

	p = (sim.wall_collisions)/float(sim.width*2+sim.height*2)
	return p

def testGasLaw():
	#pV=nRT
	#Kein Stoff,Waerme,Arbeitsaustausch: U=Cv.nRT = const => T = const => nRT = const => pV = const

	V1, V2 = 100*100, 100*10

	p1 = calculatePressure(V1)
	p2 = calculatePressure(V2)

	print("p1(%f),V1(%f),p1V1(%f)",p1,V1,p1*V1)
	print("p2(%f),V2(%f),p2V2(%f)",p2,V2,p2*V2)

	deviation = (((p1*V1) - (p2*V2)) / (p1*V1)) * 100
	print("Deviation from i.G. behaviour: %f%%" % deviation)

def volumeReductionExperiment():
	results = []

	V = 100*100
	step = V/25

	print("V,p,pV")
	while V > 0:
		p = calculatePressure(V,5000,1,0.001)
		results.append([V,p,p*V])

		#print("p(%f),V(%f),pV(%f)",p,V,p*V)
		print(str(V)+","+str(p)+","+str(p*V))
		V -= step

	outfile = open("volume_pressure.csv", "wb")
	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(["V","p","pV"])
	for r in results:
		writer.writerow(r)
	outfile.close()

		
volumeReductionExperiment()
#testGasLaw()