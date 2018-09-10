import sys
from math import sqrt
input=sys.argv[1]
timedict={}
with open(input) as r:
	for lines in r:
		line=lines.strip().split(",")
		if int(line[0]) not in timedict:
			timedict[int(line[0])]=int(line[1])
		else:
			timedict[int(line[0])]+=int(line[1])
			
statdict={}
mean=0
variance=0
count=0
for j in timedict:
	if timedict[j] not in statdict:
		statdict[timedict[j]]=1
	else:
		statdict[timedict[j]]+=1
with open("stat-all.csv","w") as f:
	for j in statdict:
		f.write("{},{}\n".format(str(j),str(statdict[j])))
		mean+=j*statdict[j]
		count+=statdict[j]
		variance+=j*j*statdict[j]
meand=float(mean)
countd=float(count)
varianced=float(variance)
meand/=countd
varianced/=countd
varianced-=meand*meand
print "mean: ",meand,"variance: ",varianced,"standard derivation: ",sqrt(varianced)
chosendict={}
start=0
end=0
for j in (start,end):
	if j in timedict:
		if timedict[j] not in chosendict:
			chosendict[timedict[j]]=1
		else:
			chosendict[timedict[j]]+=1
with open("stat-chosen.csv","w") as f:
	for j in chosendict:
		f.write("{},{}\n".format(str(j),str(chosendict[j])))
