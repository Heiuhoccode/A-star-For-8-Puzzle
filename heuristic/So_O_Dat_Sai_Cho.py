def heuristic_so_o_sai_cho(current,goal):
    count = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if current[i][j] != goal[i][j] and current[i][j]!='*': count += 1
    return count

