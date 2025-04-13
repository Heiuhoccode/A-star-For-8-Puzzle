from collections import deque
from copy import deepcopy



def So_O_Dat_Sai_Cho(current,goal):
    count = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if current[i][j] != goal[i][j] and current[i][j]!='*': count += 1
    return count

def Khoang_Cach_Manhattan(current, goal):
    count = 0
    temp = [0,0,0,0,0,0,0,0]
    temp1 = [0,0,0,0,0,0,0,0]
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if goal[i][j] == '*': continue
            temp[int(goal[i][j])-1] = i
            temp1[int(goal[i][j])-1] = j
    for i in range(len(current)):
        for j in range(len(current[i])):
            if current[i][j] == '*': continue
            temp[int(current[i][j]) - 1] = abs(temp[int(current[i][j]) - 1] - i)
            temp1[int(current[i][j])-1] = abs(temp1[int(current[i][j])-1] - j)
    for i in range(len(temp)):
        count += temp[i] + temp1[i]
    return count

# Hàm heuristic Pattern Database
def SplitMatrix(matrix):
    matrix_A = []
    matrix_B = []
    for i in matrix:
        temp_A=[]
        temp_B=[]
        for j in i:
            if j=='1' or j=='4' or j=='2' or j=='3':
                temp_A.append(j)
                temp_B.append('*')
            elif j=='5' or j=='6' or j=='7' or j=='8':
                temp_B.append(j)
                temp_A.append('*')
            else:
                temp_A.append('*')
                temp_B.append('*')
        matrix_A.append(temp_A)
        matrix_B.append(temp_B)
    return matrix_A, matrix_B

def transform(blank_position,matrix):
    x,y = blank_position[0],blank_position[1]
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    for di, dj in directions:
        ni, nj = x + di, y + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            # Tạo bản sao của ma trận
            new_matrix = deepcopy(matrix)
            # Hoán đổi vị trí
            new_matrix[x][y], new_matrix[ni][nj] = new_matrix[ni][nj],new_matrix[x][y]
            neighbors.append(new_matrix)
    return neighbors

def build_pdb(matrix):
    visited = {}
    queue = deque()
    start = matrix
    queue.append((matrix,0))
    visited[tuple(map(tuple, matrix))]=0

    while queue:
        current, cost = queue.popleft()
        blanks = []
        for i in range(len(current)):
            for j in range(i + 1):
                if current[i][j] == '*':
                    blank_position = (i, j)
                    blanks.append(blank_position)

        for blank_position in blanks:
            for neighbor in transform(blank_position, current):
                if tuple(map(tuple, neighbor)) not in visited:
                    visited[tuple(map(tuple, neighbor))] = cost+1
                    queue.append((neighbor,cost+1))
    return visited

def PatternDatabase(current, goal):
    current_A, current_B = SplitMatrix(current)
    goal_A, goal_B = SplitMatrix(goal)

    heuristic_value = build_pdb(goal_B).get(tuple(map(tuple, current_B))) + build_pdb(goal_A).get(tuple(map(tuple, current_A)))
    # for i in goal_B:
    #     for j in i:
    #         print(j, end=' ')
    #     print()
    # print()
    # for i in current_B:
    #     for j in i:
    #         print(j, end=' ')
    #     print()
    # print(build_pdb(goal_A).get(tuple(map(tuple, current_A)), "not found"), len(build_pdb(goal_A)))
    # print(build_pdb(goal_B).get(tuple(map(tuple, current_B)),"not found"), len(build_pdb(goal_B)))
    #
    # for i in build_pdb(goal_B):
    #     print(i)
    return heuristic_value

# current = [['1', '2', '3'],['5', '*', '6'],['4', '7', '8']]
# goal = [['1','2','3'],['4','5','6'],['7','8','*']]
# PatternDatabase(current,goal)