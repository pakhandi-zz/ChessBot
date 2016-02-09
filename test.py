import ChessBoard

obj = ChessBoard.ChessBoard("temp/Sharp_r2.jpg", 200, 150, 10, 142, 80, 0.13)
corners = obj.getFourCorners()

for point in corners:
	print point

obj.displayFourCorners()
obj.displayFourEdges()
obj.detectVerticesOnOuterEdges()
obj.displayAllEdges()
obj.detectAllVertices()
obj.displayAllVertices()
obj.createTopology()
obj.displayTopology()