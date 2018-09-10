#arguments
import sys
hashthreshold=int(sys.argv[1])
votethreshold=int(sys.argv[2])


#constants
nodenumber=300
warmup=500


#initializtion
vote={}
for i in range(1,nodenumber+1):
	vote[i]={}
	for j in range(1,nodenumber+1):
		vote[i][j]=0
hashdict={}
hashcount={}

#parse verbatimlog
now="start"
with open("verbatimlog.csv","r") as f:
	f.readline()
	for line in f:
		lineup=line.strip().split(",")
		if (int(lineup[0])>=warmup):
			if now<>lineup[0]:
				print now
				now=lineup[0]
			hash=int(lineup[1])
			node=int(lineup[2])
			if hash not in hashdict:
				hashdict[hash]=node
				hashcount[hash]=0
			else:
				if hashcount[hash]<hashthreshold:
					hashcount[hash]+=1
					vote[hashdict[hash]][node]+=1

#printout
with open("verbatimparsed.txt","w") as f:
	for i in range(1,nodenumber+1):
		for j in range(1,nodenumber+1):
			mark=0
			if i in vote[j]:
				mark+=vote[j][i]
			if j in vote[i]:
				mark+=vote[i][j]
			if (mark>=votethreshold):
				f.write("1")
			else:
				f.write("0")
		f.write("\n")
