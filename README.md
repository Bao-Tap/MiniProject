# Digital twin trong quy trình sản xuất
Dự án này là một ứng dụng được phát triển bằng Python, Tkinter và SQLAlchemy, giúp các doanh nghiệp quản lý quy trình sản xuất một cách hiệu quả. Với giao diện người dùng đơn giản và tích hợp cơ sở dữ liệu MySQL, dự án này cung cấp một cách tiếp cận để theo dõi và tối ưu hóa sản xuất.

## Tính năng
- Quản lý quy trình sản xuất từ đầu đến cuối.
- Theo dõi lịch trình sản xuất, tình trạng của các công đoạn và tài nguyên.
- Tích hợp cơ sở dữ liệu MySQL để lưu trữ và truy xuất dữ liệu một cách đáng tin cậy.
## Lợi ích
- Tối ưu hóa quy trình sản xuất: Theo dõi và phân tích hiệu suất sản xuất để tìm ra cơ hội tối ưu hóa và giảm thiểu lãng phí.
- Tăng cường kiểm soát chất lượng: Đảm bảo rằng mọi quy trình sản xuất đều tuân thủ các tiêu chuẩn chất lượng được đặt ra.
- Tiết kiệm thời gian và chi phí: Tối ưu hóa quy trình sản xuất có thể giúp giảm thiểu thời gian chờ đợi và lãng phí tài nguyên.
## Bảng tóm tắt

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lebatuanphong5398/RedLightViolation.git
    cd RedLightViolation
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Mở MySQL tạo một cơ sở dữ liệu mới và import thư mục database vào:**
    ```bash
    CREATE DATABASE quytrinhsx;
    ```
2. **Cập nhật tệp config.py với thông tin kết nối cơ sở dữ liệu của bạn.**
   ```bash
    DATABASE_URI = 'mysql+pymysql://username:password@localhost/quytrinhsx'
    ```
3. **Run the program:**

    ```bash
    python app.py
    ```



## Contributing


## License
