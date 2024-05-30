from sqlalchemy.orm import Session
from models import *
import threading
import time
from sqlalchemy import func
from sqlalchemy.orm import joinedload
class NhanCongController:
    def __init__(self, db: Session):
        self.db = db

    def get_nhan_cong(self):
        try:
            return self.db.query(NhanCong).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách nhân công: {e}")
            return []

    def chuyen_nhan_cong_di(self, nhan_cong_id, quy_trinh_id, ThuTu, so_luong):
        try:
            nhan_cong = self.db.query(NhanCong).filter(NhanCong.id == nhan_cong_id).first()
            quy_trinh_sx = self.db.query(QuyTrinhSanXuat).filter(QuyTrinhSanXuat.id == quy_trinh_id).first()
            giai_doan = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh_id, GiaiDoanSanXuat.thu_tu == ThuTu).first()
            
            if nhan_cong and quy_trinh_sx and giai_doan:
                if nhan_cong.so_nhan_cong_nhan_roi >= so_luong:
                    nhan_cong.so_nhan_cong_nhan_roi -= so_luong
                    giai_doan.so_nhan_cong_hien_tai += so_luong
                    self.db.commit()
                    print(f"Chuyển {so_luong} nhân công sang giai đoạn {ThuTu} của quy trình {quy_trinh_sx.ten_quy_trinh_san_xuat}")
                else:
                    print(f"Không đủ nhân công nhàn rỗi để chuyển. Chỉ còn {nhan_cong.so_nhan_cong_nhan_roi} nhân công")
            else:
                print("Không tìm thấy nhân công hoặc quy trình sản xuất hoặc giai đoạn sản xuất.")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi chuyển nhân công: {e}")

    def chuyen_nhan_cong_ve(self, nhan_cong_id, quy_trinh_id, ThuTu, so_luong):
        try:
            nhan_cong = self.db.query(NhanCong).filter(NhanCong.id == nhan_cong_id).first()
            quy_trinh_sx = self.db.query(QuyTrinhSanXuat).filter(QuyTrinhSanXuat.id == quy_trinh_id).first()
            giai_doan = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh_id, GiaiDoanSanXuat.thu_tu == ThuTu).first()
            
            if nhan_cong and quy_trinh_sx and giai_doan:
                if giai_doan.so_nhan_cong_hien_tai >= so_luong:
                    nhan_cong.so_nhan_cong_nhan_roi += so_luong
                    giai_doan.so_nhan_cong_hien_tai -= so_luong
                    self.db.commit()
                    print(f"Chuyển {so_luong} nhân công từ giai đoạn {ThuTu} của quy trình {quy_trinh_sx.ten_quy_trinh_san_xuat} về nhàn rỗi. Giai đoạn này còn {giai_doan.so_nhan_cong_hien_tai} nhân công")
                else:
                    print(f"Số nhân công hiện tại của giai đoạn này chỉ còn {giai_doan.so_nhan_cong_hien_tai} nhân công. Không đủ để chuyển về")
            else:
                print("Không tìm thấy nhân công hoặc quy trình sản xuất hoặc giai đoạn sản xuất.")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi chuyển nhân công: {e}")

    def them_nhan_cong(self, nhan_cong_id, so_luong):
        try:
            nhan_cong = self.db.query(NhanCong).filter(NhanCong.id == nhan_cong_id).first()
            if nhan_cong:
                nhan_cong.tong_nhan_cong += so_luong
                nhan_cong.so_nhan_cong_nhan_roi += so_luong
                self.db.commit()
                print(f"Thêm {so_luong} nhân công vào ngày {nhan_cong_id}")
            else:
                new_nhan_cong = NhanCong(id=nhan_cong_id, tong_nhan_cong=so_luong, so_nhan_cong_nhan_roi=so_luong)
                self.db.add(new_nhan_cong)
                self.db.commit()
                print(f"Tạo mới và thêm {so_luong} nhân công vào ngày {nhan_cong_id}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi thêm nhân công: {e}")

    def xoa_nhan_cong(self, nhan_cong_id, so_luong):
        try:
            nhan_cong = self.db.query(NhanCong).filter(NhanCong.id == nhan_cong_id).first()
            if nhan_cong:
                if nhan_cong.tong_nhan_cong >= so_luong:
                    if nhan_cong.so_nhan_cong_nhan_roi >= so_luong:
                        nhan_cong.tong_nhan_cong -= so_luong
                        nhan_cong.so_nhan_cong_nhan_roi -= so_luong
                        self.db.commit()
                        print(f"Xóa {so_luong} nhân công khỏi ngày {nhan_cong_id}")
                    else:
                        so_nhan_cong_thieu = so_luong - nhan_cong.so_nhan_cong_nhan_roi
                        print(f"Số nhân công nhàn rỗi không đủ. Hãy di chuyển tối thiểu {so_nhan_cong_thieu} nhân công đang làm việc về nhàn rỗi rồi mới xóa được")
                else:
                    print(f"Số lượng nhân công hiện tại không đủ để xóa. Chỉ có {nhan_cong.tong_nhan_cong} nhân công")
            else:
                print(f"Không tìm thấy bản ghi nhân công cho ngày {nhan_cong_id}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi xóa nhân công: {e}")

    def sua_nhan_cong(self, nhan_cong_id, tong_nhan_cong=None, so_nhan_cong_nhan_roi=None):
        try:
            nhan_cong = self.db.query(NhanCong).filter(NhanCong.id == nhan_cong_id).first()
            if nhan_cong:
                if tong_nhan_cong is not None:
                    nhan_cong.tong_nhan_cong = tong_nhan_cong
                if so_nhan_cong_nhan_roi is not None:
                    nhan_cong.so_nhan_cong_nhan_roi = so_nhan_cong_nhan_roi
                self.db.commit()
                print(f"Sửa thông tin nhân công cho ngày {nhan_cong_id}")
            else:
                print(f"Không tìm thấy bản ghi nhân công cho ngày {nhan_cong_id}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi sửa nhân công: {e}")
