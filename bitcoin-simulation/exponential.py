#packages
import random
import subprocess
import numpy
import sys


#constants
nodenumber=int(sys.argv[1])
outbound=8
latencyaverage=2*20
propagation=int(sys.argv[2])
maps=int(sys.argv[3])
trials=int(sys.argv[4])

#initialization
stat={}
maxtime=0

for map in range(0,maps):
	connectmap={}
	for i in range(1,nodenumber+1):
		if i not in connectmap:
			connectmap[i]={}
		count=0
		while count<outbound:
			j=random.randint(1,nodenumber)
			if (j<>i) and (j not in connectmap[i]):
				count+=1
			connectmap[i][j]=1
			if j not in connectmap:
				connectmap[j]={}
			connectmap[j][i]=1
	for trial in range (0,trials):
		pending={}
		hop={}
		arrival={}
		for i in range(1,nodenumber+1):
			hop[i]={}
			hop[i][i]=0
			arrival[i]={}
			arrival[i][i]=0
			pending[i]={}
			pending[i][i]=int(numpy.random.exponential(latencyaverage))+propagation
		
		count=0
		time=0
		while count<nodenumber*nodenumber:
			for i in range(1,nodenumber+1):
				todelete={}
				for j in pending[i]:
					if pending[i][j]>0:
						pending[i][j]-=1
					else:
		#				if j==1:
		#					print i,time
						count+=1
						todelete[j]=1
						for k in connectmap[i]:
							if j not in arrival[k]:
								arrival[k][j]=time
								hop[k][j]=hop[i][j]+1
								pending[k][j]=int(numpy.random.exponential(latencyaverage))+propagation
				for j in todelete:
					del pending[i][j]
			time+=1

		if time>maxtime:
			maxtime=time
		print map+1,trial+1,time
		for i in range(1,nodenumber+1):
			for j in range(1,nodenumber+1):
				if hop[i][j] not in stat:
					stat[hop[i][j]]={}
				if arrival[i][j] not in stat[hop[i][j]]:
					stat[hop[i][j]][arrival[i][j]]=1
				else:
					stat[hop[i][j]][arrival[i][j]]+=1
	
maxhop=0
for i in stat:
	if i>maxhop:
		maxhop=i
for i in range(0,maxtime+1):
	for j in range(1,maxhop+1):
		if i not in stat[j]:
			stat[j][i]=0
st=str(nodenumber)+"-"+str(propagation)+"-"+str(maps)+"-"+str(trials)+"test.csv"
with open(st,"w") as f:
	for i in range(0,maxtime+1):
		f.write(str(i))
		for j in range(1,maxhop+1):
			f.write(","+str(stat[j][i]))
		f.write("\n")
	

		