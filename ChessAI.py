#GamePlay
def GetPlayerPositions(board, player):
	ret = []
	for i in range(0,64,1):
		if (board[i] >= player) & (board[i] < player + 10):
			ret += [i]
	
	return ret

def GetPieceLegalMoves(board, position):
	#if (board[position] == 0):
	#	return []
	ret = []
	player = 10
	if (board[position] > 19):
		enemyPos = GetPlayerPositions(board, 10)
		friendPos = GetPlayerPositions(board, 20)
		player = 20
	else:
		enemyPos = GetPlayerPositions(board, 20)
		friendPos = GetPlayerPositions(board, 10)

	col = position % 8
	piece = board[position] % 10

	if (piece == 0): #pawn
		poss = 8
		if (board[position] > 15):
			poss = -8

		#forward one
		if (board[position] > 15) & (position + poss >= 0):
			if (board[position + poss] == 0):
				ret += [position + poss]
		elif (board[position] < 15) & (position + poss < 64):
			if (board[position + poss] == 0):
				ret += [position + poss]
		
		#attack diagonally 
		if ((position + poss + 1) in enemyPos) & (col != 7):
			ret += [position + poss + 1]
		if ((position + poss - 1) in enemyPos) & (col != 0):
			ret += [position + poss - 1]

	elif (piece == 1): #knight
		if (0 <= position - 17):
			if ((position - 17) not in friendPos) & (col != 0):
				ret += [position - 17]
		if (0 <= position - 15):
			if ((position - 15) not in friendPos) & (col != 7):
				ret += [position - 15]
		if (0 <= position - 6):
			if ((position - 6) not in friendPos) & (col < 6):
				ret += [position - 6]
		if (0 <= position - 10):
			if ((position - 10) not in friendPos) & (col > 1):
				ret += [position - 10]

		if (position + 17 < 64):
			if ((position + 17) not in friendPos) & (col != 7):
				ret += [position + 17]
		if (position + 15 < 64):
			if ((position + 15) not in friendPos) & (col != 0):
				ret += [position + 15]
		if (position + 10 < 64):
			if ((position + 10) not in friendPos) & (col < 6):
				ret += [position + 10]
		if (position + 6 < 64):
			if ((position + 6) not in friendPos) & (col > 1):
				ret += [position + 6]

	elif (piece == 2) | (piece == 4) | (piece == 5): #bishop/queen/king
		curPos = position
		while (True):
			curPos -= 9
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 0) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos -= 7
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 7) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 9
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 7) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 7
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 0) | (piece == 5):
				break

	if (piece == 3) | (piece == 4) | (piece == 5): #rook/queen/king
		curPos = position
		while (True):
			curPos -= 8
			if (curPos < 0) | (curPos in friendPos):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (piece == 5):
				break
		curPos = position
		while (True):
			curPos += 8
			if (curPos >= 64) | (curPos in friendPos):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (piece == 5):
				break
		curPos = position
		while (True):
			curPos -= 1
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 0) | (piece == 5):
				break
		curPos = position
		while (True):
			curPos += 1
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			ret += [curPos]
			if (curPos in enemyPos) | (curPos % 8 == 7) | (piece == 5):
				break

	if (piece == 5): #king
		i = 0
		while(True): #removes positions where moving into check
			if (i >= len(ret)):
				break
			hypBoard = list(board)
			hypBoard[ret[i]] = player + 5
			hypBoard[position] = 0

			if (IsPositionUnderThreat(hypBoard, ret[i], player)):
				del ret[i]
			else:
				i += 1
	else:
		kingPos = -1
		for i in range(0, len(friendPos),1): #finds friendly king position
			if board[friendPos[i]] % 10 == 5:
				kingPos = friendPos[i]
				break

		i = 0
		while(True): #removes all moves that put king in check
			if (i >= len(ret)):
				break

			hypBoard = list(board)
			hypBoard[ret[i]] = board[position] 
			hypBoard[position] = 0
			if (IsPositionUnderThreat(hypBoard, kingPos, player)):
				del ret[i]
			else:
				i += 1

	return ret

