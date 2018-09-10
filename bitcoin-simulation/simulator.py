#constants
nodenumber=300
groundtruthconnection=30
outboundconnection=8
totaltime=20*60*60*3
leastcost=1
mostcost=2
leastconnectiontime=20*60*60*1
mostconnectiontime=20*60*60*5
transactionsecond=2
godmode={1,10,100,1000,10000,100000}
latencyaverage=2*20

#packages
import random
import subprocess
import numpy

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
with open("groundtruthconnection.txt","w") as groundf:
	for i in range(1,nodenumber+1):
		for j in range(1,nodenumber+1):
			if j in groundtruthmap[i]:
				groundf.write("1")
			else:
				groundf.write("0")
		groundf.write("\n")
with open("groundtruthcost.csv","w") as groundf:
	groundf.write("node1,node2,cost\n")
	for i in range(1,nodenumber+1):
		groundf.write("coinscope,{},{}\n".format(i,coinscopecost[i]))
	for i in range(1,nodenumber+1):
		for j in groundtruthmap[i]:
			groundf.write("{},{},{}\n".format(i,j,groundtruthmap[i][j]))


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
			connectionon[i][j]=random.randint(leastconnectiontime,mostconnectiontime)
			connectionon[j][i]=-1
			counter[i]+=1
with open("connection-time.csv","w") as f:
	f.write("from node,to node,start time,end time\n")
	for i in range(1,nodenumber+1):
		for j in connectionon[i]:
			if connectionon[i][j]>0:
				f.write("{},{},{},{}\n".format(i,j,0,connectionon[i][j]))

#simulation check initialization
mkdir="mkdir godmode"
subprocess.call(mkdir.split())
for i in godmode:
	with open("godmode/"+str(i)+".csv","w") as f:
		f.write("time,node\n")


#broadcast initializtion
pending={}
transactionhash=0
received={}
for i in range(1,nodenumber+1):
	pending[i]={}
	received[i]=set()

#verbatimlog initialization
verbatimlog={}
for time in range(0,totaltime+1):
	verbatimlog[time]={}
with open("verbatimlog.csv","w") as f:
	f.write("time,transaction hash,from node\n")


#simulation
for time in range(0,totaltime+1):
	print time

	#generate transactions
	for i in range(transactionsecond):
		transactionhash+=1
		originator=random.randint(1,nodenumber)
		pending[originator][transactionhash]=0+int(numpy.random.exponential(latencyaverage))

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
						pending[k][j]=groundtruthmap[i][k]+int(numpy.random.exponential(latencyaverage))
		for j in arrived:
			del pending[i][j]
			if time+coinscopecost[i]<=totaltime:
				verbatimlog[time+coinscopecost[i]][j]=i
			if j in godmode:
				with open("godmode/"+str(j)+".csv","a") as f:
					f.write("{},{}\n".format(time,i))

	
	#coinscope recording
	with open("verbatimlog.csv","a") as f:
		for i in verbatimlog[time]:
			f.write("{},{},{}\n".format(time,i,verbatimlog[time][i]))
	del verbatimlog[time]
		

	#dynamic connection
	for i in range(1, nodenumber+1):
		todelete={}
		for j in connectionon[i]:
			if connectionon[i][j]>0:
				if connectionon[i][j]>1:
					connectionon[i][j]-=1
				else:
					todelete[j]=1
					counter[i]-=1;
		for j in todelete:
					del connectionon[i][j]
					del connectionon[j][i]
		while (counter[i]<outboundconnection):
			j=random.choice(groundtruthmap[i].keys())
			if (j not in connectionon[i]):
				connectionon[i][j]=random.randint(leastconnectiontime,mostconnectiontime)
				connectionon[j][i]=-1
				counter[i]+=1
				with open("connection-time.csv","a") as f:
					f.write("{},{},{},{}\n".format(i,j,time,time+connectionon[i][j]))
