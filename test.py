import sys
import ChessBoard

if len(sys.argv) != 4:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

blankFilename = sys.argv[1]
fullFilename = sys.argv[2]
InitialVerticesCount = sys.argv[3]
#toTest = sys.argv[3]

obj = ChessBoard.ChessBoard(blankFilename, fullFilename, InitialVerticesCount)
obj.createTopology()
obj.displayTopology()

#obj.update(toTest)

#obj.displayTopology()