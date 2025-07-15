import requests
import json
import time

url = "http://127.0.0.1:5000/api/vaccines"
headers = {'Content-Type': 'application/json'}

num_records_to_create = 1000
success_count = 0
failure_count = 0
total_time = 0

for i in range(1, num_records_to_create + 1):
    payload_data = {
        "id": i,
        "name": f"Vaccine {i}",
        "description": "Test availability",
        "manufacturer": f"NSX {i}",
        "efficacy": 0.9,
        "side_effects": "Ít",
        "category": "Tự nguyện",
        "quantity": 100
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

    except requests.exceptions.ConnectionError:
        print(f"❌ Record {i}: KHÔNG KẾT NỐI ĐƯỢC, BỎ QUA")
        failure_count += 1

print("\n🎯 --- KẾT QUẢ ---")
print(f"✅ Thành công: {success_count}")
print(f"❌ Thất bại: {failure_count}")
print(f"⏱️ Tổng thời gian: {total_time:.2f} giây")
