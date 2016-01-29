"""
	Simulation idealer Teilchen zur Modellierung idealer Gase
	Moritz Smolka
	
	Programmiert als Zusatzaufgabe fuer Physikalische Chemie
	17.03.2015

	Bestimmung der Nearest-Neighbour Verteilung für verschiedene Parameter
"""

from igsim import *
import csv

def nnd(v=1000*1000,n=1000,e=1000,t=10,dt=0.001):
	nn,sim=nnd2(v,n,e,t,dt)
	return nn

def nnd2(v=1000*1000,n=1000,e=1000,t=10,dt=0.001):
	sim = Simulation()
	sim.width = math.sqrt(v)
	sim.height = math.sqrt(v)

	for i in range(0,n):
		part = Particle()
		part.pos = Vector(2*(random.random()-0.5)*sim.width,2*(random.random()-0.5)*sim.height)
		part.vel = Vector(2*(random.random()-0.5),2*(random.random()-0.5)).normalize() * e
		sim.add(part)

	#Simulate t in t/dt steps
	for i in range(int(math.ceil(t/dt))):
		sim.step(dt)
		if i%100==0:
			print("Simulate Step #%d of %d avg_energy(%f)" % (i,t/dt,sim.avg_energy()))

	#Calculate NNDs
	nn = []
	i = 0
	for part in sim.particles:
		i += 1
		if i%100==0:
			print("Calculate NND #%d of %d" % (i,n))
		nn.append(part.get_nn(sim))

	return (nn,sim)

def export_nnd(nnd):
	outfile = open("nnd.csv", "wb")
	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(["nn_distance"])
	for d in nnd:
		writer.writerow([d])
	outfile.close()

def nndPressureVariation():
	outfile = open("var_pressure_const_temp_nnd.csv", "wb")
	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(["pressure","nn_distance"])

	V = 500*500
	step = V/7

	while V > 1000:
		results,sim = nnd2(V,10000,1000,1)
		print("********* Calculated for V=" + str(V) )
		for d in results:
			writer.writerow([sim.pressure(),d])
		outfile.flush()
		V -= step

	outfile.close()	

def nndTemperatureVariation():
	outfile = open("temperature_nnd.csv", "wb")
	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(["avg_energy","nn_distance"])

	e = 1000
	step = e/5

	while e > 0:
		results = nnd(100*100,1000,e,1)
		for d in results:
			writer.writerow([e,d])
		outfile.flush()
		e -= step

	outfile.close()


def doSimulate(v=1000*1000,n=1000,e=1000,t=10,dt=0.001):
	sim = Simulation()
	sim.width = math.sqrt(v)
	sim.height = math.sqrt(v)

	for i in range(0,n):
		part = Particle()
		part.pos = Vector(2*(random.random()-0.5)*sim.width,2*(random.random()-0.5)*sim.height)
		part.vel = Vector(2*(random.random()-0.5),2*(random.random()-0.5)).normalize() * e
		sim.add(part)

	#Simulate t in t/dt steps
	for i in range(int(math.ceil(t/dt))):
		sim.step(dt)
		print("Simulate Step #%d of %d avg_energy(%f)" % (i,t/dt,sim.avg_energy()))

	return sim

def nndTemperatureVariationConstantPressure():
	outfile = open("temperature_const_pressure_nnd.csv", "wb")
	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(["avg_energy","nn_distance"])


	e1 = 100
	v1 = 100*100
	n = 10000
	t = 1
	dt = 0.001

	sim = doSimulate(v1,n,e1,t,dt)
	p1 = sim.pressure() #Const!
	print("Pressure1: " + str(p1) )

	for i in range(7):
		e2 = e1 + i*100
		v2 = v1 * (e2/e1) #Expansion zulassen

		results,sim = nnd2(v2,n,e2,t,dt)
		print("********* Calculated for e=" + str(e2) )
		for d in results:
			writer.writerow([e2,d])
		print("Energy: " + str(e2) + " Pressure1: " + str(p1), " Pressure now: " +str(sim.pressure()) )

		outfile.flush()

	outfile.close()	

#export_nnd(nnd())
#nndPressureVariation()
#nndTemperatureVariation()
nndTemperatureVariationConstantPressure()