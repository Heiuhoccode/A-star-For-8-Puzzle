# g = số lấn vòng lặp
# h = hecristic
# f = g + h
# các trạng thái đều có h,g,f
# vòng lặp vô tận: điều kiện chọn là f nhỏ nhất, điều kiện dừng là h = 0

from . import process,heuristic


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
        return f'Ma trận {self.curr} là:\n{self.in_ma_tran(self.matrix)}h = {self.h} f = {self.f}'
def output(node, Nodes_daduyet, doSau):
    result = []
    temp = node
    while temp.curr != 0:
        result.append(temp.matrix)
        doSau[0] += 1
        print()
        for i in Nodes_daduyet:
            if temp.pre == i.curr:
                temp = i
                break
    nodes_duocduyet = len(Nodes_daduyet)
    return result, node.f, nodes_duocduyet
doSau = [0]
Nodes = []

def a_star_search(origin, goal, heuristic_name):
    path = []
    chiphi = 0
    soNodeDaDuyet = 0
    Eight_Puzzle_Origin = origin
    Eight_Puzzle_Destination =goal
    # for i in origin:
    #     temp = []
    #     for j in i:
    #         temp.append(str(j))
    #     Eight_Puzzle_Origin.append(temp)
    # for i in goal:
    #     temp = []
    #     for j in i:
    #         temp.append(str(j))
    #     Eight_Puzzle_Destination.append(temp)
    Option_Heuristic = heuristic_name

    # Node ban đầu
    Node_bandau = Node(Eight_Puzzle_Origin,0,0,0,0,0)
    match Option_Heuristic:
        case "Misplaced":
            Node_bandau = Node(Eight_Puzzle_Origin, heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin, Eight_Puzzle_Destination), 0,
                               heuristic.So_O_Dat_Sai_Cho(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)
        case "Manhattan":
            Node_bandau = Node(Eight_Puzzle_Origin, heuristic.Khoang_Cach_Manhattan(Eight_Puzzle_Origin, Eight_Puzzle_Destination), 0,
                               heuristic.Khoang_Cach_Manhattan(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)
        case "Pattern DB":
            Node_bandau = Node(Eight_Puzzle_Origin, heuristic.PatternDatabase(Eight_Puzzle_Origin, Eight_Puzzle_Destination),0,
                               heuristic.PatternDatabase(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)
        case "Edge Match":
            Node_bandau = Node(Eight_Puzzle_Origin, heuristic.Edge_Matching_Heuristic(Eight_Puzzle_Origin, Eight_Puzzle_Destination), 0,
                               heuristic.Edge_Matching_Heuristic(Eight_Puzzle_Origin, Eight_Puzzle_Destination) + 0, 0, 0)

    g=1 # Chi phí là 1
    name_node = 1 # tên của node
    Nodes_tapbien = [] # Mảng tập biên
    Nodes_daduyet = [] # Mảng lưu các nút đã duyệt

    Nodes_tapbien.append(Node_bandau)
    cothexuly=0
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

        # Nếu node được duyệt là nút đích thì in ra và dừng vòng lặp
        if Node_duyet.matrix == Eight_Puzzle_Destination:
            try:
                cothexuly=1
                path, chiphi, soNodeDaDuyet = output(Node_duyet, Nodes_daduyet, doSau)
            except:
                print("Lỗi in ra")
            break

        Nodes_kecan = []  # Mảng có node kề cận của node đang duyệt
        # Thêm vào mảng Node_kề cận các node kề với node đang duyệt
        for matrix in process.doivitri(Node_duyet.matrix):
            node_kecan = Node(matrix, 0,0,0,0,0)
            match Option_Heuristic:
                case "Misplaced":
                    node_kecan = Node(matrix,
                                      heuristic.So_O_Dat_Sai_Cho(matrix, Eight_Puzzle_Destination), g,
                                      Node_duyet.f - Node_duyet.h + g + heuristic.So_O_Dat_Sai_Cho(matrix, Eight_Puzzle_Destination),
                                      Node_duyet.curr, name_node)
                case "Manhattan":
                    node_kecan = Node(matrix,
                                      heuristic.Khoang_Cach_Manhattan(matrix, Eight_Puzzle_Destination), g,
                                      Node_duyet.f - Node_duyet.h + g + heuristic.Khoang_Cach_Manhattan(matrix, Eight_Puzzle_Destination),
                                      Node_duyet.curr, name_node)
                case "Pattern DB":
                    node_kecan = Node(matrix,
                                      heuristic.PatternDatabase(matrix, Eight_Puzzle_Destination), g,
                                      Node_duyet.f - Node_duyet.h + g + heuristic.PatternDatabase(matrix,Eight_Puzzle_Destination),
                                      Node_duyet.curr, name_node)
                case "Edge Match":
                    node_kecan = Node(matrix,
                                      heuristic.Edge_Matching_Heuristic(matrix, Eight_Puzzle_Destination), g,
                                      Node_duyet.f - Node_duyet.h + g + heuristic.Edge_Matching_Heuristic(matrix,Eight_Puzzle_Destination),
                                      Node_duyet.curr, name_node)
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
            case "Misplaced":
                print("Hàm heuristic Số ô đặt sai chỗ không thể xử lý")
            case "Manhattan":
                print("Hàm heuristic Manhattan không thể xử lý")
            case "Pattern DB":
                print("Hàm heurisric Pattern DB không thể xử lý")
            case "Edge Match":
                print("Hàm heurisric Edge Match không thể xử lý")
            case _:
                print("Lỗi chọn option")
    return path, chiphi, soNodeDaDuyet

# origin = [[1,2,3],[4,5,6],[7,8,0]]
# goal = [[1,2,3],[4,5,6],[0,7,8]]
# for i in a_star_search(origin,goal,"Manhattan"):
#     print(i)