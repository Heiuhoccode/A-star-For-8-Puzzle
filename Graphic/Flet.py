import flet as ft
import random  # Để tạo dữ liệu ngẫu nhiên cho 8 ma trận


def main(page: ft.Page):
    page.title = "Nhập ma trận và hiển thị kết quả"

    # --- Trang nhập liệu ---
    def build_input_page():
        text_fields = []  # Lưu các TextField để lấy dữ liệu sau này
        for i in range(3):
            row = []
            for j in range(3):
                text_field = ft.TextField(
                    hint_text=f"{i},{j}",
                    width=50,
                    height=50,
                    text_align="center"
                )
                row.append(text_field)
            text_fields.append(row)
            page.add(ft.Row(row, alignment="center"))

        def submit_click(e):
            # Lấy giá trị từ các TextField
            input_matrix = []
            for row in text_fields:
                input_row = []
                for field in row:
                    input_row.append(field.value or "0")  # Nếu None thì gán "0"
                input_matrix.append(input_row)

            # Tạo 8 ma trận ngẫu nhiên (hoặc xử lý logic của bạn ở đây)
            matrices = [input_matrix]  # Ma trận đầu tiên là ma trận nhập vào
            for _ in range(7):
                random_matrix = [
                    [str(random.randint(0, 9)) for _ in range(3)]
                    for _ in range(3)
                ]
                matrices.append(random_matrix)

            # Chuyển sang trang hiển thị 8 ma trận
            show_matrices_page(matrices)

        submit_btn = ft.ElevatedButton("Submit", on_click=submit_click)
        page.add(ft.Row([submit_btn], alignment="center"))

    # --- Trang hiển thị 8 ma trận ---
    def show_matrices_page(matrices):
        page.views.clear()  # Xóa trang cũ

        # Tạo một ListView để cuộn nếu có nhiều ma trận
        matrices_view = ft.ListView(expand=True)

        for idx, matrix in enumerate(matrices, 1):
            matrices_view.controls.append(
                ft.Text(f"Ma trận {idx}:", weight="bold", size=16)
            )

            # Hiển thị từng hàng của ma trận
            for row in matrix:
                matrices_view.controls.append(
                    ft.Row(
                        [ft.Text(cell, width=50, height=50, text_align="center") for cell in row],
                        alignment="center"
                    )
                )
            matrices_view.controls.append(ft.Divider())  # Đường kẻ phân cách

        # Nút quay lại trang nhập liệu
        back_btn = ft.ElevatedButton(
            "Quay lại",
            on_click=lambda e: build_input_page()
        )

        page.add(
            ft.Column(
                [
                    ft.Text("8 Ma trận 3x3", size=20, weight="bold"),
                    matrices_view,
                    back_btn
                ],
                scroll="always"
            )
        )
        page.update()

    # Khởi tạo trang nhập liệu ban đầu
    build_input_page()


ft.app(target=main)