class BangChuyenController:
    def __init__(self, db: Session):
        self.db = db
    def get_bang_chuyen(self):
        try:
            return self.db.query(BangChuyen).options(joinedload(BangChuyen.giai_doan)).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách băng chuyền: {e}")
            return []

    def them_san_pham(self, bang_chuyen_id, san_pham_id):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()
        
        if bang_chuyen.tai_hien_tai < bang_chuyen.suc_chua:
            bang_chuyen.tai_hien_tai += 1
            san_pham.san_pham_dang_xu_ly += 1
            self.db.commit()
            print(f"Thêm {san_pham.ten_san_pham} lên {bang_chuyen.ten_bang_chuyen}")
        else:
            print(f"{bang_chuyen.ten_bang_chuyen} đã đầy. Không thể thêm sản phẩm")

    def dichuyen_san_pham(self, san_pham_id, bang_chuyen_id):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()

        if bang_chuyen.tai_hien_tai > 0:
            bang_chuyen.tai_hien_tai -= 1
            self.db.commit()
            print(f"Di chuyển {san_pham.ten_san_pham} khỏi {bang_chuyen.ten_bang_chuyen}")
            self.dichuyen_san_pham_den_bang_chuyen_ke_tiep(bang_chuyen, san_pham)
        else:
            print(f"{bang_chuyen.ten_bang_chuyen} đang trống. Không có sản phẩm để di chuyển")

    def dichuyen_san_pham_den_bang_chuyen_ke_tiep(self, bang_chuyen, san_pham):
        giai_doan_hien_tai = bang_chuyen.giai_doan
        giai_doan_ke_tiep = self.db.query(GiaiDoanSanXuat).filter(
            GiaiDoanSanXuat.id_quy_trinh_san_xuat == giai_doan_hien_tai.id_quy_trinh_san_xuat,
            GiaiDoanSanXuat.thu_tu == giai_doan_hien_tai.thu_tu + 1
        ).first()

        if giai_doan_ke_tiep:
            bang_chuyen_ke_tiep = self.db.query(BangChuyen).filter(
                BangChuyen.id == giai_doan_ke_tiep.id_bang_chuyen
            ).first()

            if bang_chuyen_ke_tiep.tai_hien_tai < bang_chuyen_ke_tiep.suc_chua:
                self.them_san_pham(bang_chuyen_ke_tiep.id, san_pham.id)
            else:
                print(f"{bang_chuyen_ke_tiep.ten_bang_chuyen} đã đầy. Không thể di chuyển sản phẩm")
        else:
            print("Đây là giai đoạn cuối cùng. Chuyển sản phẩm vào kho")
            kho_controller = KhoController(self.db)
            kho = kho_controller.tim_kho_theo_san_pham(san_pham.id)
            if kho:
                kho_controller.chuyen_san_pham_vao_kho(kho.id, san_pham.id)
            else:
                print("Tất cả kho đã đầy, hãy xây thêm kho để chứa sản phẩm")

    def kiem_tra_trang_thai(self, bang_chuyen_id):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        print(f"Băng chuyền {bang_chuyen.ten_bang_chuyen}:")
        print(f"- Tốc độ: {bang_chuyen.toc_do} s/sản phẩm")
        print(f"- Sức chứa: {bang_chuyen.suc_chua} sản phẩm")
        print(f"- Tải hiện tại: {bang_chuyen.tai_hien_tai} sản phẩm")

    def thay_doi_toc_do(self, bang_chuyen_id, toc_do_moi):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        bang_chuyen.toc_do = toc_do_moi
        self.db.commit()
        print(f"Thay đổi tốc độ băng chuyền \"{bang_chuyen.ten_bang_chuyen}\" thành {toc_do_moi}s/sản phẩm")

    def them_bang_chuyen(self, ten_bang_chuyen, toc_do, suc_chua):
        bang_chuyen = BangChuyen(ten_bang_chuyen=ten_bang_chuyen, toc_do=toc_do, suc_chua=suc_chua)
        self.db.add(bang_chuyen)
        self.db.commit()
        print(f"Đã thêm băng chuyền {ten_bang_chuyen}")

    def sua_bang_chuyen(self, bang_chuyen_id, ten_bang_chuyen=None, toc_do=None, suc_chua=None):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        if bang_chuyen:
            if ten_bang_chuyen:
                bang_chuyen.ten_bang_chuyen = ten_bang_chuyen
            if toc_do:
                bang_chuyen.toc_do = toc_do
            if suc_chua:
                bang_chuyen.suc_chua = suc_chua
            self.db.commit()
            print(f"Đã sửa băng chuyền {bang_chuyen_id}")
        else:
            print(f"Băng chuyền {bang_chuyen_id} không tồn tại")

    def xoa_bang_chuyen(self, bang_chuyen_id):
        bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.id == bang_chuyen_id).first()
        if bang_chuyen:
            self.db.delete(bang_chuyen)
            self.db.commit()
            print(f"Xóa băng chuyền {bang_chuyen_id}")
        else:
            print(f"Băng chuyền {bang_chuyen_id} không tồn tại")

