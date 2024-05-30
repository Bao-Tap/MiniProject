from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class NhanCong(Base):
    __tablename__ = 'nhancong'
    id = Column('ID_NhanCong', Date, primary_key=True, nullable=False)
    tong_nhan_cong = Column('TongNhanCong', Integer)
    so_nhan_cong_nhan_roi = Column('SoNhanCongNhanRoi', Integer)

class BangChuyen(Base):
    __tablename__ = 'bangchuyen'
    id = Column('ID_BangChuyen', Integer, primary_key=True, index=True)
    ten_bang_chuyen = Column('TenBangChuyen', String(45))
    toc_do = Column('TocDo', Integer)
    suc_chua = Column('SucChua', Integer)
    tai_hien_tai = Column('TaiHienTai', Integer, default=0)
    giai_doan = relationship("GiaiDoanSanXuat", back_populates="bang_chuyen", uselist=False)

class GiaiDoanSanXuat(Base):
    __tablename__ = 'giaidoansanxuat'
    id = Column('ID_GiaiDoan', Integer, primary_key=True, index=True)
    id_quy_trinh_san_xuat = Column('ID_QuyTrinhSanXuat', Integer, ForeignKey('quytrinhsanxuat.ID_QuyTrinhSanXuat'))
    id_bang_chuyen = Column('ID_BangChuyen', Integer, ForeignKey('bangchuyen.ID_BangChuyen'))
    so_nhan_cong_hien_tai = Column('SoNhanCongHienTai', Integer)
    so_nhan_cong_nang_suat_lon_nhat = Column('SoNhanCongNangSuatLonNhat', Integer)
    thoi_gian_xu_ly_toi_thieu = Column('ThoiGianXuLyToiThieu', Integer)
    la_giai_doan_cuoi = Column('la_giai_doan_cuoi', Boolean)
    thu_tu = Column('ThuTu', Integer)
    bang_chuyen = relationship("BangChuyen", back_populates="giai_doan")


class QuyTrinhSanXuat(Base):
    __tablename__ = 'quytrinhsanxuat'
    id = Column('ID_QuyTrinhSanXuat', Integer, primary_key=True, index=True)
    ten_quy_trinh_san_xuat = Column('TenQuyTrinhSanXuat', String(45))
    so_giai_doan = Column('SoGiaiDoan', Integer)


class DonHang(Base):
    __tablename__ = 'donhang'
    id = Column('ID_DonHang', Integer, primary_key=True, index=True)
    ten_don_hang = Column('TenDonHang', String(45))
    ten_khach_hang = Column('TenKhachHang', String(45))
    thoi_gian_yeu_cau_hoan_thanh = Column('ThoiGianYeuCauHoanThanh', Date)
    don_hang_san_pham = relationship("DonHangSanPham", back_populates="don_hang")

class DonHangSanPham(Base):
    __tablename__ = 'donhang_sanpham'
    id_don_hang = Column('ID_DonHang', Integer, ForeignKey('donhang.ID_DonHang'), primary_key=True)
    id_san_pham = Column('ID_NhomSanPham', Integer, ForeignKey('sanpham.ID_NhomSanPham'), primary_key=True)
    so_luong = Column('SoLuong', Integer)
    don_hang = relationship("DonHang", back_populates="don_hang_san_pham")
    san_pham = relationship("SanPham")


class Kho(Base):
    __tablename__ = 'kho'
    id = Column('ID_Kho', Integer, primary_key=True, index=True)
    ten_kho = Column('TenKho', String(45))
    dung_tich = Column('DungTich', Integer)
    kho_san_pham = relationship("KhoSanPham", back_populates="kho")

class KhoSanPham(Base):
    __tablename__ = 'kho_sanpham'
    id_kho = Column('ID_Kho', Integer, ForeignKey('kho.ID_Kho'), primary_key=True)
    id_san_pham = Column('ID_NhomSanPham', Integer, ForeignKey('sanpham.ID_NhomSanPham'), primary_key=True)
    so_luong = Column('SoLuong', Integer)
    kho = relationship("Kho", back_populates="kho_san_pham")
    san_pham = relationship("SanPham", back_populates="kho_san_pham")
class SanPham(Base):
    __tablename__ = 'sanpham'
    id = Column('ID_NhomSanPham', Integer, primary_key=True, index=True)
    ten_san_pham = Column('TenNhomSanPham', String(45))
    san_pham_dang_xu_ly = Column('SanPhamDangXuLy', Integer, default=0)
    id_quy_trinh_san_xuat = Column('ID_QuyTrinhSanXuat', Integer, ForeignKey('quytrinhsanxuat.ID_QuyTrinhSanXuat'))
    kho_san_pham = relationship("KhoSanPham", back_populates="san_pham")