def GetPieceLegalMovesHelper(board, position):
	if (board[position] == 0):
		return []
	ret = []
	player = 10
	if (board[position] > 19):
		enemyPos = GetPlayerPositions(board, 10)
		friendPos = GetPlayerPositions(board, 20)
		player = 20
	else:
		enemyPos = GetPlayerPositions(board, 20)
		friendPos = GetPlayerPositions(board, 10)

	col =  position % 8
	piece = board[position] % 10

	if (piece == 0): #pawn
		poss = 8
		if (board[position] > 15):
			poss = -8
		
		#attack diagonally 
		if ((position + poss + 1) in enemyPos) & (abs(((position + poss + 1) % 8) - position % 8) <= 1):
			ret += [position + poss + 1]
		if ((position + poss - 1) in enemyPos) & (abs(((position + poss - 1) % 8) - position % 8) <= 1):
			ret += [position + poss - 1]

	elif (piece == 1): #knight
		if (0 <= position - 17):
			if ((position - 17) in enemyPos) & (col != 0):
				ret += [position - 17]
		if (0 <= position - 15):
			if ((position - 15) in enemyPos) & (col != 7):
				ret += [position - 15]
		if (0 <= position - 6):
			if ((position - 6) in enemyPos) & (col < 6):
				ret += [position - 6]
		if (0 <= position - 10):
			if ((position - 10) in enemyPos) & (col > 1):
				ret += [position - 10]

		if (position + 17 < 64):
			if ((position + 17) in enemyPos) & (col != 7):
				ret += [position + 17]
		if (position + 15 < 64):
			if ((position + 15) in enemyPos) & (col != 0):
				ret += [position + 15]
		if (position + 10 < 64):
			if ((position + 10) in enemyPos) & (col < 6):
				ret += [position + 10]
		if (position + 6 < 64):
			if ((position + 6) in enemyPos) & (col > 1):
				ret += [position + 6]

	elif (piece == 2) | (piece == 4) | (piece == 5): #bishop/queen/king
		curPos = position
		while (True):
			curPos -= 9
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 0) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos -= 7
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 7) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 9
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 7) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 7
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 0) | (piece == 5):
				break

	if (piece == 3) | (piece == 4) | (piece == 5): #rook/queen/king
		curPos = position
		while (True):
			curPos -= 8
			if (curPos < 0) | (curPos in friendPos):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 8
			if (curPos >= 64) | (curPos in friendPos):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (piece == 5):
				break

		curPos = position
		while (True):
			curPos -= 1
			if (curPos < 0) | (curPos in friendPos) | (curPos % 8 == 7):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 0) | (piece == 5):
				break

		curPos = position
		while (True):
			curPos += 1
			if (curPos >= 64) | (curPos in friendPos) | (curPos % 8 == 0):
				break
			if (curPos in enemyPos):
				ret += [curPos]
				break
			if (curPos % 8 == 7) | (piece == 5):
				break

	return ret

def IsPositionUnderThreat(board, position, player):
	enemyPos = GetPlayerPositions(board, player + -2*(player - 15))

	for i in range(0, len(enemyPos),1):
		if position in GetPieceLegalMovesHelper(board, enemyPos[i]):
			return True

	return False

def AI_IsPositionUnderThreat(gamestate, position):
	for i in range(0, len(gamestate.GetEnemyPos()),1):
		if position in GetPieceLegalMovesHelper(gamestate.GetBoard(), gamestate.GetEnemyPos()[i]):
			return True

	return False

def IsCheckMate(board, player):
	playerPos = GetPlayerPositions(board, player)
	kingPos = -1
	for i in range(0, len(playerPos),1): #finds friendly king position
		if board[playerPos[i]] % 10 == 5:
			kingPos = playerPos[i]
			break
	if (IsPositionUnderThreat(board, kingPos, player) == False):
		print("#Not in Check")
		return False

	print("#In Check")

	for i in range(0,len(playerPos),1):
		if (len(GetPieceLegalMoves(board, playerPos[i])) != 0):
			return False
		
	return True

