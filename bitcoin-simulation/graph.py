#arguments
import sys

hashthresholdfilename=sys.argv[1]
hashthreshold={}
with open(hashthresholdfilename,"r") as f:
	for lines in f:
		line=lines.strip().split(",")
		time=int(line[0])
		hashthreshold[time]=float(line[1])

#constants
nodenumber=300
warmup=5*60*20

start=float(sys.argv[2])
end=float(sys.argv[3])
accuracy=100


step=(end-start)/accuracy
inttool=1
while (step<1):
	inttool*=10
	step*=10
	start*=10
	end*=10

istart=int(start)
iend=int(end)

criterion=sys.argv[4]
#read1
read1={}
for i in range(1,nodenumber+1):
	read1[i]={}
with open(criterion,"r") as f:
	i=0
	for line in f:
		i+=1
		j=0
		lineup=line.strip()
	
		for c in lineup:
			j+=1
			if c=='1':
				read1[i][j]=1



pname=str(nodenumber)+"graph.csv"
with open(pname,"w") as fp:
	fp.write("votethreshold,totalcount,correct,false negative,false positive\n")


	for i in range(istart,iend+1):
		votethreshold=float(i)/float(inttool)	


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
		read2={}
		for i in range(1,nodenumber+1):
			read2[i]={}
			for j in range(1,nodenumber+1):
				mark=0
				if i in vote[j]:
					mark+=vote[j][i]
				if j in vote[i]:
					mark+=vote[i][j]
				if (mark>=votethreshold):
					read2[i][j]=1
		#initializtion
		totalcount=0
		correct=0
		falsep=0
		falsen=0
	



		#count
		for i in range(1,nodenumber+1):
			for j in range(i+1,nodenumber+1):
				totalcount+=1
				if ((j in read1[i]) and (j in read2[i])):
					correct+=1
				if ((j in read1[i]) and (j not in read2[i])):
					falsen+=1
				if ((j not in read1[i]) and (j in read2[i])):
					falsep+=1



		fp.write(str(votethreshold)+","+str(totalcount)+","+str(correct)+","+str(falsen)+","+str(falsep)+"\n")