class KhoController:
    def __init__(self, db: Session):
        self.db = db

    def get_kho(self):
        try:
            return self.db.query(Kho).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách kho: {e}")
            return []

    def cap_nhat_so_luong(self, kho_id, san_pham_id, so_luong_moi):
        try:
            kho_san_pham = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id, KhoSanPham.id_san_pham == san_pham_id).first()
            if kho_san_pham:
                kho_san_pham.so_luong = so_luong_moi
                self.db.commit()
                print(f"Cập nhật số lượng sản phẩm {san_pham_id} trong kho {kho_id} thành {so_luong_moi}")
            else:
                print(f"Không tìm thấy sản phẩm {san_pham_id} trong kho {kho_id}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi cập nhật số lượng sản phẩm: {e}")

    def giao_hang(self, kho_id, san_pham_id, so_luong_giao):
        try:
            kho_san_pham = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id, KhoSanPham.id_san_pham == san_pham_id).first()
            if kho_san_pham:
                if kho_san_pham.so_luong >= so_luong_giao:
                    kho_san_pham.so_luong -= so_luong_giao
                    self.db.commit()
                    print(f"Giao {so_luong_giao} sản phẩm {san_pham_id} từ kho {kho_id}")
                else:
                    print(f"Không đủ số lượng sản phẩm trong kho {kho_id} để giao. Chỉ còn {kho_san_pham.so_luong} sản phẩm")
            else:
                print(f"Không tìm thấy sản phẩm {san_pham_id} trong kho {kho_id}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi giao hàng: {e}")

    def tim_kho_theo_san_pham(self, san_pham_id):
        try:
            return self.db.query(KhoSanPham).filter(KhoSanPham.id_san_pham == san_pham_id).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi tìm kho theo sản phẩm: {e}")
            return []

    def them_kho(self, ten_kho, dung_tich):
        try:
            kho = Kho(ten_kho=ten_kho, dung_tich=dung_tich)
            self.db.add(kho)
            self.db.commit()
            print(f"Thêm kho {ten_kho}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi thêm kho: {e}")

    def sua_kho(self, kho_id, ten_kho=None, dung_tich=None):
        try:
            kho = self.db.query(Kho).filter(Kho.id == kho_id).first()
            if kho:
                if ten_kho:
                    kho.ten_kho = ten_kho
                if dung_tich is not None:
                    tong_so_luong = self.db.query(func.sum(KhoSanPham.so_luong)).filter(KhoSanPham.id_kho == kho_id).scalar() or 0
                    if tong_so_luong > dung_tich:
                        print(f"Dung tích mới không đủ chứa các sản phẩm hiện tại trong kho {kho_id}. Tổng số lượng sản phẩm: {tong_so_luong}, dung tích mới: {dung_tich}")
                        return
                    kho.dung_tich = dung_tich
                self.db.commit()
                print(f"Sửa kho {kho_id}")
            else:
                print(f"Kho {kho_id} không tồn tại")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi sửa kho: {e}")

    def xoa_kho(self, kho_id):
        try:
            kho = self.db.query(Kho).filter(Kho.id == kho_id).first()
            if kho:
                kho_san_pham = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id).all()
                if not kho_san_pham:
                    self.db.delete(kho)
                    self.db.commit()
                    print(f"Xóa kho {kho_id}")
                else:
                    print(f"Kho {kho_id} có chứa sản phẩm, không thể xóa.")
            else:
                print(f"Kho {kho_id} không tồn tại")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi xóa kho: {e}")

    def chuyen_san_pham(self, kho_id_nguon, kho_id_dich, san_pham_id, so_luong):
        try:
            kho_san_pham_nguon = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id_nguon, KhoSanPham.id_san_pham == san_pham_id).first()
            kho_san_pham_dich = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id_dich, KhoSanPham.id_san_pham == san_pham_id).first()
            if kho_san_pham_nguon and kho_san_pham_nguon.so_luong >= so_luong:
                tong_so_luong_kho_dich = self.db.query(func.sum(KhoSanPham.so_luong)).filter(KhoSanPham.id_kho == kho_id_dich).scalar() or 0
                kho_dich = self.db.query(Kho).filter(Kho.id == kho_id_dich).first()
                if kho_dich and tong_so_luong_kho_dich + so_luong <= kho_dich.dung_tich:
                    kho_san_pham_nguon.so_luong -= so_luong
                    if kho_san_pham_dich:
                        kho_san_pham_dich.so_luong += so_luong
                    else:
                        kho_san_pham_dich = KhoSanPham(id_kho=kho_id_dich, id_san_pham=san_pham_id, so_luong=so_luong)
                        self.db.add(kho_san_pham_dich)
                    self.db.commit()
                    print(f"Chuyển {so_luong} sản phẩm {san_pham_id} từ kho {kho_id_nguon} sang kho {kho_id_dich}")
                else:
                    print(f"Dung tích kho đích không đủ chứa sản phẩm. Dung tích kho đích: {kho_dich.dung_tich}, tổng số lượng hiện tại: {tong_so_luong_kho_dich}, số lượng chuyển: {so_luong}")
            else:
                print(f"Số lượng sản phẩm trong kho nguồn không đủ. Số lượng hiện tại: {kho_san_pham_nguon.so_luong}, số lượng chuyển: {so_luong}")
        except Exception as e:
            self.db.rollback()
            print(f"Đã xảy ra lỗi khi chuyển sản phẩm: {e}")