#AI
def MakeMove(gamestate, layer, scoreToBeat):
	#Need to get deepest health to top level while swapping sides.

	if (layer == 1): #deepest layer 
		player = gamestate.GetPlayer()
		board = gamestate.GetBoard()
		retList = []
		current = [0,10000000]

		playerPos = GetPlayerPositions(board, player)
		for i in range(0, len(playerPos),1): #for each piece
			moves = GetPieceLegalMoves(board, playerPos[i])
			#print("looking at enemy piece",ConvertToLabel(playerPos[i]))

			for j in range(0, len(moves),1): #for each possible move
				#print("Checked new move")
				nextGameState = GameState(board, playerPos[i], moves[j], player + -2*(player - 15))
				nextGameState.GenHealth()
				retList += [[playerPos[i], moves[j]],nextGameState.GetHealth()] #Adds all healths to evalTree 
				#print(nextGameState.GetHealth())
				#print([playerPos[i], moves[j]],nextGameState.GetHealth())
				if (nextGameState.GetHealth() < current[1]):
					#PrintBoard(nextGameState.GetBoard())
					#print("new win:",nextGameState.GetHealth())
					current = [[playerPos[i], moves[j]],nextGameState.GetHealth()] 
				if (nextGameState.GetHealth() < scoreToBeat):
					return current + [retList]

		return current + [retList]

	else:
		player = gamestate.GetPlayer()
		board = gamestate.GetBoard()
		fromLower = []
		retList = []
		current = [0,-10000000]

		playerPos = GetPlayerPositions(board, player)
		for i in range(0, len(playerPos),1): #for each piece
			moves = GetPieceLegalMoves(board, playerPos[i])

			for j in range(0, len(moves),1): #for each possible move
				nextGameState = GameState(board, playerPos[i], moves[j], player + -2*(player - 15))
				#print("#looking at friend piece move",ConvertToLabel(playerPos[i]),ConvertToLabel(moves[j]))
				fromLower = MakeMove(nextGameState,layer+1,current[1])
				nextGameState.SwapSides()
				nextGameState.GenHealth()
				retList += [[playerPos[i], moves[j]],nextGameState.GetHealth()] + [fromLower]

				if (fromLower[1] > current[1]):
					current = [[playerPos[i], moves[j]],fromLower[1]] 

		return current + [retList]

def GetThreatHealth(gamestate): #Gets health based off how many friendly players are threatened
	ret = 0
	friendPos = gamestate.GetFriendPos()
	board = gamestate.GetBoard()

	for i in range(0,len(friendPos),1):
		#Value of having a piece 
		if (board[friendPos[i]] % 10 == 0): #pawn
			ret += 1
		elif (board[friendPos[i]] % 10 == 1) | (board[friendPos[i]] % 10 == 2): #knight/bishop
			ret += 3
		elif (board[friendPos[i]] % 10 == 3): #rook
			ret += 5
		elif (board[friendPos[i]] % 10 == 4): #queen
			ret += 9
		elif (board[friendPos[i]] % 10 == 5): #king
			ret += 10000

		#Value of freindly piece being threatened 
		if (AI_IsPositionUnderThreat(gamestate, friendPos[i])):
			if (board[friendPos[i]] % 10 == 0): #pawn
				ret -= 1/3
			elif (board[friendPos[i]] % 10 == 1) | (board[friendPos[i]] % 10 == 2): #knight/bishop
				ret -= 3/3
			elif (board[friendPos[i]] % 10 == 3): #rook
				ret -= 5/3
			elif (board[friendPos[i]] % 10 == 4): #queen
				ret -= 9/3
			elif (board[friendPos[i]] % 10 == 5): #king
				ret -= 1000
	return ret

