
def parity(matrix):
    arr = []
    for i in matrix:
        for j in i:
            if j!=0: arr.append(j)
    songhichthe = 0
    for i in range(0,len(arr)-1):
        for j in  range(i+1, len(arr)):
            if arr[i] > arr[j]: songhichthe += 1
    if songhichthe %2 ==0:
        return "Chẵn"
    return "Lẻ"
def khongthegiai(origin, goal):
    parity_origin = parity(origin)
    parity_goal = parity(goal)
    if parity_origin != parity_goal:
        return True
    return False
