from copy import deepcopy
def doivitri(Eight_Puzzle_Current):
    matrixs = []
    position_empty_x, position_empty_y= 0,0
    for i in range(len(Eight_Puzzle_Current)):
        for j in range(len(Eight_Puzzle_Current[i])):
            if Eight_Puzzle_Current[i][j] == 0:
                position_empty_x = i
                position_empty_y = j
                break

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    for di, dj in directions:
        ni, nj = position_empty_x + di, position_empty_y + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            # Tạo bản sao của ma trận
            new_matrix = deepcopy(Eight_Puzzle_Current)
            # Hoán đổi vị trí
            new_matrix[position_empty_x][position_empty_y], new_matrix[ni][nj] = new_matrix[ni][nj], new_matrix[position_empty_x][position_empty_y]
            matrixs.append(new_matrix)

    return matrixs