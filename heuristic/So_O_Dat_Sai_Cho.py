def heuristic_so_o_sai_cho(current,goal):
    count = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if current[i][j] != goal[i][j] and current[i][j]!='*': count += 1
    return count

print("Nhập trạng thái ban đầu:")
Eight_Puzzle_Origin = []
for i in range(3):
    Eight_Puzzle_Origin.append(list(map(str,input().strip().split())))

print("Nhập trạng thái đích:")
Eight_Puzzle_Destination = []
for i in range(3):
    Eight_Puzzle_Destination.append(list(map(str,input().strip().split())))
# for i in Eight_Puzzle_Destination:
#     for j in i:
#         if j == '*':
#             print(end='  ')
#         else:
#             print(j, end=' ')
#     print()
