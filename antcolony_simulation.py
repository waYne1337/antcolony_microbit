import os
import time
import random

#define direction constants
NORTH=0
EAST=1
SOUTH=2
WEST=3

#define ant constants
ants=4 #number of ants
MAXANTS=4
MAXPATH=128
MAXPREC=1024*1024

#cumulated Probabilities for state changes (Pheromones)
P=[[0]*4 for i in range(25)]

#paths of ants
pathlen=[0]*MAXANTS
path=[[0]*MAXPATH for i in range(MAXANTS)]

#current coordinate of ants
antc=[0]*MAXANTS;
#direction of ant (north west to south east or other direction)
antd=[1]*MAXANTS #1 = NW to SE; -1 = SE to NW

#function to initialize all variables properly
def init():
	for i in range(MAXANTS):
		antc[i] = 0
		antd[i] = 1
		pathlen[i] = 0
	#start with probability 1/3 to walk false, 2/3 to walk correct
	for i in range(25):
		P[i][NORTH] = 1 * MAXPATH
		P[i][EAST] = 2 * MAXPATH
		P[i][SOUTH] = 2 * MAXPATH
		P[i][WEST] = 1 * MAXPATH
	#initialize borders correctly, also with prob 1/3 to walk false and 2/3 to walk correct
	for i in range(5):
		P[i][NORTH] = 0
		P[i][WEST] *= 2
		P[5*i][WEST] = 0
		P[5*i][NORTH] *= 2
		P[4 + 5*i][EAST] = 0
		P[4 + 5*i][SOUTH] *= 2
		P[20 + i][SOUTH] = 0
		P[20 + i][EAST] *= 2
	#build cumulative counts
	for i in range(25):
		for j in range(1,4):
			P[i][j] += P[i][j-1]
	return

#function to move the ant
def move_ant(pos, d):
	return {
  		NORTH: lambda pos: pos-5,
  		EAST:  lambda pos: pos+1,
		SOUTH: lambda pos: pos+5,
		WEST:  lambda pos: pos-1
	}[d](pos)

#main program
init()
a=0
while 1:
	#switch to next ant
	a=(a+1)%ants
	#output current situation
	M = [' ']*25
	for i in range(ants):
		c=0
		if antd[i] > 0:	#compute coordinate dependend on direction
			c = antc[i]
		else:
			c = 24 - antc[i]
		M[c]='+'
	#do output
	os.system('clear')
	print(" ----- ")
	for i in range(5):
		print("|%s%s%s%s%s|" % (M[5*i],M[5*i+1],M[5*i+2],M[5*i+3],M[5*i+4]))
	print(" ----- ")
	#sleep for a short instance
	time.sleep(0.1 / ants)
	#determine direction where ant should move
	r = random.randrange(0,P[antc[a]][3])
	d = 0;
	while r >= P[antc[a]][d]:
		d = d+1
	#compute new coordinate
	antc[a] = move_ant( antc[a], d )
	#save path
	if pathlen[a] >= MAXPATH:
		pathlen[a] = 0
		antc[a] = 0 #start at zero again
	else:
		path[a][pathlen[a]] = d
		pathlen[a] = pathlen[a]+1
	#check if target is reached
	if antc[a] == 24:
		#update probabilities (like putting pheromones on the path) if path is shortest
		c = 0 #starting coordinate
		for i in range(pathlen[a]):
			d = path[a][i]
			#compute range
			r = 0
			if d > 0:
				r = P[c][d] - P[c][d-1]
			else:
				r = P[c][d]
			#compute increase of range (maximal increase of e~2.7)
			r = 27 * (r // (pathlen[a] - 7)) // 10
			#update probabilities
			while d < 4:
				P[c][d] += r
				d = d+1
			#rescale if values get too big
			if P[c][3] >= MAXPREC:
				for j in range(4):
					P[c][j] = P[c][j] // 4
			#move to next coordinate
			c = move_ant(c, path[a][i])
		#reset ants position and stuff
		antd[a] *= -1 #treat like ant is walking the other way (only virtual)
		antc[a] = 0 #start at zero again
		pathlen[a] = 0 #forget about path












