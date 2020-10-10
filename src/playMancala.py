import sys
import random


N = 6
DEPTH = 6
STONES = 4
P1_STORE = N
P2_STORE = (2*N) + 1

class Mancala:
    def __init__(self, board):
        if not board:
            self.board=[STONES for i in range(2*(N+1))]
            self.board[P1_STORE] = 0
            self.board[P2_STORE] = 0
        else:
            self.board = board
    
    def printBoard(self, player1, player2):
        print("pits :             6   5   4   3   2   1")
        print("                   ------------------------")
        print(player2,"-->", self.board[(2*N)+1], end="")
        print(*["%3d" % self.board[x] for x in range(2*N,N,-1)], sep="|")
        print("                   ------------------------")
        print("                 ", end="")
        print(*["%3d" % self.board[x] for x in range(0,N,1)], sep="|", end=" ")
        print("    ", self.board[N], "<-- ",player1)
        print("                   ------------------------")
        print("pits :             1   2   3   4   5   6")
        print("------------------------------------------")
        print("\n")

    def game_over(self):
        if sum(self.board[0:N]) == 0 or sum(self.board[N+1:(2*N)+1]) == 0:
            return True
        return False
    
    def playMove(self, pit_id):
        size = len(self.board)
        stones = self.board[pit_id]
        self.board[pit_id] = 0
        move_again = False
        if pit_id > P1_STORE:
            while stones:
                pit_id += 1
                pit_id = pit_id % size
                if pit_id == P1_STORE:
                    continue
                else:
                    self.board[pit_id % size] += 1
                stones -= 1
            if pit_id > N and self.board[pit_id] == 1 and pit_id != P2_STORE and self.board[(N-1)-(pit_id-(N+1))] != 0:
                self.board[P2_STORE] += 1 + self.board[(N-1)-(pit_id-(N+1))]
                self.board[pit_id] = 0
                self.board[(N-1)-(pit_id-(N+1))] = 0
            if pit_id == P2_STORE:
                move_again = True
        else:
            while stones:
                pit_id += 1
                pit_id = pit_id % size
                if pit_id == P2_STORE:
                    continue
                else:
                    self.board[pit_id % size] += 1
                stones -= 1
            if pit_id < N and self.board[pit_id] == 1 and pit_id != P1_STORE and self.board[(2*N) - pit_id] != 0:
                self.board[P1_STORE] += 1 + self.board[(2*N) - pit_id]
                self.board[pit_id] = 0
                self.board[(2*N) - pit_id] = 0
            if pit_id == P1_STORE:
                move_again = True
        return move_again

    def getHeuristics(self):
        if self.game_over():
            if self.board[P2_STORE] > self.board[P1_STORE]:
                return self.board[P2_STORE] - self.board[P1_STORE]
            else:
                return self.board[P1_STORE] - self.board[P2_STORE]
        else:
            return self.board[P2_STORE]- self.board[P1_STORE]


def minimax(boardState, depth, maximizingPlayer):
    if depth == 0 or boardState.game_over():
        return boardState.getHeuristics(),-1
    if maximizingPlayer:
        maxVal = float('-inf')
        move = -1
        for i in range(N+1,(2*N)+1):
            if boardState.board[i] == 0: continue
            tempState=Mancala(boardState.board[:])
            maximizingPlayer = tempState.playMove(i);
            value, m =  minimax(tempState, depth-1, maximizingPlayer)
            if value > maxVal:
                move = i
                maxVal = value
        return maxVal, move
    else:
        minVal = float('inf')
        move = -1
        for i in range(0, N):
            if boardState.board[i] == 0: continue
            tempState = Mancala(boardState.board[:])
            maximizingPlayer = tempState.playMove(i);
            value, m = minimax(tempState, depth - 1, not  maximizingPlayer)
            if value < minVal:
                move = i
                minVal = value
        return minVal, move


    
