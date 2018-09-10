#arguments
import sys

hashthresholdfilename=sys.argv[1]
hashthreshold={}
with open(hashthresholdfilename,"r") as f:
	for lines in f:
		line=lines.strip().split(",")
		time=int(line[0])
		hashthreshold[time]=float(line[1])

	
votethreshold=float(sys.argv[2])


#constants
nodenumber=300
warmup=5*60*20


#initializtion
vote={}
for i in range(1,nodenumber+1):
	vote[i]={}
	for j in range(1,nodenumber+1):
		vote[i][j]=0.0
hashdict={}
timedict={}

#parse verbatimlog
now=warmup/60/20
with open("verbatimlog.csv","r") as f:
	f.readline()
	for line in f:
		lineup=line.strip().split(",")
		time=int(lineup[0])
		if (time>warmup):
			if now<time/60/20:
				print now,":00"
				now=time/60/20
				
			hash=int(lineup[1])
			node=int(lineup[2])
			if hash not in hashdict:
				hashdict[hash]=node
				timedict[hash]=time
			else:
				if (time-timedict[hash]) in hashthreshold:
					vote[hashdict[hash]][node]+=hashthreshold[time-timedict[hash]]

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
