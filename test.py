import sys
import ChessBoard

if len(sys.argv) != 4:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

SourceFilename = sys.argv[1]
InitialVerticesCount = sys.argv[2]
toTest = sys.argv[3]

obj = ChessBoard.ChessBoard(SourceFilename, InitialVerticesCount)

obj.update(toTest)

obj.displayTopology()