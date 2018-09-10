import sys
rfilename=sys.argv[1]

matrix={}
sum=0.0
with open(rfilename,"r") as f:
	for lines in f:
		line=lines.strip().split(",")
		time=int(line[0])
		matrix[time]={}
		for i in range(1,len(line)):
			matrix[time][i]=float(line[i])
			sum+=matrix[time][i]
prob={}
for i in matrix:
	prob[i]={}
	for j in matrix[i]:
		prob[i][j]=matrix[i][j]/sum

with open("normalized-"+rfilename,"w") as writefile:
	for time in prob:
		writefile.write(str(time))
		for i in prob[time]:
			writefile.write(","+str(prob[time][i]))
		writefile.write("\n")
