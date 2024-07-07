from board import Board
from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, player=1):
        super().__init__(player)
            
    def heuristic_utility(self, board):
        return self.heuristic_isolated_coins(board)+self.heuristic_remaining_coins(board)
    
    def heuristic_isolated_coins(self, board):
        isolated_coins = 0
        num_rows, num_cols = board.board_size
        for row in range(num_rows):
            for col in range(num_cols):
                if board.grid[row][col] == 0:
                    if col-1>0 & col+1<=num_cols:
                        if board.grid[row][col-1] == 0 & board.grid[row][col+1] == 0:
                            isolated_coins+=1
    
        if(isolated_coins % 2 ==0):
            return -1            
        else: 
            return 1

    def heuristic_remaining_coins(self, board):
        remaining_coins = 0
        num_rows, num_cols = board.board_size
        for row in range(num_rows):
            for col in range(num_cols):
                if board.grid[row][col] == 0:
                    remaining_coins+=1
        return remaining_coins
    
    def minimax_action(self, board):
        possible_actions = board.get_possible_actions()
        action = possible_actions
        return action

    def next_action(self, obs):
        DEPTH = 3
        playerr = self.player
        action, _ = self.minimax(board=obs, player=(playerr%2)+1, depth=DEPTH)
        if not action:
            possible_actions = obs.get_possible_actions()
            action = possible_actions[0]
        assert True, "is final"
        return action
    
    def minimax(self, board, player, depth):
        action= None
        if depth==0 or board.is_end(player):
            return action, self.heuristic_utility(board)
       
        #Maximaize self
        if player == self.player:
            best_action = None
            best_utility = float('-inf')
            for action in board.get_possible_actions():
                new_board = board.clone()
                new_board.play(action)
                utility, _ = self.minimax(new_board, (player%2)+1, depth=depth - 1)
                if utility > best_utility:
                    best_action = action
                    best_utility = utility
            return best_action, best_utility

        #Minimize other
        else:
            best_action = None
            best_utility = float('inf')
            for action in board.get_possible_actions():
                new_board = board.clone()
                new_board.play(action)
                utility, _ = self.minimax(new_board, (player%2)+1, depth=depth - 1)
                if utility < best_utility:
                    best_action = action
                    best_utility = utility
                return best_action, best_utility
        