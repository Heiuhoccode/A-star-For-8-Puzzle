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
# def Euclide()