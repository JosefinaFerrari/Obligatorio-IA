from board import Board
from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, player=1, depth=3):
        super().__init__(player)
        self.default_depth = depth
            
    def heuristic_utility(self, board):
        nim_sum = self.heuristic_nim_sum(board)
        remaining_coins = self.heuristic_remaining_coins(board)
        return -nim_sum
    
    def heuristic_nim_sum(self, board):
        nim_sum = 0
        for row in board.grid:
            nim_sum ^= sum(row)
        return nim_sum

    def heuristic_remaining_coins(self, board):
        remaining_coins = 0
        num_rows, num_cols = board.board_size
        for row in range(num_rows):
            for col in range(num_cols):
                if board.grid[row][col] == 0:
                    remaining_coins+=1
        return remaining_coins
    
    def next_action(self, obs):
        playerr = self.player
        action, _ = self.minimax(board=obs, player=(playerr % 2) + 1, depth=self.default_depth)
        if not action:
            heuristic_values = [self.heuristic_utility(obs) for a in obs.get_possible_actions()] 
            best_action_index = heuristic_values.index(max(heuristic_values))
            action = obs.get_possible_actions()[best_action_index]
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
        