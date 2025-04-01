from copy import deepcopy
def doivitri(Eight_Puzzle_Current):
    Eight_Puzzle_New = []
    position_empty_x, position_empty_y= 0,0
    for i in Eight_Puzzle_Current:
        for j in Eight_Puzzle_Current[i]:
            if Eight_Puzzle_Current[i][j] == '*':
                position_empty_x = i
                position_empty_y = j
                break

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            # Tạo bản sao của ma trận
            new_matrix = deepcopy(Eight_Puzzle_Current)
            # Hoán đổi vị trí
            new_matrix[i][j], new_matrix[ni][nj] = new_matrix[ni][nj], new_matrix[i][j]
            Eight_Puzzle_New.append(new_matrix)

    return Eight_Puzzle_Current