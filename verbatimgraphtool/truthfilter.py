con="start"
with open("groundtruth.csv","r") as inputfile:
	with open("output.csv","w") as outputfile:
		for line in inputfile:
			time=line.split(" ")[0]
			if time<>con:
				
				con=time
				print time
			if time=="2017-08-15":
				outputfile.write(line)