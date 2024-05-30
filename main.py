import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from database import init_db, SessionLocal
from controllers import *
from tkinter.scrolledtext import ScrolledText
from windows import set_dpi_awareness
from tkinter import messagebox
from datetime import datetime
class BangChuyen2:
    def __init__(self, id, ten_bang_chuyen, toc_do, suc_chua, tai_hien_tai=0,quy_trinh="",thu_tu=0):
        self.id = id
        self.ten_bang_chuyen = ten_bang_chuyen
        self.toc_do = toc_do
        self.suc_chua = suc_chua
        self.tai_hien_tai = tai_hien_tai
        self.quy_trinh = quy_trinh
        self.thu_tu = thu_tu
        self.running = False
        self.text_content = ""
        self.thread = None
        self.text_widget=None
        self.start_button = None
        self.stop_button = None
        self.edit_button = None
        self.delete_button = None
        self.name_entry = None
        self.speed_entry = None
        self.capacity_entry = None
        self.tai_hien_tai_label = None
        self.grid_info = {}

class GiaiDoan:
    def __init__(self, id, id_quy_trinh_san_xuat, id_bang_chuyen, so_nhan_cong_hien_tai, so_nhan_cong_nang_suat_lon_nhat, thoi_gian_xu_ly_toi_thieu, la_giai_doan_cuoi, thu_tu):
        self.id = id
        self.id_quy_trinh_san_xuat = id_quy_trinh_san_xuat
        self.id_bang_chuyen = id_bang_chuyen
        self.so_nhan_cong_hien_tai = so_nhan_cong_hien_tai
        self.so_nhan_cong_nang_suat_lon_nhat = so_nhan_cong_nang_suat_lon_nhat
        self.thoi_gian_xu_ly_toi_thieu = thoi_gian_xu_ly_toi_thieu
        self.la_giai_doan_cuoi = la_giai_doan_cuoi
        self.thu_tu = thu_tu
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý sản xuất")
        self.geometry("1200x600")
            # Khởi tạo cơ sở dữ liệu
        init_db()

        # Tạo session để tương tác với cơ sở dữ liệu
        self.db = SessionLocal()
        self.controller = BangChuyenController(self.db)
        self.giai_doan_controller = GiaiDoanSanXuatController(self.db)
        self.quy_trinh_controller = QuyTrinhSanXuatController(self.db)
        self.san_pham_controller = SanPhamController(self.db)
        self.don_hang_controller = DonHangController(self.db)
        self.don_hang_san_pham_controller = DonHangController(self.db)
        self.kho_controller = KhoController(self.db)
        self.kho_san_pham_controller = KhoSanPhamController(self.db)
        self.nhan_cong_controller = NhanCongController(self.db)
        # Tạo frame cho menu

        menu_frame = tk.Frame(self)
        menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Tạo các nút menu và dấu phân cách
        # Biến lưu trạng thái menu hiện tại
        self.current_menu = None

        # Tạo các nút menu và dấu phân cách
        menu_items = [
            ("Quản lý tiến trình", self.show_bang_chuyen_list),
            ("Quản lý giai đoạn sản xuất", self.show_giai_doan_list),
            ("Quản lý quy trình sản xuất", self.show_quy_trinh_list),
            ("Quản lý sản phẩm", self.show_san_pham_list),
            ("Quản lý đơn hàng", self.show_don_hang_list),
            ("Quản lý kho", self.show_kho_list),
            ("Quản lý nhân công", self.show_nhan_cong_list),
        ]

        # Số cột
        num_columns = len(menu_items)

        for i, (text, command) in enumerate(menu_items):
            button = tk.Button(menu_frame, text=text, command=lambda cmd=command: self.switch_menu(cmd), padx=10, pady=5)
            button.grid(row=0, column=i, sticky="ew")

        # Đặt tất cả các cột có trọng số bằng nhau để chia đều không gian
        for i in range(num_columns):
            menu_frame.grid_columnconfigure(i, weight=1)

        # Frame chính
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Biến để lưu trạng thái băng chuyền
        self.bang_chuyen_data = []
        self.previous_bang_chuyen_state = {}
        # Hiển thị trang chủ
        self.show_bang_chuyen_list()

    def switch_menu(self, new_menu):
        if self.current_menu == self.show_bang_chuyen_list:
            print("ok")
            self.save_bang_chuyen_state()  # Lưu trữ trạng thái trước khi chuyển menu
        self.current_menu = new_menu
        new_menu()
    def save_bang_chuyen_state(self):
        self.previous_bang_chuyen_state = {}
        for bc in self.bang_chuyen_data:
            try:
                print(bc.running)
                print(bc.text_widget.get("1.0", tk.END) if bc.text_widget else "")
                self.previous_bang_chuyen_state[bc.id] = {
                    'running': bc.running,
                    'text_content': bc.text_widget.get("1.0", tk.END) if bc.text_widget else "",
                    'tai_hien_tai': bc.tai_hien_tai,
                    'thread': bc.thread
                }
                
            except tk.TclError:
                # Nếu widget đã bị hủy, bỏ qua
                pass



    def show_bang_chuyen_list(self):
        self.clear_frame()

        # Tạo canvas và scrollbar cho toàn bộ nội dung
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Làm mới dữ liệu từ controller
        self.bang_chuyen_data = [
            BangChuyen2(bc.id, bc.ten_bang_chuyen, bc.toc_do, bc.suc_chua, bc.tai_hien_tai, bc.giai_doan.id_quy_trinh_san_xuat if bc.giai_doan else "Chưa rõ", bc.giai_doan.thu_tu if bc.giai_doan else "Chưa có")
            for bc in self.controller.get_bang_chuyen()
        ]

        # Tạo một từ điển để lưu trữ các băng chuyền theo quy trình
        quy_trinh_dict = {}
        for bang_chuyen in self.bang_chuyen_data:
            if bang_chuyen.quy_trinh not in quy_trinh_dict:
                quy_trinh_dict[bang_chuyen.quy_trinh] = []
            quy_trinh_dict[bang_chuyen.quy_trinh].append(bang_chuyen)

        # Tạo các khung cho từng quy trình
        for quy_trinh, bang_chuyens in quy_trinh_dict.items():
            frame = tk.LabelFrame(scrollable_frame, text=f"Quy trình {quy_trinh}", padx=10, pady=10)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Tạo tiêu đề cho các cột
            headers = ["Giai đoạn", "Tên băng chuyền", "Tốc độ (s/sp)", "Sức chứa", "Tải hiện tại", "Thông tin", "Điều khiển"]
            for col, header in enumerate(headers):
                label = ttk.Label(frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
                label.grid(row=0, column=col, sticky="e" if col == 6 else "w")

            # Thêm các băng chuyền vào scrollable_frame
            for row, bang_chuyen in enumerate(bang_chuyens, start=1):
                ttk.Label(frame, text=bang_chuyen.thu_tu, padding=(5, 5)).grid(row=row, column=0, sticky="w")
                name_label = ttk.Label(frame, text=bang_chuyen.ten_bang_chuyen, padding=(5, 5))
                name_label.grid(row=row, column=1, sticky="w")
                speed_label = ttk.Label(frame, text=bang_chuyen.toc_do, padding=(5, 5))
                speed_label.grid(row=row, column=2, sticky="w")
                capacity_label = ttk.Label(frame, text=bang_chuyen.suc_chua, padding=(5, 5))
                capacity_label.grid(row=row, column=3, sticky="w")
                tai_hien_tai_label = ttk.Label(frame, text=bang_chuyen.tai_hien_tai, padding=(5, 5))
                tai_hien_tai_label.grid(row=row, column=4, sticky="w")

                # Tạo vùng thông tin với Scrollbar
                text_frame = tk.Frame(frame)
                text_frame.grid(row=row, column=5, sticky="w")
                bang_chuyen.text_widget = ScrolledText(text_frame, height=5, width=60, wrap=tk.WORD)
                bang_chuyen.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                # Khôi phục nội dung text nếu có
                if bang_chuyen.id in self.previous_bang_chuyen_state:
                    bang_chuyen.text_widget.insert(tk.END, self.previous_bang_chuyen_state[bang_chuyen.id]['text_content'])

                # Tạo các nút điều khiển
                control_frame = tk.Frame(frame)
                control_frame.grid(row=row, column=6, sticky="e")

                start_button = tk.Button(control_frame, text="Bắt đầu hoạt động", command=lambda bc=bang_chuyen, tw=bang_chuyen.text_widget, lbl=tai_hien_tai_label: self.start_bang_chuyen(bc, tw, lbl))
                start_button.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

                stop_button = tk.Button(control_frame, text="Dừng", command=lambda bc=bang_chuyen: self.stop_bang_chuyen(bc))
                stop_button.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
                stop_button.config(state=tk.DISABLED)
                bang_chuyen.start_button = start_button
                bang_chuyen.stop_button = stop_button

                edit_button = tk.Button(control_frame, text="Chỉnh sửa")
                edit_button.config(command=lambda bc=bang_chuyen, nl=name_label, sl=speed_label, cl=capacity_label, el=edit_button: self.toggle_edit_mode(bc, nl, sl, cl, el))
                edit_button.grid(row=2, column=0, padx=5, pady=2, sticky="ew")
                delete_button = tk.Button(control_frame, text="Xóa", command=lambda bc=bang_chuyen: self.delete_bang_chuyen(bc))
                delete_button.grid(row=3, column=0, padx=5, pady=2, sticky="ew")

                bang_chuyen.edit_button = edit_button
                bang_chuyen.delete_button = delete_button
                bang_chuyen.tai_hien_tai_label = tai_hien_tai_label

                # Khôi phục trạng thái luồng nếu đang chạy
                if bang_chuyen.id in self.previous_bang_chuyen_state and self.previous_bang_chuyen_state[bang_chuyen.id]['running']:
                    bang_chuyen.running = True
                    bang_chuyen.thread = threading.Thread(target=self.simulate_bang_chuyen, args=(bang_chuyen, bang_chuyen.text_widget, tai_hien_tai_label))
                    bang_chuyen.thread.start()
                    start_button.config(state=tk.DISABLED)
                    stop_button.config(state=tk.NORMAL)



    # def show_bang_chuyen_list(self):
    #     self.clear_frame()

    #     # Tạo canvas và scrollbar cho toàn bộ nội dung
    #     canvas = tk.Canvas(self.main_frame)
    #     scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
    #     scrollable_frame = ttk.Frame(canvas)

    #     scrollable_frame.bind(
    #         "<Configure>",
    #         lambda e: canvas.configure(
    #             scrollregion=canvas.bbox("all")
    #         )
    #     )

    #     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #     canvas.configure(yscrollcommand=scrollbar.set)

    #     canvas.pack(side="left", fill="both", expand=True)
    #     scrollbar.pack(side="right", fill="y")


    #     if not self.bang_chuyen_data:
    #         self.bang_chuyen_data = [
    #             BangChuyen2(bc.id, bc.ten_bang_chuyen, bc.toc_do, bc.suc_chua, bc.tai_hien_tai, bc.giai_doan.id_quy_trinh_san_xuat if bc.giai_doan else "Chưa rõ",bc.giai_doan.thu_tu if bc.giai_doan else "Chưa có")
    #             for bc in self.controller.get_bang_chuyen()
    #         ]

    #     # Tạo một từ điển để lưu trữ các băng chuyền theo quy trình
    #     quy_trinh_dict = {}
    #     for bang_chuyen in self.bang_chuyen_data:
    #         if bang_chuyen.quy_trinh not in quy_trinh_dict:
    #             quy_trinh_dict[bang_chuyen.quy_trinh] = []
    #         quy_trinh_dict[bang_chuyen.quy_trinh].append(bang_chuyen)

    #     # Tạo các khung cho từng quy trình
    #     for quy_trinh, bang_chuyens in quy_trinh_dict.items():
    #         frame = tk.LabelFrame(scrollable_frame, text=f"Quy trình {quy_trinh}", padx=10, pady=10)
    #         frame.pack(fill="both", expand=True, padx=10, pady=10)



    #         # Tạo tiêu đề cho các cột
    #         headers = ["Giai đoạn", "Tên băng chuyền", "Tốc độ (s/sp)", "Sức chứa", "Tải hiện tại", "Thông tin", "Điều khiển"]
    #         for col, header in enumerate(headers):
    #             label = ttk.Label(frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
    #             label.grid(row=0, column=col, sticky= "e" if col == 6 else "w")

    #         # Thêm các băng chuyền vào scrollable_frame
    #         for row, bang_chuyen in enumerate(bang_chuyens, start=1):
    #             ttk.Label(frame, text=bang_chuyen.thu_tu, padding=(5, 5)).grid(row=row, column=0, sticky="w")
    #             name_label = ttk.Label(frame, text=bang_chuyen.ten_bang_chuyen, padding=(5, 5))
    #             name_label.grid(row=row, column=1, sticky="w")
    #             speed_label = ttk.Label(frame, text=bang_chuyen.toc_do, padding=(5, 5))
    #             speed_label.grid(row=row, column=2, sticky="w")
    #             capacity_label = ttk.Label(frame, text=bang_chuyen.suc_chua, padding=(5, 5))
    #             capacity_label.grid(row=row, column=3, sticky="w")
    #             tai_hien_tai_label = ttk.Label(frame, text=bang_chuyen.tai_hien_tai, padding=(5, 5))
    #             tai_hien_tai_label.grid(row=row, column=4, sticky="w")
    #             # Tạo vùng thông tin với Scrollbar
    #             text_frame = tk.Frame(frame)
    #             text_frame.grid(row=row, column=5, sticky="w")
    #             text_widget = ScrolledText(text_frame, height=5, width=60, wrap=tk.WORD)
    #             text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #             text_widget.insert(tk.END, bang_chuyen.text_content)  # Khôi phục nội dung text
    #             bang_chuyen.text_widget = text_widget   

    #             # Tạo các nút điều khiển
    #             control_frame = tk.Frame(frame)
    #             control_frame.grid(row=row, column=6, sticky="e")

    #             start_button = tk.Button(control_frame, text="Bắt đầu hoạt động", command=lambda bc=bang_chuyen, tw=text_widget, lbl=tai_hien_tai_label: self.start_bang_chuyen(bc, tw, lbl))
    #             start_button.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

    #             stop_button = tk.Button(control_frame, text="Dừng", command=lambda bc=bang_chuyen: self.stop_bang_chuyen(bc))
    #             stop_button.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    #             stop_button.config(state=tk.DISABLED)
    #             bang_chuyen.start_button = start_button
    #             bang_chuyen.stop_button = stop_button

    #             edit_button = tk.Button(control_frame, text="Chỉnh sửa")
    #             edit_button.config(command=lambda bc=bang_chuyen, nl=name_label, sl=speed_label, cl=capacity_label, el=edit_button: self.toggle_edit_mode(bc, nl, sl, cl, el))
    #             edit_button.grid(row=2, column=0, padx=5, pady=2, sticky="ew")
    #             delete_button = tk.Button(control_frame, text="Xóa", command=lambda bc=bang_chuyen: self.delete_bang_chuyen(bc))
    #             delete_button.grid(row=3, column=0, padx=5, pady=2, sticky="ew")

    #             bang_chuyen.edit_button = edit_button
    #             bang_chuyen.delete_button = delete_button
    #             bang_chuyen.tai_hien_tai_label = tai_hien_tai_label
    #             # Cập nhật lại thread nếu đang chạy
    #             if bang_chuyen.thread: 

    #                 bang_chuyen.thread = None
    #             try:
    #                 if bang_chuyen.running and not bang_chuyen.thread:
    #                     bang_chuyen.thread = threading.Thread(target=self.simulate_bang_chuyen, args=(bang_chuyen, text_widget, tai_hien_tai_label))
    #                     bang_chuyen.thread.start()
    #                     start_button.config(state=tk.DISABLED)
    #                     stop_button.config(state=tk.NORMAL)
    #             except Exception as e:  # Bắt tất cả các loại ngoại lệ
    #                 print(f"Đã xảy ra lỗi: {e}") 


    def start_bang_chuyen(self, bang_chuyen, text_widget, tai_hien_tai_label):
        bang_chuyen.running = True
        if not bang_chuyen.thread:
            bang_chuyen.thread = threading.Thread(target=self.simulate_bang_chuyen, args=(bang_chuyen, text_widget, tai_hien_tai_label))
            bang_chuyen.thread.start()
            self.update_buttons_state(bang_chuyen, True)

    def stop_bang_chuyen(self, bang_chuyen):
        bang_chuyen.running = False
        if bang_chuyen.thread:
            bang_chuyen.thread = None
        self.update_buttons_state(bang_chuyen, False)
    def simulate_bang_chuyen(self, bang_chuyen, text_widget, tai_hien_tai_label):
        san_pham_id = 1  # Giả sử ID sản phẩm là 1, bạn có thể thay đổi theo nhu cầu

        while bang_chuyen.running:
            time.sleep(bang_chuyen.toc_do)
            if bang_chuyen.tai_hien_tai < bang_chuyen.suc_chua:
                self.controller.them_san_pham(bang_chuyen.id, san_pham_id)
                bang_chuyen.tai_hien_tai += 1
                message = f"Thêm 1 sản phẩm lên băng chuyền (Tổng: {bang_chuyen.tai_hien_tai})"
            else:
                self.controller.dichuyen_san_pham(san_pham_id, bang_chuyen.id)
                bang_chuyen.tai_hien_tai -= 1
                message = "Di chuyển 1 sản phẩm khỏi băng chuyền"

                    # Cập nhật thông tin vào Text widget
            bang_chuyen.text_content += message + "\n"
            if bang_chuyen.text_widget and bang_chuyen.text_widget.winfo_exists():

                bang_chuyen.text_widget.insert(tk.END, message + "\n")
                bang_chuyen.text_widget.see(tk.END)
                if self.current_menu == None or self.current_menu == self.show_bang_chuyen_list:
                    tai_hien_tai_label.config(text=bang_chuyen.tai_hien_tai)
            

        # Khi dừng, xóa thread
        bang_chuyen.thread = None
    def update_buttons_state(self, bang_chuyen, is_running):
        if is_running:
            bang_chuyen.start_button.config(state=tk.DISABLED)
            bang_chuyen.stop_button.config(state=tk.NORMAL)
        else:
            bang_chuyen.start_button.config(state=tk.NORMAL)
            bang_chuyen.stop_button.config(state=tk.DISABLED)

    def toggle_edit_mode(self, bang_chuyen, name_label, speed_label, capacity_label, edit_button):
        if edit_button.cget("text") == "Chỉnh sửa":
            # Lưu thông tin lưới của các nhãn
            bang_chuyen.grid_info['name_label'] = name_label.grid_info()
            bang_chuyen.grid_info['speed_label'] = speed_label.grid_info()
            bang_chuyen.grid_info['capacity_label'] = capacity_label.grid_info()

            # Chuyển sang chế độ chỉnh sửa
            name_entry = tk.Entry(name_label.master)
            name_entry.insert(0, name_label.cget("text"))
            name_entry.grid(row=name_label.grid_info()["row"], column=name_label.grid_info()["column"], sticky="w")

            speed_entry = tk.Entry(speed_label.master)
            speed_entry.insert(0, speed_label.cget("text"))
            speed_entry.grid(row=speed_label.grid_info()["row"], column=speed_label.grid_info()["column"], sticky="w")

            capacity_entry = tk.Entry(capacity_label.master)
            capacity_entry.insert(0, capacity_label.cget("text"))
            capacity_entry.grid(row=capacity_label.grid_info()["row"], column=capacity_label.grid_info()["column"], sticky="w")

            bang_chuyen.name_entry = name_entry
            bang_chuyen.speed_entry = speed_entry
            bang_chuyen.capacity_entry = capacity_entry
            
            name_label.grid_forget()
            speed_label.grid_forget()
            capacity_label.grid_forget()

            edit_button.config(text="Xác nhận")
        else:
            # Lưu thay đổi và chuyển về chế độ hiển thị
            bang_chuyen.ten_bang_chuyen = bang_chuyen.name_entry.get()
            bang_chuyen.toc_do = int(bang_chuyen.speed_entry.get())
            bang_chuyen.suc_chua = int(bang_chuyen.capacity_entry.get())

            name_label.config(text=bang_chuyen.ten_bang_chuyen)
            speed_label.config(text=bang_chuyen.toc_do)
            capacity_label.config(text=bang_chuyen.suc_chua)
            self.controller.sua_bang_chuyen(bang_chuyen.id, bang_chuyen.ten_bang_chuyen,bang_chuyen.toc_do,bang_chuyen.suc_chua)
            bang_chuyen.name_entry.grid_forget()
            bang_chuyen.speed_entry.grid_forget()
            bang_chuyen.capacity_entry.grid_forget()

            name_label.grid(row=bang_chuyen.grid_info['name_label']["row"], column=bang_chuyen.grid_info['name_label']["column"], sticky="w")
            speed_label.grid(row=bang_chuyen.grid_info['speed_label']["row"], column=bang_chuyen.grid_info['speed_label']["column"], sticky="w")
            capacity_label.grid(row=bang_chuyen.grid_info['capacity_label']["row"], column=bang_chuyen.grid_info['capacity_label']["column"], sticky="w")

            edit_button.config(text="Chỉnh sửa")


    def delete_bang_chuyen(self, bang_chuyen):
        response = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa băng chuyền này?")
        if response:
            self.bang_chuyen_data.remove(bang_chuyen)
            self.show_bang_chuyen_list()
    
    def show_giai_doan_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        giai_doan_data = self.giai_doan_controller.get_giai_doan()

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["ID", "Tên quy trình", "ID băng chuyền", "Số nhân công hiện tại", "Số nhân công max năng suất", "Thời gian xử lý tối thiểu/sp", "Là giai đoạn cuối?", "Thứ tự giai đoạn", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="nsew")

        # Thêm các giai đoạn vào scrollable_frame
        for row, giai_doan in enumerate(giai_doan_data, start=1):
            ttk.Label(scrollable_frame, text=giai_doan.id, padding=(5, 5)).grid(row=row*2-1, column=0, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.id_quy_trinh_san_xuat, padding=(5, 5)).grid(row=row*2-1, column=1, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.id_bang_chuyen, padding=(5, 5)).grid(row=row*2-1, column=2, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.so_nhan_cong_hien_tai, padding=(5, 5)).grid(row=row*2-1, column=3, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.so_nhan_cong_nang_suat_lon_nhat, padding=(5, 5)).grid(row=row*2-1, column=4, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.thoi_gian_xu_ly_toi_thieu, padding=(5, 5)).grid(row=row*2-1, column=5, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.la_giai_doan_cuoi, padding=(5, 5)).grid(row=row*2-1, column=6, sticky="nsew")
            ttk.Label(scrollable_frame, text=giai_doan.thu_tu, padding=(5, 5)).grid(row=row*2-1, column=7, sticky="nsew")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row*2-1, column=8, sticky="e")

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda gd=giai_doan: self.edit_giai_doan(gd))
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda gd=giai_doan: self.delete_giai_doan(gd))
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

            # Thêm thanh ngang để ngăn cách giữa các dòng
            separator = ttk.Separator(scrollable_frame, orient='horizontal')
            separator.grid(row=row*2, column=0, columnspan=9, sticky='ew', pady=5)

        # canvas.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")
        add_button = tk.Button(self.main_frame, text="Thêm giai đoạn", command=self.add_giai_doan, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    def add_giai_doan(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm giai đoạn sản xuất")

        # Lấy danh sách các băng chuyền trống và quy trình sản xuất
        bang_chuyen_trong = self.db.query(BangChuyen).filter(~self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_bang_chuyen == BangChuyen.id).exists()).all()
        quy_trinh_list = self.db.query(QuyTrinhSanXuat).all()

        fields = [
            ("ID quy trình", None),
            ("ID băng chuyền", None),
            ("Số nhân công hiện tại", ""),
            ("Số nhân công năng suất lớn nhất", ""),
            ("Thời gian xử lý tối thiểu", ""),
            ("Là giai đoạn cuối?", ""),
            ("Thứ tự giai đoạn", "")
        ]

        entries = {}
        for idx, (label_text, value) in enumerate(fields):
            label = ttk.Label(add_window, text=label_text)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            if label_text in ["ID quy trình", "ID băng chuyền"]:
                combobox = ttk.Combobox(add_window)
                if label_text == "ID quy trình":
                    combobox['values'] = [qt.id for qt in quy_trinh_list]
                else:
                    combobox['values'] = [bc.id for bc in bang_chuyen_trong]
                combobox.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
                entries[label_text] = combobox
            else:
                entry = ttk.Entry(add_window)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
                entry.insert(0, value)
                entries[label_text] = entry

        def save_new_giai_doan():
            try:
                id_quy_trinh_san_xuat = int(entries["ID quy trình"].get())
                id_bang_chuyen = int(entries["ID băng chuyền"].get())
                so_nhan_cong_hien_tai = int(entries["Số nhân công hiện tại"].get())
                so_nhan_cong_nang_suat_lon_nhat = int(entries["Số nhân công năng suất lớn nhất"].get())
                thoi_gian_xu_ly_toi_thieu = float(entries["Thời gian xử lý tối thiểu"].get())
                la_giai_doan_cuoi = entries["Là giai đoạn cuối?"].get().lower() in ['true', '1', 'yes', 'y']
                thu_tu = int(entries["Thứ tự giai đoạn"].get())

                new_giai_doan = GiaiDoanSanXuat(
                    id_quy_trinh_san_xuat=id_quy_trinh_san_xuat,
                    id_bang_chuyen=id_bang_chuyen,
                    so_nhan_cong_hien_tai=so_nhan_cong_hien_tai,
                    so_nhan_cong_nang_suat_lon_nhat=so_nhan_cong_nang_suat_lon_nhat,
                    thoi_gian_xu_ly_toi_thieu=thoi_gian_xu_ly_toi_thieu,
                    la_giai_doan_cuoi=la_giai_doan_cuoi,
                    thu_tu=thu_tu
                )

                self.giai_doan_controller.them_giai_doan_san_xuat(id_quy_trinh_san_xuat,id_bang_chuyen,so_nhan_cong_hien_tai,so_nhan_cong_nang_suat_lon_nhat,thoi_gian_xu_ly_toi_thieu,la_giai_doan_cuoi,thu_tu)
                self.db.commit()

                # Cập nhật số lượng giai đoạn của quy trình tương ứng
                quy_trinh = self.db.query(QuyTrinhSanXuat).filter(QuyTrinhSanXuat.id == id_quy_trinh_san_xuat).first()
                if quy_trinh:
                    quy_trinh.so_giai_doan += 1
                    self.db.commit()

                messagebox.showinfo("Thành công", "Đã thêm giai đoạn sản xuất thành công!")
                add_window.destroy()
                self.show_giai_doan_list()
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")

        save_button = ttk.Button(add_window, text="Xác nhận", command=save_new_giai_doan)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)


    def edit_giai_doan(self, giai_doan):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa giai đoạn sản xuất")

        fields = [
            ("ID quy trình", giai_doan.id_quy_trinh_san_xuat),
            ("ID băng chuyền", giai_doan.id_bang_chuyen),
            ("Số nhân công năng suất lớn nhất", giai_doan.so_nhan_cong_nang_suat_lon_nhat),
            ("Thời gian xử lý tối thiểu", giai_doan.thoi_gian_xu_ly_toi_thieu),
            ("Là giai đoạn cuối?", giai_doan.la_giai_doan_cuoi),
            ("Thứ tự giai đoạn", giai_doan.thu_tu)
        ]

        entries = {}
        for idx, (label_text, value) in enumerate(fields):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(edit_window)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(0, value)
            entries[label_text] = entry

        # Hiển thị số nhân công hiện tại nhưng không cho phép chỉnh sửa
        ttk.Label(edit_window, text="Số nhân công hiện tại").grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")
        ttk.Label(edit_window, text=giai_doan.so_nhan_cong_hien_tai).grid(row=len(fields), column=1, padx=10, pady=5, sticky="ew")

        def save_changes():
            try:
                id_quy_trinh_san_xuat = int(entries["ID quy trình"].get())
                id_bang_chuyen = int(entries["ID băng chuyền"].get())
                so_nhan_cong_nang_suat_lon_nhat = int(entries["Số nhân công năng suất lớn nhất"].get())
                thoi_gian_xu_ly_toi_thieu = float(entries["Thời gian xử lý tối thiểu"].get())
                la_giai_doan_cuoi = entries["Là giai đoạn cuối?"].get().lower() in ['true', '1', 'yes', 'y']
                thu_tu = int(entries["Thứ tự giai đoạn"].get())

                self.giai_doan_controller.sua_giai_doan_san_xuat(
                    giai_doan.id,
                    id_quytrinh=id_quy_trinh_san_xuat,
                    id_bang_chuyen=id_bang_chuyen,
                    so_nhan_cong_nang_suat_lon_nhat=so_nhan_cong_nang_suat_lon_nhat,
                    thoi_gian_xu_ly_toi_thieu=thoi_gian_xu_ly_toi_thieu,
                    la_giai_doan_cuoi=la_giai_doan_cuoi,
                    thu_tu=thu_tu
                )

                messagebox.showinfo("Thành công", "Đã cập nhật giai đoạn sản xuất thành công!")
                edit_window.destroy()
                self.show_giai_doan_list()
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")

        save_button = ttk.Button(edit_window, text="Xác nhận", command=save_changes)
        save_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)



    def delete_giai_doan(self, giai_doan):
        response = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giai đoạn này?")
        if response:
            self.giai_doan_controller.xoa_giai_doan_san_xuat(giai_doan.id)
            self.show_giai_doan_list()

    def show_quy_trinh_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        quy_trinh_data = self.quy_trinh_controller.get_quy_trinh_san_xuat()

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["ID", "Tên quy trình sản xuất", "Số giai đoạn", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="w")

        # Thêm các quy trình sản xuất vào scrollable_frame
        for row, quy_trinh in enumerate(quy_trinh_data, start=1):
            ttk.Label(scrollable_frame, text=quy_trinh.id, padding=(5, 5)).grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=quy_trinh.ten_quy_trinh_san_xuat, padding=(5, 5)).grid(row=row, column=1, sticky="w")
            ttk.Label(scrollable_frame, text=quy_trinh.so_giai_doan, padding=(5, 5)).grid(row=row, column=2, sticky="w")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row, column=3, sticky="w")

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda qt=quy_trinh: self.edit_quy_trinh(qt))
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda qt=quy_trinh: self.delete_quy_trinh(qt))
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

        # Thêm nút "Thêm quy trình sản xuất" ở phía dưới giữa khung
        add_button = tk.Button(self.main_frame, text="Thêm quy trình sản xuất", command=self.add_quy_trinh, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


    def add_quy_trinh(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm quy trình sản xuất")

        ttk.Label(add_window, text="Tên quy trình sản xuất").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_quy_trinh_entry = ttk.Entry(add_window)
        ten_quy_trinh_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        def save_new_quy_trinh():
            ten_quy_trinh = ten_quy_trinh_entry.get()
            if ten_quy_trinh:
                new_quy_trinh = QuyTrinhSanXuat(ten_quy_trinh_san_xuat=ten_quy_trinh, so_giai_doan=0)
                self.db.add(new_quy_trinh)
                self.db.commit()
                messagebox.showinfo("Thành công", "Đã thêm quy trình sản xuất thành công!")
                add_window.destroy()
                self.show_quy_trinh_list()
            else:
                messagebox.showerror("Lỗi", "Tên quy trình sản xuất không được để trống.")

        save_button = ttk.Button(add_window, text="Xác nhận", command=save_new_quy_trinh)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def edit_quy_trinh(self, quy_trinh):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa quy trình sản xuất")

        ttk.Label(edit_window, text="Tên quy trình sản xuất").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_quy_trinh_entry = ttk.Entry(edit_window)
        ten_quy_trinh_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ten_quy_trinh_entry.insert(0, quy_trinh.ten_quy_trinh_san_xuat)

        def save_edited_quy_trinh():
            ten_quy_trinh = ten_quy_trinh_entry.get()
            if ten_quy_trinh:
                quy_trinh.ten_quy_trinh_san_xuat = ten_quy_trinh
                self.db.commit()
                messagebox.showinfo("Thành công", "Đã chỉnh sửa quy trình sản xuất thành công!")
                edit_window.destroy()
                self.show_quy_trinh_list()
            else:
                messagebox.showerror("Lỗi", "Tên quy trình sản xuất không được để trống.")

        save_button = ttk.Button(edit_window, text="Xác nhận", command=save_edited_quy_trinh)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def delete_quy_trinh(self, quy_trinh):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa quy trình sản xuất này?")
        if confirm:
            # Xóa các giai đoạn thuộc quy trình
            self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh.id).delete()
            self.db.query(SanPham).filter(SanPham.id_quy_trinh_san_xuat == quy_trinh.id).delete()
            # Xóa quy trình sản xuất
            self.db.delete(quy_trinh)
            self.db.commit()
            messagebox.showinfo("Thành công", "Đã xóa quy trình sản xuất thành công!")
            self.show_quy_trinh_list()


    def show_san_pham_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        san_pham_data = self.san_pham_controller.get_san_pham()

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["ID", "Tên nhóm sản phẩm", "Số sản phẩm đang xử lý", "ID Quy trình sản xuất", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="w")

        # Thêm các sản phẩm vào scrollable_frame
        for row, san_pham in enumerate(san_pham_data, start=1):
            ttk.Label(scrollable_frame, text=san_pham.id, padding=(5, 5)).grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=san_pham.ten_san_pham, padding=(5, 5)).grid(row=row, column=1, sticky="w")
            ttk.Label(scrollable_frame, text=san_pham.san_pham_dang_xu_ly, padding=(5, 5)).grid(row=row, column=2, sticky="w")
            ttk.Label(scrollable_frame, text=san_pham.id_quy_trinh_san_xuat, padding=(5, 5)).grid(row=row, column=3, sticky="w")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row, column=4, sticky="w")

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda sp=san_pham: self.edit_san_pham(sp))
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda sp=san_pham: self.delete_san_pham(sp))
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

        # Thêm nút "Thêm sản phẩm" ở phía dưới giữa khung
        add_button = tk.Button(self.main_frame, text="Thêm sản phẩm", command=self.add_san_pham, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_san_pham(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm sản phẩm")

        ttk.Label(add_window, text="Tên sản phẩm").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_san_pham_entry = ttk.Entry(add_window)
        ten_san_pham_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="ID Quy trình sản xuất").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        id_quy_trinh_entry = ttk.Entry(add_window)
        id_quy_trinh_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        def save_new_san_pham():
            ten_san_pham = ten_san_pham_entry.get()
            id_quy_trinh = id_quy_trinh_entry.get()
            if ten_san_pham and id_quy_trinh:
                self.san_pham_controller.them_san_pham(ten_san_pham, id_quy_trinh)
                messagebox.showinfo("Thành công", "Đã thêm sản phẩm thành công!")
                add_window.destroy()
                self.show_san_pham_list()
            else:
                messagebox.showerror("Lỗi", "Tên sản phẩm và ID quy trình sản xuất không được để trống.")

        save_button = ttk.Button(add_window, text="Xác nhận", command=save_new_san_pham)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def edit_san_pham(self, san_pham):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa sản phẩm")

        ttk.Label(edit_window, text="Tên sản phẩm").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_san_pham_entry = ttk.Entry(edit_window)
        ten_san_pham_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ten_san_pham_entry.insert(0, san_pham.ten_san_pham)

        ttk.Label(edit_window, text="ID Quy trình sản xuất").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        id_quy_trinh_entry = ttk.Entry(edit_window)
        id_quy_trinh_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        id_quy_trinh_entry.insert(0, san_pham.id_quy_trinh_san_xuat)

        def save_edited_san_pham():
            ten_san_pham = ten_san_pham_entry.get()
            id_quy_trinh = id_quy_trinh_entry.get()
            if ten_san_pham and id_quy_trinh:
                self.san_pham_controller.sua_san_pham(san_pham.id, ten_san_pham=ten_san_pham, id_quy_trinh_san_xuat=id_quy_trinh)
                messagebox.showinfo("Thành công", "Đã chỉnh sửa sản phẩm thành công!")
                edit_window.destroy()
                self.show_san_pham_list()
            else:
                messagebox.showerror("Lỗi", "Tên sản phẩm và ID quy trình sản xuất không được để trống.")

        save_button = ttk.Button(edit_window, text="Xác nhận", command=save_edited_san_pham)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def delete_san_pham(self, san_pham):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?")
        if confirm:
            self.san_pham_controller.xoa_san_pham(san_pham.id)
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm thành công!")
            self.show_san_pham_list()

    def show_don_hang_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        don_hang_data = self.don_hang_controller.get_don_hang()

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["ID", "Tên đơn hàng", "Tên khách hàng", "Thời gian yêu cầu hoàn thành", "Sản phẩm", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="w")

        # Thêm các đơn hàng vào scrollable_frame
        for row, don_hang in enumerate(don_hang_data, start=1):
            ttk.Label(scrollable_frame, text=don_hang.id, padding=(5, 5)).grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=don_hang.ten_don_hang, padding=(5, 5)).grid(row=row, column=1, sticky="w")
            ttk.Label(scrollable_frame, text=don_hang.ten_khach_hang, padding=(5, 5)).grid(row=row, column=2, sticky="w")
            ttk.Label(scrollable_frame, text=don_hang.thoi_gian_yeu_cau_hoan_thanh, padding=(5, 5)).grid(row=row, column=3, sticky="w")

            san_pham_text = "\n".join([f"{sp.san_pham.ten_san_pham} (x{sp.so_luong})" for sp in don_hang.don_hang_san_pham])
            ttk.Label(scrollable_frame, text=san_pham_text, padding=(5, 5)).grid(row=row, column=4, sticky="w")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row, column=5, sticky="w")

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda dh=don_hang: self.edit_don_hang(dh))
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda dh=don_hang: self.delete_don_hang(dh))
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

        # Thêm nút "Thêm đơn hàng" ở phía dưới giữa khung
        add_button = tk.Button(self.main_frame, text="Thêm đơn hàng", command=self.add_don_hang, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")




    def add_don_hang(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm đơn hàng")

        ttk.Label(add_window, text="Tên đơn hàng").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_don_hang_entry = ttk.Entry(add_window)
        ten_don_hang_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="Tên khách hàng").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ten_khach_hang_entry = ttk.Entry(add_window)
        ten_khach_hang_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="Thời gian yêu cầu hoàn thành").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        thoi_gian_entry = ttk.Entry(add_window)
        thoi_gian_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="Sản phẩm và số lượng").grid(row=3, column=0, padx=10, pady=5, sticky="w")

        san_pham_frame = ttk.Frame(add_window)
        san_pham_frame.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Lấy danh sách sản phẩm từ controller và thêm vào frame
        san_pham_data = self.san_pham_controller.get_san_pham()
        san_pham_entries = []
        for sp in san_pham_data:
            sp_label = ttk.Label(san_pham_frame, text=f"{sp.id} - {sp.ten_san_pham}")
            sp_label.pack(side=tk.TOP, anchor="w")
            sp_entry = ttk.Entry(san_pham_frame)
            sp_entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
            san_pham_entries.append((sp.id, sp_entry))

        def save_new_don_hang():
            ten_don_hang = ten_don_hang_entry.get()
            ten_khach_hang = ten_khach_hang_entry.get()
            thoi_gian = thoi_gian_entry.get()
            selected_san_pham = [(sp_id, int(sp_entry.get())) for sp_id, sp_entry in san_pham_entries if sp_entry.get().isdigit()]

            if ten_don_hang and ten_khach_hang and thoi_gian and selected_san_pham:
                self.don_hang_controller.them_don_hang(ten_don_hang, ten_khach_hang, thoi_gian, selected_san_pham)
                messagebox.showinfo("Thành công", "Đã thêm đơn hàng thành công!")
                add_window.destroy()
                self.show_don_hang_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và số lượng sản phẩm hợp lệ.")

        save_button = ttk.Button(add_window, text="Xác nhận", command=save_new_don_hang)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)


    def edit_don_hang(self, don_hang):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa đơn hàng")

        ttk.Label(edit_window, text="Tên đơn hàng").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_don_hang_entry = ttk.Entry(edit_window)
        ten_don_hang_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ten_don_hang_entry.insert(0, don_hang.ten_don_hang)

        ttk.Label(edit_window, text="Tên khách hàng").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ten_khach_hang_entry = ttk.Entry(edit_window)
        ten_khach_hang_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ten_khach_hang_entry.insert(0, don_hang.ten_khach_hang)

        ttk.Label(edit_window, text="Thời gian yêu cầu hoàn thành").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        thoi_gian_entry = ttk.Entry(edit_window)
        thoi_gian_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        thoi_gian_entry.insert(0, don_hang.thoi_gian_yeu_cau_hoan_thanh)

        ttk.Label(edit_window, text="Sản phẩm và số lượng").grid(row=3, column=0, padx=10, pady=5, sticky="w")

        san_pham_frame = ttk.Frame(edit_window)
        san_pham_frame.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Lấy danh sách sản phẩm từ controller và thêm vào frame
        san_pham_data = self.san_pham_controller.get_san_pham()
        san_pham_entries = []
        for sp in san_pham_data:
            sp_label = ttk.Label(san_pham_frame, text=f"{sp.id} - {sp.ten_san_pham}")
            sp_label.pack(side=tk.TOP, anchor="w")
            sp_entry = ttk.Entry(san_pham_frame)
            sp_entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
            # Kiểm tra nếu sản phẩm đã có trong đơn hàng thì điền số lượng hiện tại
            existing_sp = next((dsp for dsp in don_hang.don_hang_san_pham if dsp.id_san_pham == sp.id), None)
            if existing_sp:
                sp_entry.insert(0, existing_sp.so_luong)
            san_pham_entries.append((sp.id, sp_entry))

        def save_edited_don_hang():
            ten_don_hang = ten_don_hang_entry.get()
            ten_khach_hang = ten_khach_hang_entry.get()
            thoi_gian = thoi_gian_entry.get()
            selected_san_pham = [(sp_id, int(sp_entry.get())) for sp_id, sp_entry in san_pham_entries if sp_entry.get().isdigit()]

            if ten_don_hang and ten_khach_hang and thoi_gian and selected_san_pham:
                self.don_hang_controller.sua_don_hang(don_hang.id, ten_don_hang, ten_khach_hang, thoi_gian, selected_san_pham)
                messagebox.showinfo("Thành công", "Đã chỉnh sửa đơn hàng thành công!")
                edit_window.destroy()
                self.show_don_hang_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và số lượng sản phẩm hợp lệ.")

        save_button = ttk.Button(edit_window, text="Xác nhận", command=save_edited_don_hang)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)


    def delete_don_hang(self, don_hang):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa đơn hàng này?")
        if confirm:
            self.don_hang_controller.xoa_don_hang(don_hang.id)
            messagebox.showinfo("Thành công", "Đã xóa đơn hàng thành công!")
            self.show_don_hang_list()



    def show_kho_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        kho_data = self.kho_controller.get_kho()

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["ID", "Tên kho", "Dung tích", "Sản phẩm hiện có", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="w")

        # Thêm các kho vào scrollable_frame
        for row, kho in enumerate(kho_data, start=1):
            ttk.Label(scrollable_frame, text=kho.id, padding=(5, 5)).grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=kho.ten_kho, padding=(5, 5)).grid(row=row, column=1, sticky="w")
            ttk.Label(scrollable_frame, text=kho.dung_tich, padding=(5, 5)).grid(row=row, column=2, sticky="w")

            # Hiển thị sản phẩm hiện có trong kho
            san_pham_text = "\n".join([f"{sp.san_pham.ten_san_pham} (x{sp.so_luong})" for sp in kho.kho_san_pham])
            ttk.Label(scrollable_frame, text=san_pham_text, padding=(5, 5)).grid(row=row, column=3, sticky="w")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row, column=4, sticky="w")

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda k=kho: self.edit_kho(k))
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda k=kho: self.delete_kho(k))
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

            transfer_button = tk.Button(control_frame, text="Chuyển SP", command=lambda k=kho: self.transfer_product(k))
            transfer_button.pack(side=tk.LEFT, padx=5, pady=2)

        # Thêm nút "Thêm kho" ở phía dưới giữa khung
        add_button = tk.Button(self.main_frame, text="Thêm kho", command=self.add_kho, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



    def add_kho(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm kho")

        ttk.Label(add_window, text="Tên kho").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_kho_entry = ttk.Entry(add_window)
        ten_kho_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="Dung tích").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        dung_tich_entry = ttk.Entry(add_window)
        dung_tich_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        def save_new_kho():
            ten_kho = ten_kho_entry.get()
            dung_tich = dung_tich_entry.get()

            if ten_kho and dung_tich.isdigit():
                self.kho_controller.them_kho(ten_kho, int(dung_tich))
                messagebox.showinfo("Thành công", "Đã thêm kho thành công!")
                add_window.destroy()
                self.show_kho_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và dung tích phải là số.")

        save_button = ttk.Button(add_window, text="Xác nhận", command=save_new_kho)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)


    def edit_kho(self, kho):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa kho")

        ttk.Label(edit_window, text="Tên kho").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ten_kho_entry = ttk.Entry(edit_window)
        ten_kho_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ten_kho_entry.insert(0, kho.ten_kho)

        ttk.Label(edit_window, text="Dung tích").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        dung_tich_entry = ttk.Entry(edit_window)
        dung_tich_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        dung_tich_entry.insert(0, kho.dung_tich)

        def save_edited_kho():
            ten_kho = ten_kho_entry.get()
            dung_tich = dung_tich_entry.get()

            if ten_kho and dung_tich.isdigit():
                self.kho_controller.sua_kho(kho.id, ten_kho, int(dung_tich))
                messagebox.showinfo("Thành công", "Đã chỉnh sửa kho thành công!")
                edit_window.destroy()
                self.show_kho_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và dung tích phải là số.")

        save_button = ttk.Button(edit_window, text="Xác nhận", command=save_edited_kho)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)


    def delete_kho(self, kho):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa kho này?")
        if confirm:
            self.kho_controller.xoa_kho(kho.id)
            messagebox.showinfo("Thành công", "Đã xóa kho thành công!")
            self.show_kho_list()

    def deliver_product(self, kho):
        deliver_window = tk.Toplevel(self)
        deliver_window.title("Giao sản phẩm")

        ttk.Label(deliver_window, text="ID sản phẩm").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        san_pham_id_entry = ttk.Entry(deliver_window)
        san_pham_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(deliver_window, text="Số lượng giao").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(deliver_window)
        so_luong_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        def save_delivered_product():
            san_pham_id = san_pham_id_entry.get()
            so_luong_giao = so_luong_entry.get()

            if san_pham_id.isdigit() & so_luong_giao.isdigit():
                self.kho_controller.giao_hang(kho.id, int(san_pham_id), int(so_luong_giao))
                messagebox.showinfo("Thành công", "Đã giao sản phẩm thành công!")
                deliver_window.destroy()
                self.show_kho_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập ID sản phẩm và số lượng hợp lệ.")

        save_button = ttk.Button(deliver_window, text="Xác nhận", command=save_delivered_product)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def transfer_product(self, kho):
        transfer_window = tk.Toplevel(self)
        transfer_window.title("Chuyển sản phẩm")

        ttk.Label(transfer_window, text="Chọn sản phẩm").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Lấy danh sách sản phẩm hiện có trong kho
        san_pham_dict = {sp.san_pham.ten_san_pham: sp.id_san_pham for sp in kho.kho_san_pham}
        
        san_pham_combo = ttk.Combobox(transfer_window, values=list(san_pham_dict.keys()))
        san_pham_combo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="Số lượng chuyển").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(transfer_window)
        so_luong_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="ID kho đích").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        kho_dich_id_entry = ttk.Entry(transfer_window)
        kho_dich_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        def save_transfer():
            ten_san_pham = san_pham_combo.get()
            so_luong = so_luong_entry.get()
            kho_dich_id = kho_dich_id_entry.get()

            if ten_san_pham in san_pham_dict and so_luong.isdigit() and kho_dich_id.isdigit():
                san_pham_id = san_pham_dict[ten_san_pham]
                self.kho_controller.chuyen_san_pham(kho.id, int(kho_dich_id), int(san_pham_id), int(so_luong))
                messagebox.showinfo("Thành công", "Đã chuyển sản phẩm thành công!")
                transfer_window.destroy()
                self.show_kho_list()
            else:
                messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm, nhập số lượng và ID kho đích hợp lệ.")

        save_button = ttk.Button(transfer_window, text="Xác nhận", command=save_transfer)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

  

    def show_nhan_cong_list(self):
        self.clear_frame()

        # Lấy dữ liệu từ controller
        nhan_cong_data = self.nhan_cong_controller.get_nhan_cong()

        if not nhan_cong_data:
            return

        # Xác định ngày nhân công cuối cùng
        last_nhan_cong_date = max(nc.id for nc in nhan_cong_data)

        # Tạo canvas và scrollbar
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo tiêu đề cho các cột
        headers = ["Ngày", "Tổng nhân công", "Số nhân công nhàn rỗi", "Điều khiển"]
        for col, header in enumerate(headers):
            label = ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), padding=(5, 5))
            label.grid(row=0, column=col, sticky="w")

        # Thêm các nhân công vào scrollable_frame
        for row, nhan_cong in enumerate(nhan_cong_data, start=1):
            ttk.Label(scrollable_frame, text=nhan_cong.id, padding=(5, 5)).grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=nhan_cong.tong_nhan_cong, padding=(5, 5)).grid(row=row, column=1, sticky="w")
            ttk.Label(scrollable_frame, text=nhan_cong.so_nhan_cong_nhan_roi, padding=(5, 5)).grid(row=row, column=2, sticky="w")

            # Tạo các nút điều khiển
            control_frame = tk.Frame(scrollable_frame)
            control_frame.grid(row=row, column=3, sticky="w")

            is_last_day = nhan_cong.id == last_nhan_cong_date

            edit_button = tk.Button(control_frame, text="Chỉnh sửa", command=lambda nc=nhan_cong: self.edit_nhan_cong(nc), state=tk.NORMAL if is_last_day else tk.DISABLED)
            edit_button.pack(side=tk.LEFT, padx=5, pady=2)

            delete_button = tk.Button(control_frame, text="Xóa", command=lambda nc=nhan_cong: self.delete_nhan_cong(nc), state=tk.NORMAL if is_last_day else tk.DISABLED)
            delete_button.pack(side=tk.LEFT, padx=5, pady=2)

            transfer_out_button = tk.Button(control_frame, text="Chuyển đi", command=lambda nc=nhan_cong: self.transfer_nhan_cong_out(nc), state=tk.NORMAL if is_last_day else tk.DISABLED)
            transfer_out_button.pack(side=tk.LEFT, padx=5, pady=2)

            transfer_in_button = tk.Button(control_frame, text="Chuyển về", command=lambda nc=nhan_cong: self.transfer_nhan_cong_in(nc), state=tk.NORMAL if is_last_day else tk.DISABLED)
            transfer_in_button.pack(side=tk.LEFT, padx=5, pady=2)

        # Thêm nút "Thêm nhân công" ở phía dưới giữa khung
        add_button = tk.Button(self.main_frame, text="Thêm nhân công", command=self.add_nhan_cong, font=("Arial", 12, "bold"), padx=20, pady=10)
        add_button.pack(side="bottom", pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


    def add_nhan_cong(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm ngày nhân công")

        ttk.Label(add_window, text="Ngày (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ngay_entry = ttk.Entry(add_window)
        ngay_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(add_window, text="Số lượng").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(add_window)
        so_luong_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        def save_nhan_cong():
            ngay = ngay_entry.get()
            so_luong = so_luong_entry.get()
            try:
                nhan_cong_id = datetime.strptime(ngay, '%Y-%m-%d').date()
                so_luong = int(so_luong)
                self.nhan_cong_controller.them_nhan_cong(nhan_cong_id, so_luong)
                messagebox.showinfo("Thành công", "Đã thêm nhân công thành công!")
                add_window.destroy()
                self.show_nhan_cong_list()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập ngày và số lượng hợp lệ.")

        save_button = ttk.Button(add_window, text="Lưu", command=save_nhan_cong)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)
    def edit_nhan_cong(self, nhan_cong):
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa nhân công")

        ttk.Label(edit_window, text="Tổng nhân công").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tong_nhan_cong_entry = ttk.Entry(edit_window)
        tong_nhan_cong_entry.insert(0, nhan_cong.tong_nhan_cong)
        tong_nhan_cong_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Số nhân công nhàn rỗi").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        so_nhan_cong_nhan_roi_entry = ttk.Entry(edit_window)
        so_nhan_cong_nhan_roi_entry.insert(0, nhan_cong.so_nhan_cong_nhan_roi)
        so_nhan_cong_nhan_roi_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        def save_edit():
            tong_nhan_cong = tong_nhan_cong_entry.get()
            so_nhan_cong_nhan_roi = so_nhan_cong_nhan_roi_entry.get()
            try:
                tong_nhan_cong = int(tong_nhan_cong)
                so_nhan_cong_nhan_roi = int(so_nhan_cong_nhan_roi)
                self.nhan_cong_controller.sua_nhan_cong(nhan_cong.id, tong_nhan_cong, so_nhan_cong_nhan_roi)
                messagebox.showinfo("Thành công", "Đã chỉnh sửa nhân công thành công!")
                edit_window.destroy()
                self.show_nhan_cong_list()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hợp lệ.")

        save_button = ttk.Button(edit_window, text="Lưu", command=save_edit)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)
    def delete_nhan_cong(self, nhan_cong):
        delete_window = tk.Toplevel(self)
        delete_window.title("Xóa nhân công")

        ttk.Label(delete_window, text="Số lượng").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(delete_window)
        so_luong_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        def confirm_delete():
            so_luong = so_luong_entry.get()
            try:
                so_luong = int(so_luong)
                self.nhan_cong_controller.xoa_nhan_cong(nhan_cong.id, so_luong)
                messagebox.showinfo("Thành công", "Đã xóa nhân công thành công!")
                delete_window.destroy()
                self.show_nhan_cong_list()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hợp lệ.")

        confirm_button = ttk.Button(delete_window, text="Xác nhận", command=confirm_delete)
        confirm_button.grid(row=1, column=0, columnspan=2, pady=10)
    def transfer_nhan_cong_out(self, nhan_cong):
        transfer_window = tk.Toplevel(self)
        transfer_window.title("Chuyển nhân công đi")

        # Giả sử bạn có danh sách các ID quy trình và thứ tự giai đoạn
        quy_trinh_ids = [1, 2, 3]  # Thay thế bằng dữ liệu thực tế
        thu_tu_giai_doan = [1, 2, 3]  # Thay thế bằng dữ liệu thực tế

        ttk.Label(transfer_window, text="ID Quy trình").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        quy_trinh_id_combobox = ttk.Combobox(transfer_window, values=quy_trinh_ids)
        quy_trinh_id_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="Thứ tự giai đoạn").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        thu_tu_combobox = ttk.Combobox(transfer_window, values=thu_tu_giai_doan)
        thu_tu_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="Số lượng").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(transfer_window)
        so_luong_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        def confirm_transfer_out():
            quy_trinh_id = quy_trinh_id_combobox.get()
            thu_tu = thu_tu_combobox.get()
            so_luong = so_luong_entry.get()
            try:
                quy_trinh_id = int(quy_trinh_id)
                thu_tu = int(thu_tu)
                so_luong = int(so_luong)
                self.nhan_cong_controller.chuyen_nhan_cong_di(nhan_cong.id, quy_trinh_id, thu_tu, so_luong)
                messagebox.showinfo("Thành công", "Đã chuyển nhân công đi thành công!")
                transfer_window.destroy()
                self.show_nhan_cong_list()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

        confirm_button = ttk.Button(transfer_window, text="Xác nhận", command=confirm_transfer_out)
        confirm_button.grid(row=3, column=0, columnspan=2, pady=10)

    def transfer_nhan_cong_in(self, nhan_cong):
        transfer_window = tk.Toplevel(self)
        transfer_window.title("Chuyển nhân công về")

        # Giả sử bạn có danh sách các ID quy trình và thứ tự giai đoạn
        quy_trinh_ids = [1, 2, 3]  # Thay thế bằng dữ liệu thực tế
        thu_tu_giai_doan = [1, 2, 3]  # Thay thế bằng dữ liệu thực tế

        ttk.Label(transfer_window, text="ID Quy trình").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        quy_trinh_id_combobox = ttk.Combobox(transfer_window, values=quy_trinh_ids)
        quy_trinh_id_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="Thứ tự giai đoạn").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        thu_tu_combobox = ttk.Combobox(transfer_window, values=thu_tu_giai_doan)
        thu_tu_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(transfer_window, text="Số lượng").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        so_luong_entry = ttk.Entry(transfer_window)
        so_luong_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        def confirm_transfer_in():
            quy_trinh_id = quy_trinh_id_combobox.get()
            thu_tu = thu_tu_combobox.get()
            so_luong = so_luong_entry.get()
            try:
                quy_trinh_id = int(quy_trinh_id)
                thu_tu = int(thu_tu)
                so_luong = int(so_luong)
                self.nhan_cong_controller.chuyen_nhan_cong_ve(nhan_cong.id, quy_trinh_id, thu_tu, so_luong)
                messagebox.showinfo("Thành công", "Đã chuyển nhân công về thành công!")
                transfer_window.destroy()
                self.show_nhan_cong_list()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

        confirm_button = ttk.Button(transfer_window, text="Xác nhận", command=confirm_transfer_in)
        confirm_button.grid(row=3, column=0, columnspan=2, pady=10)


    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
