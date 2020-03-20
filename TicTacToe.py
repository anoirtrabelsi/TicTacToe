import pygame
pygame.init()

class Grid:

    def __init__(self):
        #empty board
        self.board = [['','',''], ['','',''], ['','','']]
        w, h = pygame.display.get_surface().get_size()
        self.s = w // 3

    def draw (self, window):
        #draw grid lines:
        s = self.s
        pygame.draw.line(window, (255,0,0), (s,0), (s,w), 5)
        pygame.draw.line(window, (255,0,0), (2*s,0), (2*s,w), 5)
        pygame.draw.line(window, (255,0,0), (0,s), (w,s), 5)
        pygame.draw.line(window, (255,0,0), (0,2*s), (w,2*s), 5)
        
        #draw current game state:
        for i in range (3):
            for j in range (3):
                if self.board[i][j] != '':
                    self.draw_move(window,i * 3 + j, self.board[i][j])
            
    
    def draw_move (self, window, cell_num, move):
        s = self.s

        if move == 'X':
            p = 50
            (x,y) = (cell_num % 3 * s, cell_num // 3 * s)
            pygame.draw.line(window, (0,0,255), (x+p,y+p), (x+s-p, y+s-p), 5)
            pygame.draw.line(window, (0,0,255), (x+s-p,y+p), (x+p, y+s-p), 5)

        elif move == 'O':
            (x,y) = (cell_num % 3 * s, cell_num // 3 * s)
            center = (x + s//2, y + s//2)
            pygame.draw.circle (window, (0,0,255), center, 50, 5)


class Game:
    # X always starts
    def __init__(self, grid, curr_player = 'X'):
        self.curr_player = curr_player
        self.board = grid.board


    def game_over(self):
        for i in range (3):
            for j in range (3):
                if self.board[i][j] == '':
                    return False
        return True


    #returns:
    #'X' if X has won
    #'O' if O has won
    #'Tie' if the game ended with a tie
    #None if the game isn't over yet

    def get_winner(self):
        b = self.board
        #rows:
        for i in range (3):
            if b[i][0] != '' and self.eq_3 (b[i][0], b[i][1], b[i][2]):
                return b[i][0]
        
        #cols:
        for i in range (3):
            if b[0][i] != '' and self.eq_3(b[0][i], b[1][i], b[2][i]):
                return b[0][i]

        #diagonals:
        if b[1][1] != '' and (self.eq_3 (b[0][0], b[1][1], b[2][2]) or self.eq_3(b[0][2], b[1][1], b[2][0])):
            return b[1][1]

        if self.game_over():
            return "Tie"

        return None

    # Implementation of the minimax algorithm
    # AI is player 'X' : Maximizer => Score = +10
    # Human is player 'O' : Minimize => Score = -10
    # For a tie, the function returns 0.

    def minimax(self, board, isMax):
        inf = float('inf')
        #Terminal states:
        result = self.get_winner()
        if result == 'X':
            return 10
        if result == 'O':
            return -10
        if result == 'Tie':
            return 0

        if isMax:
            best_score = -inf
            for i in range (3):
                for j in range (3):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        score = self.minimax(self.board, False)
                        self.board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score

        else:
            best_score = inf
            for i in range (3):
                for j in range (3):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        score = self.minimax(self.board, True)
                        self.board[i][j] = ''
                        best_score = min(score, best_score)

            return best_score


    # The AI starts the game and plays as 'X'
    def ai_move (self):
    
        best_score = float('-inf')
        move = (-1,-1)
        for i in range (3):
            for j in range (3):
                if self.board[i][j] == '':
                    self.board[i][j] = self.curr_player
                    score = self.minimax(self.board, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i,j)
                        if score == 10:
                            return move
                        
        return move
        

    def eq_3 (self,x,y,z):
        return x == y and y == z


#window dimensions:
w = 600
h = 600

window = pygame.display.set_mode((w,h))
window.fill((255,255,255))
pygame.display.set_caption("Tic Tac Toe")


grid = Grid()
game = Game(grid)

running = True
done = False

while running:
    mouse = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Turn of the AI:
    if game.curr_player == 'X':
        r,c = game.ai_move()
        game.board[r][c] = 'X'
        num_cell = r * 3 + c
        pygame.time.delay(100)
        grid.draw_move(window, num_cell, 'X')
        game.curr_player = 'O'
    
    elif mouse[0]:
        x,y = pygame.mouse.get_pos()
        (r,c) = (y//grid.s, x//grid.s)

        if grid.board[r][c] == '':

            cell_num = r*3 + c
            grid.draw_move(window, cell_num, game.curr_player)
            
            curr = game.curr_player
            grid.board[r][c] = curr
            if curr == 'X':
                game.curr_player = 'O'
            else:
                game.curr_player = 'X'

    grid.draw(window)
    pygame.display.update()
    

    result = game.get_winner()
    
    if result and not done:
        if result == 'Tie':
            print ("Tie!")
        else:
            print (result + " won!")
        done = True