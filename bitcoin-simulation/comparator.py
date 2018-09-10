#get prepared
import sys
criterion=sys.argv[1]
target=sys.argv[2]

#constants
nodenumber=300

#initializtion
totalcount=0
correct=0
falsep=0
falsen=0

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

#read2
read2={}
for i in range(1,nodenumber+1):
	read2[i]={}
with open(target,"r") as f:
	i=0
	for line in f:
		i+=1
		j=0
		lineup=line.strip()
		
		for c in lineup:
			j+=1
			if c=='1':
				read2[i][j]=1

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
print "totalcount     ",totalcount
print "correct        ",correct
print "false negative ",falsen
print "false positive ",falsep