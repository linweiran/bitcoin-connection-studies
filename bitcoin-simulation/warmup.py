tag="start"
counter=0
with open("verbatimlog.csv","r") as f:
	for line in f:
		lineup=line.strip().split(",")[0]
		if lineup<>tag:
			print tag,counter
			tag=lineup
			counter=1
		else:
			counter+=1
