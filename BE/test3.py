import requests
import json
import random
import time
from datetime import datetime, timedelta
from requests.exceptions import ConnectionError, ChunkedEncodingError

url = "http://127.0.0.1:5000/api/appointments"
headers = {'Content-Type': 'application/json'}

num_records_to_create = 1000
success_count = 0
failure_count = 0
total_time = 0

def random_date(start=1, end=60):
    return (datetime.today() + timedelta(days=random.randint(start, end))).strftime('%Y-%m-%d')

def random_time_slot():
    return random.choice([
        "07:00 - 08:00", "08:00 - 09:00", "09:00 - 10:00",
        "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"
    ])

def random_location():
    return random.choice([
        "Trạm Y tế Phường 1", "Trạm Y tế Phường 2",
        "Bệnh viện ABC", "TTVX Quốc Gia"
    ])

def random_dose():
    return random.choice(["Mũi 1", "Mũi 2", "Nhắc lại"])

for i in range(1, num_records_to_create + 1):
    payload_data = {
        "scheduled_date": random_date(),
        "time_slot": random_time_slot(),
        "location": random_location(),
        "id_customer": i,   
        "id_vaccine": i,    
        "dose_number": random_dose()
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
        print(f"❌ Record {i}: KHÔNG KẾT NỐI ĐƯỢC, BỎ QUA")
        failure_count += 1
    time.sleep(0.01)

print("\n🎯 --- KẾT QUẢ ---")
print(f"✅ Thành công: {success_count}")
print(f"❌ Thất bại: {failure_count}")
print(f"⏱️ Tổng thời gian: {total_time:.2f} giây")