class KhoSanPhamController:
    def __init__(self, db: Session):
        self.db = db

    def get_kho_san_pham(self, kho_id: int):
        try:
            return self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách sản phẩm của kho: {e}")
            return []


class GiaiDoanSanXuatController:
    def __init__(self, db: Session):
        self.db = db
    def get_giai_doan(self):
        try:
            return self.db.query(GiaiDoanSanXuat).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách giai đoạn: {e}")
            return []
    def wait_(self, n, san_pham, giai_doan, quytrinh_ten):
        time.sleep(n)
        print(f"Hoàn thành xử lý sản phẩm {san_pham.ten_san_pham} tại giai đoạn {giai_doan.thu_tu} của quy trình {quytrinh_ten}")

        if giai_doan.la_giai_doan_cuoi:
            kho_controller = KhoController(self.db)
            kho = kho_controller.tim_kho_theo_san_pham(san_pham.id)
            if kho:
                kho_controller.chuyen_san_pham_vao_kho(kho.id, san_pham.id)
            else:
                print("Tất cả kho đã đầy, hãy xây thêm kho để chứa sản phẩm")
        else:
            bang_chuyen = self.db.query(BangChuyen).filter(BangChuyen.giai_doan_id == giai_doan.id).first()
            bang_chuyen_controller = BangChuyenController(self.db)
            bang_chuyen_controller.dichuyen_san_pham(san_pham.id, bang_chuyen.id)

    def xu_ly_san_pham(self, quy_trinh_id, ThuTu, san_pham_id):
        giai_doan = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh_id, 
                                                          GiaiDoanSanXuat.thu_tu== ThuTu).first()
        quy_trinh_sx = self.db.query(QuyTrinhSanXuat).filter(QuyTrinhSanXuat.id == quy_trinh_id).first()
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()
        
        if giai_doan.so_nhan_cong_hien_tai > 0:
            print(f"Bắt đầu xử lý sản phẩm {san_pham.ten_san_pham} tại giai đoạn {ThuTu} của quy trình {quy_trinh_sx.ten_quy_trinh_san_xuat}")
            thoi_gian_xu_ly_thuc_te = giai_doan.thoi_gian_xu_ly_toi_thieu * max(1, giai_doan.so_nhan_cong_nang_suat_lon_nhat / giai_doan.so_nhan_cong_hien_tai)
            print(thoi_gian_xu_ly_thuc_te)
            thread = threading.Thread(target=self.wait_, args=(thoi_gian_xu_ly_thuc_te, san_pham, giai_doan,quy_trinh_sx.ten_quy_trinh_san_xuat ))
            thread.start()
        else:
            print(f"Giai đoạn {ThuTu} của quy trình {quy_trinh_sx.ten_quy_trinh_san_xuat} không có nhân công để xử lý sản phẩm. Cần thêm nhân công vào giai đoạn này")

    def chuyen_san_pham_vao_kho(self, kho_id, san_pham_id):
        kho = self.db.query(Kho).filter(Kho.id == kho_id).first()
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()
        kho_san_pham = self.db.query(KhoSanPham).filter(KhoSanPham.id_kho == kho_id, KhoSanPham.id_san_pham == san_pham_id).first()
        
        if kho_san_pham:
            kho_san_pham.so_luong += 1
        else:
            kho_san_pham = KhoSanPham(id_kho=kho_id, id_san_pham=san_pham_id, so_luong=1)
            self.db.add(kho_san_pham)
        
        self.db.commit()
        print(f"Chuyển sản phẩm {san_pham.ten_san_pham} vào {kho.ten_kho}")

    def them_giai_doan_san_xuat(self, id_quy_trinh_san_xuat, id_bang_chuyen, so_nhan_cong_hien_tai, so_nhan_cong_nang_suat_lon_nhat, thoi_gian_xu_ly_toi_thieu, la_giai_doan_cuoi, thu_tu):
        # Lấy tất cả các giai đoạn sản xuất của quy trình
        giai_doansx = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == id_quy_trinh_san_xuat).all()

        # Tăng thứ tự của các giai đoạn có thứ tự lớn hơn hoặc bằng thứ tự mới
        for gd in giai_doansx:
            if gd.thu_tu >= thu_tu:
                gd.thu_tu += 1

        # Nếu giai đoạn mới là giai đoạn cuối, cập nhật các giai đoạn khác
        if la_giai_doan_cuoi:
            for gd in giai_doansx:
                if gd.la_giai_doan_cuoi:
                    gd.la_giai_doan_cuoi = False

        # Tạo giai đoạn mới
        giai_doan = GiaiDoanSanXuat(
            id_quy_trinh_san_xuat=id_quy_trinh_san_xuat,
            id_bang_chuyen=id_bang_chuyen,
            so_nhan_cong_hien_tai=so_nhan_cong_hien_tai,
            so_nhan_cong_nang_suat_lon_nhat=so_nhan_cong_nang_suat_lon_nhat,
            thoi_gian_xu_ly_toi_thieu=thoi_gian_xu_ly_toi_thieu,
            la_giai_doan_cuoi=la_giai_doan_cuoi,
            thu_tu=thu_tu
        )

        # Thêm giai đoạn mới vào cơ sở dữ liệu
        self.db.add(giai_doan)
        self.db.commit()
        print(f"Thêm giai đoạn sản xuất {thu_tu} vào quy trình {id_quy_trinh_san_xuat}")


    def sua_giai_doan_san_xuat(self, giai_doan_id, id_quytrinh=None, id_bang_chuyen=None, so_nhan_cong_hien_tai=None, so_nhan_cong_nang_suat_lon_nhat=None, thoi_gian_xu_ly_toi_thieu=None, la_giai_doan_cuoi=None, thu_tu=None):
        giai_doan = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id == giai_doan_id).first()
        if giai_doan:
            if id_bang_chuyen:
                giai_doan.id_bang_chuyen = id_bang_chuyen
            if id_quytrinh:
                giai_doan.id_quy_trinh_san_xuat = id_quytrinh
            if so_nhan_cong_hien_tai:
                giai_doan.so_nhan_cong_hien_tai = so_nhan_cong_hien_tai
            if so_nhan_cong_nang_suat_lon_nhat:
                giai_doan.so_nhan_cong_nang_suat_lon_nhat = so_nhan_cong_nang_suat_lon_nhat
            if thoi_gian_xu_ly_toi_thieu:
                giai_doan.thoi_gian_xu_ly_toi_thieu = thoi_gian_xu_ly_toi_thieu
            if la_giai_doan_cuoi is not None:
                giai_doan.la_giai_doan_cuoi = la_giai_doan_cuoi
            if thu_tu:
                giai_doan.thu_tu = thu_tu
            self.db.commit()
            print(f"Sửa giai đoạn sản xuất {giai_doan_id}")
        else:
            print(f"Giai đoạn sản xuất {giai_doan_id} không tồn tại")

    def xoa_giai_doan_san_xuat(self, giai_doan_id):
        giai_doan = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id == giai_doan_id).first()
        if giai_doan:
            quy_trinh_id = giai_doan.id_quy_trinh_san_xuat
            la_giai_doan_cuoi = giai_doan.la_giai_doan_cuoi
            thu_tu_giai_doan = giai_doan.thu_tu

            # Xóa giai đoạn sản xuất
            self.db.delete(giai_doan)
            self.db.commit()
            print(f"Xóa giai đoạn sản xuất {giai_doan_id}")

            # Cập nhật lại thứ tự của các giai đoạn còn lại
            giai_doan_list = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh_id).order_by(GiaiDoanSanXuat.thu_tu).all()
            for idx, gd in enumerate(giai_doan_list):
                gd.thu_tu = idx + 1
                self.db.commit()
                print(f"Cập nhật thứ tự giai đoạn {gd.id} thành {gd.thu_tu}")

            # Nếu giai đoạn bị xóa là giai đoạn cuối, tìm giai đoạn có thứ tự cao nhất và thiết lập nó là giai đoạn cuối
            if la_giai_doan_cuoi:
                giai_doan_max_thutu = self.db.query(GiaiDoanSanXuat).filter(GiaiDoanSanXuat.id_quy_trinh_san_xuat == quy_trinh_id).order_by(GiaiDoanSanXuat.thu_tu.desc()).first()
                if giai_doan_max_thutu:
                    giai_doan_max_thutu.la_giai_doan_cuoi = True
                    self.db.commit()
                    print(f"Giai đoạn {giai_doan_max_thutu.id} được thiết lập là giai đoạn cuối của quy trình {quy_trinh_id}")

            # Giảm số lượng giai đoạn của quy trình tương ứng
            quy_trinh = self.db.query(QuyTrinhSanXuat).filter(QuyTrinhSanXuat.id == quy_trinh_id).first()
            if quy_trinh:
                quy_trinh.so_giai_doan -= 1
                self.db.commit()
                print(f"Giảm số lượng giai đoạn của quy trình {quy_trinh_id} thành {quy_trinh.so_giai_doan}")
        else:
            print(f"Giai đoạn sản xuất {giai_doan_id} không tồn tại")


