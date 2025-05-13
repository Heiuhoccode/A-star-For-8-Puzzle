# A* cho Bài Toán 8-Puzzle

## Giới thiệu

Dự án này triển khai thuật toán tìm kiếm A* để giải bài toán 8-puzzle. Bài toán 8-puzzle là một trò chơi trượt số kinh điển, bao gồm một lưới 3x3 với 8 ô số (từ 1 đến 8) và một ô trống. Mục tiêu là di chuyển các ô số bằng cách trượt chúng vào ô trống để đạt được trạng thái mục tiêu từ trạng thái ban đầu.

Thuật toán A* được sử dụng trong dự án này là một thuật toán tìm kiếm có thông tin (informed search), kết hợp chi phí thực tế (g) và hàm heuristic (h) để tìm đường đi ngắn nhất từ trạng thái ban đầu đến trạng thái mục tiêu. Dự án sử dụng hai hàm heuristic phổ biến:
- **Manhattan Distance**: Tổng khoảng cách dọc và ngang của mỗi ô số so với vị trí mục tiêu.
- **Misplaced Tiles**: Đếm số ô số không nằm đúng vị trí so với trạng thái mục tiêu.
- **Pattern Databae**: Chia thành các nhóm nhỏ.
- **Edge Matching**: Điểm thường
## Yêu cầu

- **Ngôn ngữ lập trình**: Python 3.6 trở lên

## Cài đặt

1. **Clone repository**:
   ```bash
   git clone https://github.com/Heiuhoccode/A-star-For-8-Puzzle.git
   cd A-star-For-8-Puzzle
   ```

2. **Kiểm tra Python**:
   Đảm bảo bạn đã cài đặt Python 3.6 hoặc cao hơn. Kiểm tra phiên bản Python:
   ```bash
   python --version
   ```

## Cách sử dụng

1. **Chạy chương trình**:
   Chương trình chính nằm trong file `main.py`. Để chạy chương trình, sử dụng lệnh:
   ```bash
   python main.py
   ```

2. **Nhập liệu**:
   - Chương trình sẽ yêu cầu bạn nhập trạng thái ban đầu và trạng thái mục tiêu của bài toán 8-puzzle.
   - Trạng thái là một lưới 3x3, được nhập dưới dạng 9 số (từ 0 đến 8, trong đó 0 biểu thị ô trống). Ví dụ:
     ```
     1 2 3
     8 0 4
     7 6 5
     ```
     Nhập lần lượt 9 số, cách nhau bởi dấu cách: `1 2 3 8 0 4 7 6 5`.

3. **Chọn hàm heuristic**:
   - Khi chạy chương trình, bạn có thể chọn sử dụng hàm heuristic:
     -  Manhattan Distance
     -  Misplaced Tiles
     -  Pattern Database
     -  Edge Matching

4. **Kết quả**:
   - Chương trình sẽ in ra:
     - Đường đi từ trạng thái ban đầu đến trạng thái mục tiêu.
     - Số bước di chuyển tối thiểu.
     - Tổng số nút được tạo ra trong quá trình tìm kiếm.
     - Nếu bài toán không có lời giải, chương trình sẽ thông báo: "Bài toán không thể giải được."

## Ví dụ

### Trạng thái ban đầu:
```
1 2 3
8 0 4
7 6 5
```

### Trạng thái mục tiêu:
```
1 2 3
4 5 6
7 8 0
```

### Chạy chương trình:
```bash
python main.py
```
Nhập trạng thái ban đầu: `1 2 3 8 0 4 7 6 5`
Nhập trạng thái mục tiêu: `1 2 3 4 5 6 7 8 0`
Chọn heuristic (1: Manhattan, 2: Misplaced): `1`

### Kết quả mẫu:
```
Đường đi:
Bước 1: 1 2 3
        8 0 4
        7 6 5
Bước 2: 1 2 3
        0 8 4
        7 6 5
...
Số bước: 20
Số nút được tạo: 1234
```

## Cấu trúc mã nguồn

- `main.py`: File chính chứa logic chạy chương trình và giao diện người dùng.
- `heuristics.py`: Chứa các hàm heuristic (Manhattan Distance, Misplaced Tiles, Pattern Database, Edge Matching).
- `setting.py`: Chứa các cấu hình cho giao diện.
- `sprite.py`: Chứa các lớp thành phần của giao diện (Button, Tile, Dropdown, Checkbox).

## Liên hệ

Nếu bạn có câu hỏi hoặc cần hỗ trợ, liên hệ qua email: [hieund12104@gmail.com] hoặc tạo một issue trên GitHub.