def GetAttackHealth(gamestate): #Gets health based off how many enemy players are threatened
	ret = 0
	board = gamestate.GetBoard()
	friendPos = list(gamestate.GetFriendPos())
	enemyPos = list(gamestate.GetEnemyPos())

	gamestate.SwapSides() #enemy eyes 
	#Value of enemy having a piece 
	for i in range(0,len(enemyPos),1): #for each enemy piece 
		posVal = board[enemyPos[i]]
		if (posVal == 2):
			ret += 8/3 #Value of enemy having a knight-2.6
		elif (posVal == 5):
			ret += 1000 #Value of enemy having the king
		else:
			ret += ((board[enemyPos[i]] % 10+1)**2 - 1)/3 #Value of enemy having another piece: Q-8, B-2.6, R-5

		#Value of threatening an enemy 
		if (AI_IsPositionUnderThreat(gamestate, enemyPos[i])): #if enemy is under threat
			if (posVal == 0): #Threaten a pawn-0.5
				ret -= 1/1.2
			elif (posVal % 10 == 1) | (posVal == 2): #Threaten a knight/bishop-1.5
				ret -= 3/1.2
			elif (posVal == 3): #Threaten a rook-2.5
				ret -= 5/1.2
			elif (posVal == 4): #Threaten a queen-4.5
				ret -= 9/1.2
			elif (posVal == 5): #Threaten a king-2.5
				ret -= 5/1.2

	if (AI_IsPositionUnderThreat(gamestate, gamestate.GetPos2()) == False): #not protected
		gamestate.SwapSides()
		if (AI_IsPositionUnderThreat(gamestate, gamestate.GetPos2())): #and under attack
			ret += (board[gamestate.GetPos2()] % 10 + 2)**3 #really not good
	else:
		gamestate.SwapSides()

	return ret * -1