class QuyTrinhSanXuatController:
    def __init__(self, db: Session):
        self.db = db
    def get_quy_trinh_san_xuat(self):
        try:
            return self.db.query(QuyTrinhSanXuat).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách quy trình sản xuất: {e}")
            return []


class SanPhamController:
    def __init__(self, db: Session):
        self.db = db
    def get_san_pham(self):
        try:
            return self.db.query(SanPham).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách sản phẩm: {e}")
            return []

    def them_san_pham(self, ten_san_pham, id_quy_trinh_san_xuat, san_pham_dang_xu_ly=0):
        san_pham = SanPham(
            ten_san_pham=ten_san_pham,
            id_quy_trinh_san_xuat=id_quy_trinh_san_xuat,
            san_pham_dang_xu_ly=san_pham_dang_xu_ly
        )
        self.db.add(san_pham)
        try:
            self.db.commit()
            print(f"Thêm sản phẩm {ten_san_pham} thành công")
        except Exception as e:
            self.db.rollback()
            print(f"Lỗi khi thêm sản phẩm: {e}")

    def sua_san_pham(self, san_pham_id, ten_san_pham=None, id_quy_trinh_san_xuat=None, san_pham_dang_xu_ly=None):
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()
        if san_pham:
            if ten_san_pham:
                san_pham.ten_san_pham = ten_san_pham
            if id_quy_trinh_san_xuat is not None:
                san_pham.id_quy_trinh_san_xuat = id_quy_trinh_san_xuat
            if san_pham_dang_xu_ly is not None:
                san_pham.san_pham_dang_xu_ly = san_pham_dang_xu_ly
            try:
                self.db.commit()
                print(f"Sửa sản phẩm {san_pham_id} thành công")
            except Exception as e:
                self.db.rollback()
                print(f"Lỗi khi sửa sản phẩm: {e}")
        else:
            print(f"Sản phẩm với ID {san_pham_id} không tồn tại")

    def xoa_san_pham(self, san_pham_id):
        san_pham = self.db.query(SanPham).filter(SanPham.id == san_pham_id).first()
        if san_pham:
            self.db.delete(san_pham)
            try:
                self.db.commit()
                print(f"Xóa sản phẩm {san_pham_id} thành công")
            except Exception as e:
                self.db.rollback()
                print(f"Lỗi khi xóa sản phẩm: {e}")
        else:
            print(f"Sản phẩm với ID {san_pham_id} không tồn tại")


