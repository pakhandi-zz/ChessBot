import sys
import ChessBoard

if len(sys.argv) != 3:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

SourceFilename = sys.argv[1]
InitialVerticesCount = sys.argv[2]

obj = ChessBoard.ChessBoard(SourceFilename, InitialVerticesCount)
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