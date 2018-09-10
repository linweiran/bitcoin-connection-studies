def dictmax(p,n):
	reti={}
	ret={}
	for i in range(1,n+1):
		ret[i]=0
		reti[i]=0
	for j in p:
		i=1
		while (i<n+1) and (p[j]<=ret[i]):
			i+=1
		for k in range(n,i,-1):
			ret[k]=ret[k-1]
			reti[k]=reti[k-1]
		if (i<n+1):
			ret[i]=p[j]
			reti[i]=j
	return reti




#constants
nodenumber=300
groundtruthconnection=30
outboundconnection=8
leastcost=1
mostcost=1
latencyaverage=2*20
maxtrials=20

#packages
import random
import sys
import numpy

hashthresholdfilename=sys.argv[1]
hashthreshold={}
with open(hashthresholdfilename,"r") as f:
	for lines in f:
		line=lines.strip().split(",")
		time=int(line[0])
		hashthreshold[time]=float(line[1])
totaltime=time


#groundtruth generation
groundtruthmap={}
coinscopecost={}
for i in range(1,nodenumber+1):
	groundtruthmap[i]={}
	coinscopecost[i]=random.randint(leastcost,mostcost)
for i in range(1,nodenumber-groundtruthconnection):
	while (len(groundtruthmap[i])<groundtruthconnection):
		j=random.randint(i+1,nodenumber)
#		print j
		if ((j not in groundtruthmap[i])):
			groundtruthmap[i][j]=random.randint(leastcost,mostcost)
			groundtruthmap[j][i]=groundtruthmap[i][j]
for i in range(nodenumber-groundtruthconnection,nodenumber+1):
	while (len(groundtruthmap[i])<groundtruthconnection):
		j=random.randint(1,i-1)
#		print j
		if ((j not in groundtruthmap[i])):
			groundtruthmap[i][j]=random.randint(leastcost,mostcost)
			groundtruthmap[j][i]=groundtruthmap[i][j]



#connection initializtion
connectionon={}
for i in range(1,nodenumber+1):
	connectionon[i]={}
counter={}
for i in range(1,nodenumber+1):
	counter[i]=0
	for j in connectionon[i]:
		if connectionon[i][j]>0 :
			counter[i]+=1
	while (counter[i]<outboundconnection):
		j=random.choice(groundtruthmap[i].keys())
		if (j not in connectionon[i]):
			connectionon[i][j]=1
			connectionon[j][i]=-1
			counter[i]+=1



vote={}
for i in range(1,nodenumber+1):
	vote[i]={}
	for j in range(1,nodenumber+1):
		vote[i][j]=0

for trials in range(1,maxtrials+1):
	print trials
	#verbatimlog initialization
	verbatimlog={}
	for time in range(0,totaltime+1):
		verbatimlog[time]={}

	#broadcast initializtion
	pending={}
	transactionhash=0
	received={}
	for i in range(1,nodenumber+1):
		pending[i]={}
		received[i]=set()

	#generate transactions
	for i in range(1,nodenumber+1):
		transactionhash=i
		originator=i
		pending[originator][transactionhash]=0+int(numpy.random.exponential(latencyaverage))


	#simulation
	for time in range(0,totaltime+1):
		#broadcast
		for i in range(1,nodenumber+1):
			arrived={}
			for j in pending[i]:
				if pending[i][j]>0:
					pending[i][j]-=1
				else:
					arrived[j]=1
					received[i].add(j)
					for k in connectionon[i]:
						if ((j not in received[k]) and ((connectionon[i][k]>=groundtruthmap[i][k]) or (connectionon[k][i]>=groundtruthmap[i][k]))):
							pending[k][j]=3*groundtruthmap[i][k]+int(numpy.random.exponential(latencyaverage))
			for j in arrived:
				del pending[i][j]
				if time+3*coinscopecost[i]<=totaltime:
					verbatimlog[time+coinscopecost[i]][j]=i

	hashtime={}
	for time in verbatimlog:
		for hash in verbatimlog[time]:
			node=verbatimlog[time][hash]
			if hash==node:
				hashtime[node]=time
			else:
				vote[hash][node]+=hashthreshold[time-hashtime[hash]]
				vote[node][hash]+=hashthreshold[time-hashtime[hash]]
	correct=0
	falsen=0
	falsep=0
	for i in range(1,nodenumber+1):
		maxvote=dictmax(vote[i],2*outboundconnection)
		maxvotec={}
		for j in maxvote:
			if maxvote[j] in connectionon[i]:
				correct+=1
			else:
				falsep+=1
			maxvotec[maxvote[j]]=1
		for j in connectionon[i]:
			if j not in maxvotec:
				falsen+=1
	print correct,falsen,falsep