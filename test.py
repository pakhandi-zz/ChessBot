import sys
import ChessBoard

if len(sys.argv) != 5:
	print "Correct Usage : python chess_board.py <BlankBoardFilename> <SourceFilename> <NumberOfInitialVertices> <BlackThreshold>"
	exit()

blankFilename = sys.argv[1]
fullFilename = sys.argv[2]
InitialVerticesCount = sys.argv[3]
blackThreshold = sys.argv[4]
#toTest = sys.argv[3]

obj = ChessBoard.ChessBoard(blankFilename, fullFilename, InitialVerticesCount, blackThreshold)
obj.createTopology()
obj.displayTopology()

#obj.update(toTest)

#obj.displayTopology()