def GetPositionHealth(gamestate): #Gets health based off how many moves you can make (more is better)
	ret=0
	board = gamestate.GetBoard()
	friendPos = gamestate.GetFriendPos()

	for i in range(0,len(friendPos),1):
		if (board[friendPos[i]] % 10 == 1):
			ret += len(GetPieceLegalMoves(board,friendPos[i]))/4 #Encourages moving knight
		elif (board[friendPos[i]] % 10 == 4):
			ret += len(GetPieceLegalMoves(board,friendPos[i]))/15 #Queen mobility
		elif (board[friendPos[i]] % 10 == 0): #only for pawns - encourages middle ones to move forward
			ret -= ((friendPos[i] // 8) * (gamestate.GetPlayer()-15)/30 + abs(friendPos[i] % 8 - 4)/30)
		else:
			ret += len(GetPieceLegalMoves(board,friendPos[i]))/6

		
	return ret

#Functional
def GenBoard():
	return [ 13, 11, 12, 15, 14, 12, 11, 13,
				10, 10, 10, 10, 10, 10, 10, 10,
				0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 
				0, 0, 0, 0, 0, 0, 0, 0, 
				20, 20, 20, 20, 20, 20, 20, 20, 
				23, 21, 22, 25, 24, 22, 21, 23 ]

def PrintBoard(board):
	cnt = 0
	cnt2 = 2
	print("\n\t     A  B  C  D  E  F  G  H \n\t    ------------------------")
	print("\t 8 |",end='')
	for i in range(63, -1, -1):
		if (board[i] != 0):
			if (board[i] > 15):
				if (board[i] % 10 == 0):
					print(" p ",end='')
				if (board[i] % 10 == 1):
					print(" n ",end='')
				if (board[i] % 10 == 2):
					print(" b ",end='')
				if (board[i] % 10 == 3):
					print(" r ",end='')
				if (board[i] % 10 == 4):
					print(" q ",end='')
				if (board[i] % 10 == 5):
					print(" k ",end='')
			else:
				if (board[i] % 10 == 0):
					print(" P ",end='')
				if (board[i] % 10 == 1):
					print(" N ",end='')
				if (board[i] % 10 == 2):
					print(" B ",end='')
				if (board[i] % 10 == 3):
					print(" R ",end='')
				if (board[i] % 10 == 4):
					print(" Q ",end='')
				if (board[i] % 10 == 5):
					print(" K ",end='')
		else:
			if (cnt % 2 == 0):
				print(" - ",end='')
			else:
				print(" _ ",end='')
		if (i%8==0):
			if (cnt2 < 10):
				print("|",9-cnt2 + 1,end='')
			if (cnt2 < 9):
				print("\n")
				print("\t",9-cnt2,"|",end='')
			cnt -= 1
			cnt2 += 1
		cnt += 1
	print("\n\t    ------------------------\n\t     A  B  C  D  E  F  G  H\n")

def PrintMoves(inp):
	print("#Legal moves: ",end='')
	if (len(inp) < 1):
		print("none\n")
		return True
	for i in range(0,len(inp)-1,1):
		print(str(ConvertToLabel(inp[i])) + ", ",end='')
	print(ConvertToLabel(inp[len(inp)-1]),"\n")
	return True

def PrintAllMoves(board, player):
	playerPos = GetPlayerPositions(board, player)
	for i in range(0, len(playerPos),1):
		print("'"+str(ConvertToLabel(playerPos[i]))+"' ",end='')
		PrintMoves(GetPieceLegalMoves(board, playerPos[i]))

def ConvertToPos(inp):
	ret1 = 0
	ret1 += (int(inp[1]) - 1) * 8
	if (inp[0] == 'a'):
		ret1 += 7
	if (inp[0] == 'b'):
		ret1 += 6
	if (inp[0] == 'c'):
		ret1 += 5
	if (inp[0] == 'd'):
		ret1 += 4
	if (inp[0] == 'e'):
		ret1 += 3
	if (inp[0] == 'f'):
		ret1 += 2
	if (inp[0] == 'g'):
		ret1 += 1
	if (inp[0] == 'h'):
		ret1 += 0

	if (len(inp) < 3):
		return [ret1]

	ret2 = 0
	ret2 += (int(inp[4]) - 1) * 8
	if (inp[3] == 'a'):
		ret2 += 7
	if (inp[3] == 'b'):
		ret2 += 6
	if (inp[3] == 'c'):
		ret2 += 5
	if (inp[3] == 'd'):
		ret2 += 4
	if (inp[3] == 'e'):
		ret2 += 3
	if (inp[3] == 'f'):
		ret2 += 2
	if (inp[3] == 'g'):
		ret2 += 1
	if (inp[3] == 'h'):
		ret2 += 0
	
	return [ret1, ret2]

def ConvertToLabel(inp):
	cnt = 0
	while (True):
		if (cnt * 8 > inp):
			break
		else:
			cnt += 1

	cnt2 = inp % 8

	if (cnt2 == 0):
		return "h"+str(cnt)
	if (cnt2 == 1):
		return "g"+str(cnt)
	if (cnt2 == 2):
		return "f"+str(cnt)
	if (cnt2 == 3):
		return "e"+str(cnt)
	if (cnt2 == 4):
		return "d"+str(cnt)
	if (cnt2 == 5):
		return "c"+str(cnt)
	if (cnt2 == 6):
		return "b"+str(cnt)
	if (cnt2 == 7):
		return "a"+str(cnt)

class GameState:
	def __init__(self, board, pos1, pos2, player):
		self.board = list(board)
		self.player = player
		self.pos1 = 65
		self.pos2 = 65
		if (pos1 != 65):
			self.pos1 = pos1
			self.pos2 = pos2
			self.board[pos2] = self.board[pos1]
			self.board[pos1] = 0
		self.enemyPos = GetPlayerPositions(self.board, player + -2*(player - 15))
		self.friendPos = GetPlayerPositions(self.board, player)
		self.health = 0
		
	def GenHealth(self):
		self.health = 0
		self.health += GetThreatHealth(self)
		self.health += GetPositionHealth(self)
		self.health += GetAttackHealth(self)

	def SwapSides(self):
		self.player = self.player + -2*(self.player - 15)
		temp = list(self.enemyPos)
		self.enemyPos = list(self.friendPos)
		self.friendPos = temp

	def GetHealth(self):
		#print(str(ConvertToLabel(self.pos1))+", "+str(ConvertToLabel(self.pos2))+" =",self.health)
		return self.health
	def SetHealth(self, val):
		self.health = val
	def GetEnemyPos(self):
		return self.enemyPos
	def GetFriendPos(self):
		return self.friendPos
	def GetPlayer(self):
		return self.player
	def GetBoard(self):
		return self.board
	def GetPos1(self):
		return self.pos1
	def GetPos2(self):
		return self.pos2