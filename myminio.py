from minio import Minio
from minio.error import S3Error

# Kết nối tới MinIO
client = Minio(
    "192.168.144.1:9000",  # Địa chỉ MinIO
    access_key="***********", 
    secret_key="***********", 
    secure=False 
)

# Tên bucket và file cần upload
bucket_name = "pgback-2808"
file_path = "/home/vinh/Documents/test-s3-aws/file.txt"
object_name = "file.txt"  # Tên file sau khi upload lên MinIO

# Kiểm tra nếu bucket không tồn tại thì tạo mới
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

try:
    # Upload file
    client.fput_object(
        bucket_name, object_name, file_path,
    )
    print(f"{object_name} đã được upload thành công lên {bucket_name}.")
except S3Error as e:
    print(f"Lỗi khi upload file: {e}")
