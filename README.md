# Cấu hình MinIO với HTTPS sử dụng chứng chỉ tự ký (self-signed certificate)

## Bước 1: Tạo self-signed certificate
Bạn có thể sử dụng openssl để tạo một chứng chỉ tự ký. Dưới đây là các lệnh cần thiết:

Tạo Private Key:

```bash
openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048
```

Tạo Certificate Signing Request (CSR):

```bash
openssl req -new -key private.key -out certificate.csr
```

Khi được yêu cầu thông tin, hãy nhập các thông tin liên quan. Đặc biệt quan trọng là Common Name (CN) phải là địa chỉ IP hoặc tên miền mà MinIO sẽ sử dụng.

Tạo Self-Signed Certificate:

```bash
openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out public.crt
```

Điều này sẽ tạo ra một chứng chỉ tự ký có thời hạn 1 năm.

## Bước 2: Cấu hình MinIO để sử dụng HTTPS
Sau khi tạo xong các file chứng chỉ (private.key và public.crt), bạn cần cấu hình MinIO để sử dụng các chứng chỉ này.

Tạo các thư mục cần thiết:

Nếu bạn đang chạy MinIO trong Docker, bạn cần tạo các thư mục sau để lưu trữ chứng chỉ.
bash

```
mkdir -p /path/to/minio/certs
```

Di chuyển các file chứng chỉ vào đúng thư mục:

Di chuyển các file private.key và public.crt vào thư mục certs mà bạn đã tạo:

```bash
mv private.key /path/to/minio/certs/private.key
mv public.crt /path/to/minio/certs/public.crt
```
Lưu ý: Trong cấu hình Docker, bạn cần map thư mục này vào container MinIO.

Cấu hình Docker Compose để sử dụng chứng chỉ:

Nếu bạn sử dụng Docker Compose, cập nhật docker-compose.yml để map thư mục chứa chứng chỉ vào container MinIO:

```yaml
version: '3.8'

services:
  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: your-access-key
      MINIO_ROOT_PASSWORD: your-secret-key
    volumes:
      - data:/data
      - config:/root/.minio
      - /path/to/minio/certs:/root/.minio/certs
    command: server /data --console-address ":9001"

volumes:
  data:
  config:
```

Khởi động lại MinIO:

Khởi động lại MinIO để áp dụng các thay đổi:
bash

docker-compose down
docker-compose up -d
Bước 3: Cấu hình pgBackRest để kết nối với MinIO qua HTTPS
Sau khi MinIO đã được cấu hình với HTTPS, cập nhật file cấu hình pgBackRest để sử dụng HTTPS:

```ini
[global]
repo1-s3-endpoint=https://192.168.144.1:9000
repo1-s3-bucket=your-bucket-name
repo1-s3-region=default
repo1-s3-key=your-access-key
repo1-s3-key-secret=your-secret-key
repo1-s3-verify-tls=n  # Đặt 'n' nếu bạn muốn bỏ qua xác minh chứng chỉ

repo1-type=s3
repo1-path=/backups
repo1-retention-full=2
repo1-retention-diff=7
repo1-retention-archive=7
```