class DonHangController:
    def __init__(self, db: Session):
        self.db = db

    def get_don_hang(self):
        try:
            return self.db.query(DonHang).all()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy danh sách đơn hàng: {e}")
            return []

    def them_don_hang(self, ten_don_hang, ten_khach_hang, thoi_gian_yeu_cau_hoan_thanh, san_pham_list):
        don_hang = DonHang(
            ten_don_hang=ten_don_hang,
            ten_khach_hang=ten_khach_hang,
            thoi_gian_yeu_cau_hoan_thanh=thoi_gian_yeu_cau_hoan_thanh
        )
        self.db.add(don_hang)
        self.db.flush()  # Để lấy ID của đơn hàng mới
        # Thêm các sản phẩm vào đơn hàng
        for sp_id, so_luong in san_pham_list:
            don_hang_san_pham = DonHangSanPham(
                id_don_hang=don_hang.id,
                id_san_pham=sp_id,
                so_luong=so_luong
            )
            self.db.add(don_hang_san_pham)

        try:
            self.db.commit()
            print(f"Thêm đơn hàng {ten_don_hang} thành công")
        except Exception as e:
            self.db.rollback()
            print(f"Lỗi khi thêm đơn hàng: {e}")

    def sua_don_hang(self, don_hang_id, ten_don_hang, ten_khach_hang, thoi_gian_yeu_cau_hoan_thanh, san_pham_list):
        don_hang = self.db.query(DonHang).filter(DonHang.id == don_hang_id).first()
        if don_hang:
            don_hang.ten_don_hang = ten_don_hang
            don_hang.ten_khach_hang = ten_khach_hang
            don_hang.thoi_gian_yeu_cau_hoan_thanh = thoi_gian_yeu_cau_hoan_thanh

            # Xóa các sản phẩm cũ của đơn hàng
            self.db.query(DonHangSanPham).filter(DonHangSanPham.id_don_hang == don_hang_id).delete()

            # Thêm các sản phẩm mới vào đơn hàng
            for sp_id, so_luong in san_pham_list:
                don_hang_san_pham = DonHangSanPham(
                    id_don_hang=don_hang_id,
                    id_san_pham=sp_id,
                    so_luong=so_luong
                )
                self.db.add(don_hang_san_pham)

            try:
                self.db.commit()
                print(f"Sửa đơn hàng {don_hang_id} thành công")
            except Exception as e:
                self.db.rollback()
                print(f"Lỗi khi sửa đơn hàng: {e}")
        else:
            print(f"Đơn hàng với ID {don_hang_id} không tồn tại")

    def xoa_don_hang(self, don_hang_id):
        don_hang = self.db.query(DonHang).filter(DonHang.id == don_hang_id).first()
        if don_hang:
            # Xóa các sản phẩm liên quan đến đơn hàng
            self.db.query(DonHangSanPham).filter(DonHangSanPham.id_don_hang == don_hang_id).delete()
            self.db.commit()
            self.db.delete(don_hang)
            try:
                self.db.commit()
                print(f"Xóa đơn hàng {don_hang_id} thành công")
            except Exception as e:
                self.db.rollback()
                print(f"Lỗi khi xóa đơn hàng: {e}")
        else:
            print(f"Đơn hàng với ID {don_hang_id} không tồn tại")
