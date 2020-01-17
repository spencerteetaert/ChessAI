from ChessAI import *
import time

def main():
	board = GenBoard()
	times = []
	print("You are playing against my AI which\ncurrently is capable of looking 2 move\ninto the future. Good luck!\n")
	print("NOTE: This is kids chess. This means\nEn Passant and Castling are not considered\nvalid moves.\n")
	print("Move input format: 'a2 a3'\nCheck available moves (piece): 'a2'\nCheck all available moves: 'Enter'\nReset game: 'r'\n")

	done = False
	while (done == False):
		while(True): #Lowercase move
			
			PrintBoard(board)
			inp = input("Player move: ")
			print("\n")

			if (inp == ""):
				PrintAllMoves(board, 10)
			elif (inp == "i"):
				PrintEverything(board)
			else:
				if (inp == "r"):
					board = GenBoard()
					break
				pos = ConvertToPos(inp)

				if (len(pos) < 2):
					PrintMoves(GetPieceLegalMoves(board, pos[0]))
				else:	
					playerPos = GetPlayerPositions(board, 10)
					legalMoves = GetPieceLegalMoves(board, pos[0])

					if (pos[0] not in playerPos):
						print("#ERR: Must move your piece\n")
					elif (pos[1] not in legalMoves):
						print("#ERR: Invalid move\n")
					else:
						if (board[pos[1]] != 0):
							print("Captured:",ConvertToLabel(pos[1]))
						board[pos[1]] = board[pos[0]]
						board[pos[0]] = 0
						#PrintMoves(GetPieceLegalMoves(board, pos[1]))
						if (IsCheckMate(board, 20) == True):
							PrintBoard(board)
							print("#Game Over. Check Mate.")
							done = True
						break

		if (done == False):
			PrintBoard(board)
			print("Computer is thinking...")
			start = time.time()
			nextmove = MakeMove(GameState(board, 65, 65, 20), 0, 0)
			end = time.time()
			times += [round(end-start,2)]
			print("Time elapsed: ",round(end-start,2),"s")

			if (board[nextmove[0][1]] != 0):
				print("Computer captured:",ConvertToLabel(nextmove[0][1]))
			print("Computer move choice:",ConvertToLabel(nextmove[0][0]),ConvertToLabel(nextmove[0][1]))
			board[nextmove[0][1]] = board[nextmove[0][0]]
			board[nextmove[0][0]] = 0

			if (IsCheckMate(board, 10) == True):
				PrintBoard(board)
				print("#Game Over. Check Mate.")
				done = True

	print("times:")
	for i in range(0,len(times),1):
		print(times[i])

main()