def alphabeta(boardState, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or boardState.game_over():
        return boardState.getHeuristics(),-1
    if maximizingPlayer:
        maxVal = float('-inf')
        move = -1
        for i in range(N+1,(2*N)+1):
            if boardState.board[i] == 0:
                continue
            tempState = Mancala(boardState.board[:])
            maximizingPlayer = tempState.playMove(i);
            value, m =  alphabeta(tempState, depth-1, alpha, beta, maximizingPlayer)
            if value > maxVal:
                move = i
                maxVal = value
            alpha = max(maxVal, alpha)
            if alpha >= beta :
                break
        return maxVal, move
    else:
        minVal = float('inf')
        move = -1
        for i in range(0, N):
            if boardState.board[i] == 0:
                continue
            tempState = Mancala(boardState.board[:])
            maximizingPlayer = tempState.playMove(i);
            value, m = alphabeta(tempState, depth - 1, alpha, beta, not  maximizingPlayer)
            if value < minVal:
                move = i
                minVal = value
            beta = min(minVal, beta)
            if alpha >= beta:
                break
        return minVal, move

def isValidMove(obj, pit_id, opponentFlag):
    if  pit_id <= 0 or pit_id > 6:
        return False
    elif (not opponentFlag and obj.board[pit_id - 1] == 0):
        return False
    elif opponentFlag and obj.board[pit_id + N] == 0:
        return False
    else:
        return True

def declare_results(obj, p1, p2):
    P1_SCORE = obj.board[P1_STORE] + sum(obj.board[0:N])
    P2_SCORE = obj.board[P2_STORE] + sum(obj.board[(N+1):(2*N)+1])
    if  P1_SCORE == P2_SCORE:
        print(p1,' score: ',P1_SCORE,'\n')
        print(p2,' score: ',P2_SCORE,'\n')
        print("Draw Game!")
    elif P1_SCORE > P2_SCORE:
        print(p1,' score: ',P1_SCORE,'\n')
        print(p2,' score: ',P2_SCORE,'\n')
        print(p1,"Wins!")
    else:
        print(p1,' score: ',P1_SCORE,'\n')
        print(p2,' score: ',P2_SCORE,'\n')
        print(p2,"Wins!")

def get_next_move(player, opponentFlag, boardState):
    #print(player.strip(), "'s TURN: ")
    if 'human' in player:
        pit_id = input("Pick your pit: ").split()
        val = int(pit_id[0])
        while not isValidMove(boardState, val,opponentFlag):
            pit_id = input("Illegal Move! Pick a valid pit: ").split()
            val = int(pit_id[0]) 
        val = (val + N) if opponentFlag else (val-1)
        
    elif 'random' in player:
        if not opponentFlag:
            lis = [x for x in range(0,N)]
            r = random.choice(lis)
            while boardState.board[r] == 0:
                lis.remove(r)
                r = random.choice(lis)
            val = r
            print(player,' played move:',r+1) 
        else:
            lis = [x for x in range(N+1, 2*N+1)]
            r = random.choice(lis)
            while boardState.board[r] == 0:
                lis.remove(r)
                r = random.choice(lis)
            val = r
            print(player,' played move:',r-N)
    elif 'minimax' in player:
        if not opponentFlag:
            hval,val = minimax(boardState,DEPTH,False)
            print(player,' played move:',val+1)
        else:
            hval,val = minimax(boardState,DEPTH,True)
            print(player,' played move:',val-N)
    elif 'alphabeta' in player:
        if not opponentFlag:
            hval,val = alphabeta(boardState,DEPTH,float('-inf'),float('inf'),False)
            print(player,' played move:',val+1)
        else:
            hval,val = alphabeta(boardState,DEPTH,float('-inf'),float('inf'),True)
            print(player,' played move:',val-N)
    return val

def startGame(player1, player2):
    haltGame = False
    p1 = player1.strip()
    p2 = player2.strip()
    emptyBoard = None
    boardState=Mancala(emptyBoard)
    boardState.printBoard(player1,player2)
    while not haltGame:
        move_again_p1 = True
        move_again_p2 = True
        #if boardState.game_over():
        #    break
        while move_again_p1:
            if boardState.game_over():
                haltGame = True
                break
            opponentFlag = False
            pit = get_next_move(p1, opponentFlag,boardState)
            move_again_p1 = boardState.playMove(pit)
            boardState.printBoard(player1,player2)
        while move_again_p2:
            if boardState.game_over():
                haltGame = True
                break
            opponentFlag = True
            pit = get_next_move(p2, opponentFlag,boardState)
            move_again_p2 = boardState.playMove(pit)
            boardState.printBoard(player1,player2)            
    declare_results(boardState, player1.strip(),player2.strip())

def validateInputs(argv):
    validInputs = ['random','human','minimax','alphabeta']
    if len(argv) != 2:
        print("Please enter exactly two valid input arguments")
        sys.exit()
    for args in argv:
        if args.lower() not in validInputs:
            print("Please enter valid input arguments like: ", validInputs)
            sys.exit()
    if argv[0].lower() == argv[1].lower():
        argv[0] = argv[0] + '_1'
        argv[1] = argv[1] + '_2'
    while len(argv[0]) < 11:
        argv[0] = argv[0] + ' '
    while len(argv[1]) < 11:
        argv[1] = argv[1] + ' '

    startGame(argv[0], argv[1])

if __name__ == "__main__":
    print('\nWelcome to the Mancala Game!\n')
    validateInputs(sys.argv[1:])
