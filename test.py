#test.py 
# -*- coding: utf-8 -*-

from math import *

def getdistance(pi,pj):
	tmp = pow(pi[0]-pj[0],2)+pow(pj[1]-pj[1],2)
	return sqrt(tmp)


b=getdistance([1,2],[3,4])
print b

p=[[1,2],[1,4],[2,3]]
print len(p)

InputFileName = "Aggregation"
OutputFileName = InputFileName + "_out"
suffix = ".txt"

Fin = open(InputFileName+suffix,"r")
Fout = open(OutputFileName+suffix,"w")

points = []
for line in Fin.readlines():
		data = line.split()
		if len(data)==3:
			a = float(data[0])
			b = float(data[1])
			points.append((a,b))
print points[len(points)-1]