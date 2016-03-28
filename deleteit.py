FACTOR = 4

INFACTOR = 3

mat = [[[[(0) for x in range(INFACTOR)] for x in range(INFACTOR)] for x in range(FACTOR)] for x in range(FACTOR)]

for i in range (0,FACTOR):
	for j in range (0,FACTOR):
		print mat[i][j],
	print ""