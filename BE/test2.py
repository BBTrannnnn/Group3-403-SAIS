import requests
import json
import time
from datetime import datetime, timedelta
import random
from requests.exceptions import ConnectionError, ChunkedEncodingError

url = "http://127.0.0.1:5000/api/customers"
headers = {'Content-Type': 'application/json'}

num_records_to_create = 1000
success_count = 0
failure_count = 0
total_time = 0

def random_date(start_year=1970, end_year=2010):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def random_gender():
    return random.choice(['Nam', 'Nữ'])

for i in range(1, num_records_to_create + 1):
    payload_data = {
        "name": f"Người Dùng {i}",
        "day_of_birth": random_date(),
        "sex": random_gender(),
        "phone_number": f"090{i:07}",  # Đảm bảo không trùng
        "cccd": f"0123{i:06}",         # CCCD giả định
        "email": f"user{i}@example.com",
        "address": f"Số {i} Đường ABC, Quận XYZ",
        "medical_history": "Không có",
        "vaccine_reaction_history": "Không rõ"
    }

    payload = json.dumps(payload_data)

    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=payload)
        response_time = time.time() - start_time
        total_time += response_time

        if response.status_code in [200, 201]:
            success_count += 1
            print(f"✅ Record {i}: Thành công | Time: {response_time:.3f}s")
        else:
            try:
                print(f"❌ Record {i}: Status {response.status_code}, Response: {response.json()}")
            except ValueError:
                print(f"❌ Record {i}: Status {response.status_code}, Response không phải JSON: {response.text}")
            failure_count += 1

    except (ConnectionError, ChunkedEncodingError) as e:
        print(f"❌ Record {i}: KHÔNG KẾT NỐI hoặc MẤT KẾT NỐI: {str(e)}")
        failure_count += 1

    # Tránh gửi liên tục làm server treo
    time.sleep(0.01)

# Tổng kết
print("\n🎯 --- KẾT QUẢ ---")
print(f"✅ Thành công: {success_count}")
print(f"❌ Thất bại: {failure_count}")
print(f"⏱️ Tổng thời gian: {total_time:.2f} giây")
