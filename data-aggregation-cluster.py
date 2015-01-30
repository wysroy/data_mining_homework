# -*- coding: utf-8 -*-
#cluster algorithm #
#计研146 王奕森 2014310631 #

from math import *

def getdistance(pi,pj):
	tmp = pow(pi[0]-pj[0],2)+pow(pi[1]-pj[1],2)
	return sqrt(tmp)

def choosedc(dc_percent,points,dis,distance):

	maxd = 0
	for i in range(0,len(points)):
		for j in range(i+1,len(points)):
			pi = points[i]
			pj = points[j]
			d = getdistance(pi,pj)
			#print d
			dis.append(d)
			distance[i,j] = d
			dis.append(d)
			distance[j,i] = d
			if d > maxd:
				maxd = d
	dis.sort()

	avgneighbornum = dc_percent*len(points)*len(points)
	#print avgneighbornum
	#print len(points)
	return dis[int(avgneighbornum*2)]

def compute_rho(case,points,dc):
	rho = [0 for i in range(len(points))] #初始化列表
	for i in range(0,len(points)):
		for j in range(i+1,len(points)):
			dij = getdistance(points[i],points[j])
			if case == 1:
				#print 'cut-off kernel'
				if dij < dc:
					rho[i] += 1
					rho[j] += 1
			if case == 2:
				#print 'Gaussian kernel'
				rho[i] += exp(-(dij/dc)*(dij/dc))
				rho[j] += exp(-(dij/dc)*(dij/dc))

	rho_list = [(rho[i],i) for i in range(len(rho))]
	rho_sorted = sorted(rho_list, reverse=1 )
	return [rho_sorted,rho]			

def compute_delta(dis,distance,rho_sorted):
	n = [0 for i in range(len(points))]
	maxd = dis[-1]
	delta = [maxd for i in range(len(points))]
	for i in range(1,len(rho_sorted)):
		for j in range(0,i):
			q_i = rho_sorted[i][1]
			q_j = rho_sorted[j][1]
			if (distance[q_i,q_j] < delta[q_i]):
				delta[q_i] = distance[q_i,q_j]
				n[q_i] = q_j
	return [delta,n]

def assignment(rho_sorted,delta,n):
	cl = [-1 for i in range(len(points))]	
	colornum = 0
	for i in range(len(rho_sorted)):
		q_i = rho_sorted[i][1]
		if (cl[q_i]== -1 and delta[q_i]>2.5):
			cl[q_i] = colornum
			colornum += 1
		else:
			if (cl[q_i] == -1 and cl[n[q_i]!=-1]):
				cl[q_i] = cl[n[q_i]]
	print ('cluster num ='+str(colornum))
	return [cl,colornum]

def draworigin(pl,points,cl,colornum):
	y = [yy for (xx,yy) in points]
	x = [xx for (xx,yy) in points]
	cm = pl.get_cmap("RdYlGn")
	for i in range(len(points)):
		pl.plot(x[i],y[i],'o',color=cm(cl[i]*1.0/colornum))

def drawdecision(pl,rho,delta,cl,colornum):
	cm = pl.get_cmap("RdYlGn")
	for i in range(len(rho)):
		pl.plot(rho[i], delta[i],'o',color=cm(cl[i]*1.0/colornum))
	pl.xlabel(r'$\rho$')
	pl.ylabel(r'$\delta$')

#loading data
fin = open('Aggregation.txt')
points = []
rho = []
delta = []
for line in fin.readlines():
	line = line.split()
	points.append((float(line[0]),float (line[1])))
#print 'points'
#print points[len(points)-1]
fin.close()

#calculating

#dc
dc_percent = 0.02
dis = []
distance = {}
dc = choosedc(dc_percent, points, dis, distance)
print ('dc='+str(dc))

#rho
rho_tmp = compute_rho(1,points,dc)
rho_sorted = rho_tmp[0]
rho = rho_tmp[1]
print ('Highest rho ='+str(rho_sorted[0][0]))

#delta
delta_tmp = compute_delta(dis,distance,rho_sorted)
delta = delta_tmp[0]
n =	delta_tmp[1]
delta_sorted = sorted(delta,reverse =1)
print ('Highest delta =' +str(delta_sorted[0]))

#assignment
cluster = assignment(rho_sorted,delta,n)
cl = cluster[0]
colornum = cluster[1]
#print cluster[1]

#draw graph
import pylab as pl
fig1 = pl.figure(1)
pl.subplot(121)
draworigin(pl,points,cl,colornum)
pl.subplot(122)
drawdecision(pl,rho,delta,cl,colornum)
pl.show()

