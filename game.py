import numpy as np
class Board:
    def __init__(self):
        self.first_player = "O"
        self.AI_player  = "X"
        self.board = np.array([
            ["0","1","2"],
            ["3","4","5"],
            ["6","7","8"]
        ])
        self.score = 0


    def draw_board(self):
        for row in self.board:
            print(" | ".join(str(cell) for cell in row))
            print("-" * 9)


    def fill_board(self,choosen_numbers):
        self.draw_board()
        self.is_x = True
        while True:
            try:
                o_player = int(input("Укажите номер внутри доски!.Вы ходите как 'O': "))
                if o_player < 0 or o_player >= 9:
                    raise ValueError
            except ValueError:
                print("Напишите цифру в диапазоне от 0 до 8 включительно! ")
                self.draw_board()
                continue
            
            if o_player in choosen_numbers:
                print("Выбранная ячейка уже занято!")
                continue
            
            choosen_numbers.append(o_player)
            indexY = np.where(self.board == str(o_player))[0]
            indexX = np.where(self.board == str(o_player))[1]
            self.board[indexY,indexX] = self.first_player
            self.draw_board()
            check_win = self.check_win(self.first_player)
            if check_win:
                self.running = False
                self.is_x = False
                print(f"Игрок {self.first_player} победил!")
            
            is_draw = self.check_draw(choosen_numbers)
            if is_draw and not check_win:
                self.running = False
                self.is_x = False
                print("Ничья!")
            
            break

        while self.is_x:
            bot_player = self.minimax(self.AI_player,self.board)
            x_player = bot_player['index']
            if x_player in choosen_numbers:
                print("Выбранная ячейка уже занято!")
                self.draw_board()
                continue
            
            
            choosen_numbers.append(x_player)
            indexY = np.where(self.board==str(x_player))[0]
            indexX = np.where(self.board==str(x_player))[1]
            self.board[indexY,indexX] = self.AI_player
            print(f'Игрок {self.AI_player} сделал ход! ')

            check_win = self.check_win(self.AI_player)
            if check_win:
                self.running = False
                self.is_x = False
                print(f"Игрок {self.AI_player} победил!")
            
            is_draw = self.check_draw(choosen_numbers)
            if is_draw and not check_win:
                self.running = False
                self.is_x = False
                print("Ничья!")
            break
    

    def check_win(self,player):
        win_combos = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
        for combo in win_combos:
            if all(self.board[y][x] == player for y,x in combo):
                return True
        return False
    
    def check_draw(self,cell):
        if len(cell)== 9:
            return True
        

    def emptySquares(self):
        empty_list = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c].isnumeric():
                    index = r * 3 + c
                    empty_list.append(index)
            
        return empty_list
    
    def index_to_coords(self,index):
        return divmod(index,3)

    def minimax(self,player,newBoard):
        availSpots = self.emptySquares()

        if self.check_win(self.first_player):
            return {"score":-10}
        elif self.check_win(self.AI_player):
            return {"score": +10}
        
        elif len(availSpots)== 0:
            return {"score":0}
        
        moves = []
        for i in range(len(availSpots)):
            move = {}
            move['index'] = availSpots[i]
            r,c = self.index_to_coords(availSpots[i])

            newBoard[r][c] = player

            if player == self.AI_player:
                result = self.minimax(self.first_player,newBoard)
                move["score"] = result["score"]
            else:
                result = self.minimax(self.AI_player,newBoard)
                move["score"] = result["score"]
            
            newBoard[r][c] = str(availSpots[i])
            moves.append(move)
        
        best_move = None
        if player == self.AI_player:
            best_move = max(moves,key=lambda m:m["score"])

        else:
            best_move = min(moves,key=lambda m:m["score"])
        
        return best_move

    def game(self):
        self.running = True
        choosen_numbers = []
        while self.running:
            self.fill_board(choosen_numbers)

game = Board()
game.game()
