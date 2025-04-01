# g = số lấn vòng lặp
# h = hecristic
# f = g + h
# các trạng thái đều có h,g,f
# vòng lặp vô tận: điều kiện chọn là f nhỏ nhất, điều kiện dừng là h = 0

print("Nhập trạng thái ban đầu:")
Eight_Puzzle_Origin = []
for i in range(3):
    Eight_Puzzle_Origin.append(list(map(str,input().strip().split())))

print("Nhập trạng thái đích:")
Eight_Puzzle_Destination = []
for i in range(3):
    Eight_Puzzle_Destination.append(list(map(str,input().strip().split())))
Eight_Puzzle_Current = Eight_Puzzle_Origin
i=0
while True:


