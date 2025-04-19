import heapq
import numpy as np
from copy import deepcopy

class PuzzleNode:
    def __init__(self, state, parent=None, move="", depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.size = len(state)
        self.f = 0  # f = g + h
        self.g = 0  # cost from start to current node
        self.h = 0  # heuristic (Manhattan distance)

    def __lt__(self, other):
        return self.f < other.f

    def get_blank_position(self):
        """Find position of the blank (0)"""
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0:
                    return i, j
        return -1, -1

    def get_possible_moves(self):
        """Get all possible moves from current state"""
        moves = []
        row, col = self.get_blank_position()

        # Check all four directions
        if row > 0:
            moves.append("up")
        if row < self.size - 1:
            moves.append("down")
        if col > 0:
            moves.append("left")
        if col < self.size - 1:
            moves.append("right")
            
        return moves

    def get_new_state(self, move):
        """Apply move to state and return new state"""
        row, col = self.get_blank_position()
        new_state = deepcopy(self.state)
        
        if move == "up":
            new_state[row][col], new_state[row-1][col] = new_state[row-1][col], new_state[row][col]
        elif move == "down":
            new_state[row][col], new_state[row+1][col] = new_state[row+1][col], new_state[row][col]
        elif move == "left":
            new_state[row][col], new_state[row][col-1] = new_state[row][col-1], new_state[row][col]
        elif move == "right":
            new_state[row][col], new_state[row][col+1] = new_state[row][col+1], new_state[row][col]
            
        return new_state

    def calculate_manhattan_distance(self, goal):
        """Calculate Manhattan distance heuristic"""
        distance = 0
        size = self.size
        
        for i in range(size):
            for j in range(size):
                if self.state[i][j] != 0 and self.state[i][j] != goal[i][j]:
                    # Find where this tile should be in goal state
                    value = self.state[i][j]
                    for gi in range(size):
                        for gj in range(size):
                            if goal[gi][gj] == value:
                                distance += abs(i - gi) + abs(j - gj)
                                break
        return distance
    
    def calculate_euclidean_distance(self, goal):
        """Calculate Euclidean distance heuristic"""
        distance = 0
        size = self.size
        
        for i in range(size):
            for j in range(size):
                if self.state[i][j] != 0 and self.state[i][j] != goal[i][j]:
                    # Find where this tile should be in goal state
                    value = self.state[i][j]
                    for gi in range(size):
                        for gj in range(size):
                            if goal[gi][gj] == value:
                                distance += ((i - gi) ** 2 + (j - gj) ** 2) ** 0.5
                                break
        return distance
    
    def calculate_misplaced_tiles(self, goal):
        """Calculate misplaced tiles heuristic"""
        distance = 0
        size = self.size
        
        for i in range(size):
            for j in range(size):
                if self.state[i][j] != 0 and self.state[i][j] != goal[i][j]:
                    distance += 1
        return distance
        
    def calculate_f(self, goal, heuristic="manhattan"):
        """Calculate f value (f = g + h) using the specified heuristic"""
        self.g = self.depth  # g is the depth of the node
        
        if heuristic == "manhattan":
            self.h = self.calculate_manhattan_distance(goal)
        elif heuristic == "euclidean":
            self.h = self.calculate_euclidean_distance(goal)
        elif heuristic == "misplaced":
            self.h = self.calculate_misplaced_tiles(goal)
        else:
            self.h = self.calculate_manhattan_distance(goal)  # Default
            
        self.f = self.g + self.h
        return self.f

def state_to_tuple(state):
    """Convert a state to a tuple for hashability"""
    return tuple(tuple(row) for row in state)

def solve_puzzle(initial_state, goal_state, heuristic="manhattan"):
    """Solve the puzzle using A* algorithm with specified heuristic"""
    initial_node = PuzzleNode(initial_state)
    initial_node.calculate_f(goal_state, heuristic)
    
    # Priority queue for A*
    open_set = []
    heapq.heappush(open_set, initial_node)
    
    # Dictionary to keep track of visited states and their nodes in open set
    open_dict = {state_to_tuple(initial_state): initial_node}
    
    # Dictionary to keep track of processed states and their g values
    closed_dict = {}
    
    while open_set:
        current = heapq.heappop(open_set)
        current_state_tuple = state_to_tuple(current.state)
        
        # Remove from open_dict as we're processing it now
        if current_state_tuple in open_dict:
            del open_dict[current_state_tuple]
        
        # Check if we've reached the goal
        if current.state == goal_state:
            # Build path from start to goal
            path = []
            node = current
            while node:
                if node.move:
                    path.append((node.move, node.state))
                node = node.parent
            return list(reversed(path))
        
        # Add to closed dictionary with g value
        closed_dict[current_state_tuple] = current.g
        
        # Expand node
        for move in current.get_possible_moves():
            new_state = current.get_new_state(move)
            new_state_tuple = state_to_tuple(new_state)
            
            # Create new node
            child = PuzzleNode(new_state, current, move, current.depth + 1)
            child.calculate_f(goal_state, heuristic)
            
            # Check if this state is in closed_dict and if we found a better path
            if new_state_tuple in closed_dict:
                # If new path is better, remove from closed and consider again
                if child.g < closed_dict[new_state_tuple]:
                    # Đường đi mới tốt hơn, loại bỏ từ closed_dict
                    del closed_dict[new_state_tuple]
                else:
                    # Nếu không tìm thấy đường đi tốt hơn, bỏ qua
                    continue
            
            # Check if this state is already in the open set
            if new_state_tuple in open_dict:
                # If we found a better path to this state, update it
                existing_node = open_dict[new_state_tuple]
                if child.g < existing_node.g:  # So sánh g thay vì f
                    # Replace the old node with the new better one
                    existing_node.parent = current
                    existing_node.move = move
                    existing_node.depth = current.depth + 1
                    existing_node.g = child.g
                    existing_node.calculate_f(goal_state, heuristic)  # Tính lại f
                    # Reheapify
                    heapq.heapify(open_set)
            else:
                # Add to open set
                heapq.heappush(open_set, child)
                open_dict[new_state_tuple] = child
    
    # No solution found
    return []