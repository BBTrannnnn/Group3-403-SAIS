import requests
import json
import time

url = "http://127.0.0.1:5000/api/vaccines"  # Sửa theo API của bạn
headers = {
    'Content-Type': 'application/json'
}

num_records_to_create = 1000
success_count = 0
failure_count = 0
total_time = 0

print("🚀 Bắt đầu gửi request tạo 1000 vaccine...\n")

for i in range(1, num_records_to_create + 1):
    payload_data = {
        "id": i,  # Nếu id này bị trùng sẽ bị lỗi (Status 400 hoặc 409)
        "name": f"Vaccine Test {i}",
        "description": f"Mô tả cho Vaccine Test {i}. Đây là vắc xin để thử nghiệm.",
        "manufacturer": f"Nhà sản xuất {i}",
        "efficacy": round(0.75 + (i * 0.002), 2),
        "side_effects": f"Tác dụng phụ nhẹ của Vaccine Test {i}.",
        "category": "Bắt buộc" if i % 2 == 0 else "Tự nguyện",
        "quantity": 500 + (i * 10)
    }

    payload = json.dumps(payload_data)

    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=payload)
        end_time = time.time()

        response_time = end_time - start_time
        total_time += response_time

        if response.status_code in [200, 201]:
            success_count += 1
            print(f"✅ Record {i}: Status {response.status_code} | Thời gian: {response_time:.3f} giây")
        else:
            failure_count += 1
            print(f"❌ Lỗi khi tạo record {i} - Status: {response.status_code}, Nội dung: {response.json()}")
            continue

    except requests.exceptions.ConnectionError as e:
        print(f"🚫 Không thể kết nối đến server ở record {i}. Lỗi: {e}")
        break
    except Exception as e:
        print(f"🚫 Lỗi không xác định ở record {i}: {e}")
        break

# Sau khi chạy xong hoặc dừng lại, in thống kê
print("\n🎯 --- Thống kê kết quả ---")
print(f"Số request thành công: {success_count}")
print(f"Số request thất bại: {failure_count}")
print(f"Tổng thời gian gửi: {total_time:.2f} giây")
if success_count > 0:
    print(f"⏱️ Thời gian trung bình mỗi request: {total_time / success_count:.3f} giây")
    print(f"⚡ Throughput: {success_count / total_time:.2f} requests/giây")
else:
    print("❌ Không có request nào thành công để tính hiệu năng.")
