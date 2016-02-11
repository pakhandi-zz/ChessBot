import sys
import ChessBoard

if len(sys.argv) != 3:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

SourceFilename = sys.argv[1]
InitialVerticesCount = sys.argv[2]

obj = ChessBoard.ChessBoard(SourceFilename, InitialVerticesCount)

obj.detectFourCorners()
obj.plotFourCorners()
obj.plotOuterEdges()
obj.detectVerticesOnOuterEdges()
obj.plotAllEdges()
obj.detectAllVertices()
obj.createTopology()
obj.displayTopology()

obj.displayAllVertices()
obj.displayFourCorners()