# g = số lấn vòng lặp
# h = hecristic
# f = g + h
# các trạng thái đều có h,g,f
# vòng lặp vô tận: điều kiện chọn là f nhỏ nhất, điều kiện dừng là h = 0
import process, heuristic, ngoaile

class Node:
    def __init__(self, matrix, h, g, f, pre, curr):
        self.matrix = matrix
        self.h = h
        self.g = g
        self.f = f
        self.pre = pre
        self.curr = curr

    def in_ma_tran(self, matrix):
        result = ""
        for i in matrix:
            for j in i:
                result += f"{j} "
            result += "\n"
        return result
    def __str__(self):
        return f'Ma trận {self.curr} là:{"\n"}{self.in_ma_tran(self.matrix)}h = {self.h} f = {self.f}'


def output(node, Nodes_daduyet):
    temp = node
    while temp.curr != 0:
        print(temp)
        print()
        for i in Nodes_daduyet:
            if temp.pre == i.curr:
                temp = i
                break


Nodes = []
# Nhập trạng thái đầu cuối và kiểu hàm Heuristic
print("Nhập trạng thái ban đầu:")
Eight_Puzzle_Origin = []
for i in range(3):
    Eight_Puzzle_Origin.append(list(map(str,input().strip().split())))
print("Nhập trạng thái đích:")
Eight_Puzzle_Destination = []
for i in range(3):
    Eight_Puzzle_Destination.append(list(map(str,input().strip().split())))

# Xét trường hợp không có lời giải
if ngoaile.khongthegiai(Eight_Puzzle_Origin,Eight_Puzzle_Destination):
    print(f'Thuật toán A* không thể giải trường hợp này do parity_origin != parity_goal: ({ngoaile.parity(Eight_Puzzle_Origin)}!={ngoaile.parity(Eight_Puzzle_Destination)})')
    exit()
else:
    print(f'Thuật toán A* giải được trường hợp này')

# Biến lựa chọn hàm Heuristic
print("Lựa chọn hàm Heuristic:")
print("1. Số ô đặt sai chỗ")
print("2. Khoảng cách Manhattan")
Option_Heuristic = int(input())

# Node ban đầu
Node_bandau = Node(Eight_Puzzle_Origin,0,0,0,0,0)
match Option_Heuristic:
    case 1:
        Node_bandau = Node(Eight_Puzzle_Origin, heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin, Eight_Puzzle_Destination), 0,
                           heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)
    case 2:
        Node_bandau = Node(Eight_Puzzle_Origin, heuristic.Khoang_Cach_Manhattan(Eight_Puzzle_Origin, Eight_Puzzle_Destination), 0,
                           heuristic.Khoang_Cach_Manhattan(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)
    case _:
        print("Lỗi chọn option")

g=1 # Chi phí là 1
name_node = 1 # tên của node
Nodes_tapbien = [] # Mảng tập biên
Nodes_daduyet = [] # Mảng lưu các nút đã duyệt

Nodes_tapbien.append(Node_bandau)
cothexuly = 0
while len(Nodes_tapbien) > 0:
    f_min = 1e9
    for node in Nodes_tapbien:
        if f_min > node.f: f_min = node.f
    Node_duyet = Node([[1, 2, 3], [4, 5, 6], [7, 8, 0]],0,0,0,0,0)
    for node in Nodes_tapbien:
        if node.f == f_min:
            Node_duyet = node
            break

    try:
        Nodes_tapbien.remove(Node_duyet)
    except:
        print("Lỗi xóa nút duyệt ra khoi tập biên")

    Nodes_daduyet.append(Node_duyet)
    # print(Node_duyet)
    # print("Độ dài tập biên = ", len(Nodes_tapbien))
    # print("Độ dài mảng node đã duyệt = ", len(Nodes_daduyet))
    # Nếu node được duyệt là nút đích thì in ra và dừng vòng lặp
    if Node_duyet.matrix == Eight_Puzzle_Destination:
        try:
            cothexuly = 1
            output(Node_duyet, Nodes_daduyet)
        except:
            print("Lỗi in ra")
        break

    Nodes_kecan = []  # Mảng có node kề cận của node đang duyệt
    # Thêm vào mảng Node_kề cận các node kề với node đang duyệt
    for matrix in process.doivitri(Node_duyet.matrix):
        node_kecan = Node(matrix, 0,0,0,0,0)
        match Option_Heuristic:
            case 1:
                node_kecan = Node(matrix, heuristic.So_O_Dat_Sai_Cho(matrix, Eight_Puzzle_Destination), g, Node_duyet.f - Node_duyet.h + g + heuristic.So_O_Dat_Sai_Cho(matrix, Eight_Puzzle_Destination), Node_duyet.curr, name_node)
            case 2:
                node_kecan = Node(matrix, heuristic.Khoang_Cach_Manhattan(matrix, Eight_Puzzle_Destination), g, Node_duyet.f - Node_duyet.h + g + heuristic.Khoang_Cach_Manhattan(matrix, Eight_Puzzle_Destination), Node_duyet.curr, name_node)
            case _:
                print("Lỗi chọn option")
        name_node += 1
        Nodes_kecan.append(node_kecan)

    # Xử lý lặp
    for node_kecan in Nodes_kecan:
        xoanode_kecan = False
        for node_tapbien in Nodes_tapbien:
            if node_kecan.matrix == node_tapbien.matrix:
                if node_kecan.f < node_tapbien.f:
                    try:
                        Nodes_tapbien.remove(node_tapbien)
                    except:
                        print("Lỗi xử lý lặp bên tập biên")
                else:
                    try:
                        Nodes_kecan.remove(node_kecan)
                        xoanode_kecan = True
                        break
                    except:
                        print("Lỗi xử lý lặp bên tập kề")
        if xoanode_kecan == False:
            for node_daduyet in Nodes_daduyet:
                if node_kecan.matrix == node_daduyet.matrix and node_kecan.f >= node_daduyet.f:
                    try:
                        Nodes_kecan.remove(node_kecan)
                        break
                    except:
                        print("Loi xu ly lap ben tap da duyet")
    # Thêm vào tập biên
    for node_kecan in Nodes_kecan:
        Nodes_tapbien.append(node_kecan)
if cothexuly == 0:
    match Option_Heuristic:
        case 1:
            print("Hàm heuristic Số ô đặt sai chỗ không thể xử lý")
        case 2:
            print("Hàm heuristic Manhattan không thể xử lý")
        case _:
            print("Lỗi chọn option")
