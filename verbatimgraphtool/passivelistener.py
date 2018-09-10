import subprocess
import networkx
countthreshold=30
votethreshold=60

hashdict={}
ipdict={}
countdict={}
vote={}
vote["us"]={}
with open("addrmap.csv","rb") as csvfile:
	for row in csvfile:
		this=row.strip().split(',')
		key=this[0]+"+++++"+this[1]
		ipdict[key]=this[2]


with open("sample.txt","r") as sample:
	for row in sample:
		this=row.strip().split(',')
#		print this[0]
		if this[0] in ipdict:
			key=ipdict[this[0]]
			hash=this[1]
			if hash not in countdict:
				countdict[hash]=1
				hashdict[hash]=key
				if key not in vote["us"]:
					vote["us"][key]=1
#				else:
#					vote["us"][key]+=1
			else:
				if countdict[hash]<=countthreshold :
					countdict[hash]+=1
					if hashdict[hash] not in vote:
						vote[hashdict[hash]]={}
					if key not in vote[hashdict[hash]]:
						vote[hashdict[hash]][key]=1
					else:
						vote[hashdict[hash]][key]+=1
#					hashdict[hash]=key
with open("output.dot","w") as writer:
	writer.write("digraph G {\n")
	for src in vote:
		for dest in vote[src]:
			if vote[src][dest]>=votethreshold:
				line='"'+src+'"'+" -> "+'"'+dest+'"'+" [label="+'"'+str(vote[src][dest])+'"'+"];"
				writer.write("{}\n".format(line))
	writer.write("}\n")
command="dot -Tpdf output.dot -o output.pdf"
subprocess.call(command.split())	
		
				