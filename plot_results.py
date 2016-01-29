"""
	Simulation idealer Teilchen zur Modellierung idealer Gase
	Moritz Smolka
	
	Programmiert als Zusatzaufgabe fuer Physikalische Chemie
	17.03.2015

	Graphische Darstellung der Resultate
"""

import matplotlib
import matplotlib.pyplot as plt
import csv
import math

def reader(filename):
	reader = csv.reader(open(filename,"rb"))
	next(reader) #Skip header
	return reader

def plot_pv():
	rows = reader("volume_pressure_a.csv") #V,p,pV
	V = []
	p = []
	for row in rows:
		V.append(float(row[0])/1000)
		p.append(row[1])

	plt.scatter(V,p)
	plt.show()

def plot_pv_const():
	rows = reader("volume_pressure_a.csv") #V,p,pV
	V = []
	pV = []
	for row in rows:
		V.append(float(row[0])/1000)
		pV.append((float(row[0])/1000) * float(row[1]))

	plt.plot(V,pV)
	plt.show()	

def plot_nnd():
	rows = reader("nnd.csv")
	values = [float(row[0]) for row in rows]
	#print(values)
	plt.hist(values,1000)
	plt.show()

def plot_nnd_adv(v,data,label_prefix=""):
	import matplotlib.pyplot as plt
	import numpy as np
	from scipy.stats import gaussian_kde
	
	density = gaussian_kde(data)
	xs = np.linspace(0,100,300)
	density.covariance_factor = lambda : .25
	density._compute_covariance()
	plt.plot(xs,density(xs),label=(label_prefix+str(v)))
	
def plot_nnds(filename,legend_title="Volume (V)",rev=True):
	nnds = {}
	for row in reader(filename):
		v = round(float(row[0]),3)

		if v in nnds:
			nnds[v].append(d)
		else:
			nnds[v] = []

	plt.xlabel("Nearest-Neighbour Distance (nm)")
	plt.ylabel("Probability Density")

	for v in sorted(nnds,reverse=rev):
		plot_nnd_adv(v,nnds[v])

	plt.legend(title=legend_title)

def plot_nnd_means(filename,legend_title=""):
	nnds = {}
	for row in reader(filename):
		v = float(row[0])
		d = float(row[1])

		if v in nnds:
			nnds[v].append(d)
		else:
			nnds[v] = []

	means = []
	volumes = []

	for v in sorted(nnds,reverse=True):
		total = 0
		for d in nnds[v]:
			total += d
		means.append(total/len(nnds[v]))
		volumes.append(v)

	variances = []
	variance_count = 0
	i=0
	for v in sorted(nnds,reverse=True):
		total = 0
		for d in nnds[v]:
			total += (d-means[i])**2
		variances.append(math.sqrt(total/len(nnds[v])))
		i += 1


	plt.ylabel("Wert")
	plt.xlabel("Druck p=collisions/(time*length)")
	plt.plot(volumes,means,label="Mittelwert")
	plt.plot(volumes,variances,label="Standardabweichung")
	plt.legend(title=legend_title,loc="upper right")

def plot_nnd_single(filename="volume_nnd.csv",what="2860"):
	rows = reader(filename)
	values = []
	for row in rows:
		if row[0] != what:
			continue
		values.append(float(row[1]))
	#print(values)
	plt.hist(values,100)
	plt.show()

#plot_pv()
#plot_nnd_adv([float(row[0]) for row in reader("nnd.csv")])
#plot_nnds("temperature_nnd.csv","avg(v)")
#plot_nnds("pressure_nnd.csv","Pressure (p)",False)
#plot_nnd_means("volume_nnd.csv")

#plot_nnds("temperature_const_pressure_nnd.csv","avg(e)",False)


#plt.xlabel("Volumen (V)")
#plt.ylabel("Druck (p)")
#plot_pv()
#plt.title("Druck bei Variation des Volumens")

#plt.xlabel("Volumen (V)")
#plt.ylabel("pV (=nRT)")
#plt.ylim(0,250)
#plot_pv_const()

#plot_nnds("results/var_temp_const_volume_nnd.csv","avg(e)")
fig = matplotlib.pyplot.gcf()
#fig.set_size_inches(8,4)

plt.tight_layout()
plt.xlim(0,13)
plt.savefig("new_nn1.png")

# plot_nnds("results/var_temp_const_pressure_nnd.csv","avg(e)")
# fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(8,4)

# plt.tight_layout()
# plt.xlim(0,30)
# plt.savefig("new_nn2.png")

# plt.xlim(0,50)
# plot_nnds("results/var_pressure_const_temp_nnd.csv","p=collisions/(time*length)")
# fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(8,4)

# plt.tight_layout()

# plt.savefig("new_nn3.png")

# plot_nnd_means("results/var_pressure_const_temp_nnd.csv")
# fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(8,4)
# plt.tight_layout()
# plt.savefig("new_nn3_means.png")