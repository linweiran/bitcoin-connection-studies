#constants
nodenumber=300

#initializtion
connection={}
for i in range(1,nodenumber+1):
	connection[i]={}

with open("connection-time.csv","r") as f:
	f.readline()
	for line in f:
		lineup=line.strip().split(",")
		node1=int(lineup[0])
		node2=int(lineup[1])
		connection[node1][node2]=1
		connection[node2][node1]=1
with open("parsedconnection.txt","w") as f:
	for i in range(1,nodenumber+1):
		for j in range(1,nodenumber+1):
			if j in connection[i]:
				f.write("1")
			else:
				f.write("0")
		f.write("\n")