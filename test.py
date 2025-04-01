# g = số lấn vòng lặp
# h = hecristic
# f = g + h
# các trạng thái đều có h,g,f
# vòng lặp vô tận: điều kiện chọn là f nhỏ nhất, điều kiện dừng là h = 0
import process, heuristic



class Node:
    def __init__(self, matrix, h, g, f, pre, curr):
        self.matrix = matrix
        self.h = h
        self.g = g
        self.f = f
        self.pre = pre
        self.curr = curr

    def __str__(self):
        return f'{self.matrix} {self.h} {self.f}'


def output(node, Node_daduyet):
    temp = node
    while temp.curr != 0:
        print(temp)
        print()
        for i in Nodes_daduyet:
            if temp.pre == i.curr:
                temp = i
                break;


Nodes = []
print("Nhập trạng thái ban đầu:")
Eight_Puzzle_Origin = []
for i in range(3):
    Eight_Puzzle_Origin.append(list(map(str,input().strip().split())))


print("Nhập trạng thái đích:")
Eight_Puzzle_Destination = []
for i in range(3):
    Eight_Puzzle_Destination.append(list(map(str,input().strip().split())))
Eight_Puzzle_Current = Eight_Puzzle_Origin
# Node ban đầu
Node_bandau = Node(Eight_Puzzle_Origin, heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin,Eight_Puzzle_Destination), 0, heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin,Eight_Puzzle_Destination) + 0, 0, 0)
# phần tử 0 là ban đầu
Nodes.append(Node_bandau)

g=1 # Chi phí là 1
name_node = 1 # tên của node
closed_set = [] # Mảng xử lý nút lặp
Nodes_tapbien = [] # Mảng tập biên
Nodes_daduyet = [] # Mảng lưu các nút đã duyệt
Nodes_tapbien.append(Node_bandau)
while len(Nodes_tapbien) > 0:
    f_min = 1e9
    for node in Nodes_tapbien:
        if f_min > node.f: f_min = node.f
    Node_duyet = Node([[1, 2, 3], [4, 5, 6], [7, 8, 0]],0,0,0,0,0)
    for node in Nodes_tapbien:
        if node.f == f_min:
            Node_duyet = node
            break
    Nodes_tapbien.remove(Node_duyet)
    Nodes_daduyet.append(Node_duyet)
    # Nếu node được duyệt là nút đích thì in ra và dừng vòng lặp
    if Node_duyet.matrix == Eight_Puzzle_Destination:
        output(Node_duyet, Nodes_daduyet)
        break

    Nodes_kecan = []  # Mảng có node kề cận của node đang duyệt
    # Thêm vào mảng Node_kề cận các node kề với node đang duyệt
    for matrix in process.doivitri(Node_duyet.matrix):
        node_kecan = Node(matrix, heuristic.So_O_Dat_Sai_Cho(matrix, Node_duyet.matrix), g, Node_duyet.f - Node_duyet.h + g + heuristic.So_O_Dat_Sai_Cho(matrix, Node_duyet.matrix), Node_duyet.curr, name_node)
        name_node += 1
        Nodes_kecan.append(node_kecan)

    # Xử lý lặp
    for node_kecan in Nodes_kecan:
        for node in Nodes_tapbien:
            if node_kecan.matrix == node.matrix:
                if node_kecan.f < node.f:
                    Nodes_tapbien.remove(node)
    # Thêm vào tập biên
    for node_kecan in Nodes_kecan:
        Nodes_tapbien.append(node_kecan)
