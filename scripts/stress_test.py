import requests
import concurrent.futures
import time
import random

URL = "http://n8n-main:5678/webhook/industrial-data"

def send_request(i):
    payload = {
        "device_id": f"MACHINE-{random.randint(100, 999)}",
        "temperature": round(random.uniform(60.0, 95.0), 2),
        "status": random.choice(["OK", "WARNING", "CRITICAL"])
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"

print("Beggining test with 1k requests...")
start_time = time.time()

# 50 hilos en paralelo para simular carga real
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = list(executor.map(send_request, range(1000)))

end_time = time.time()

total_ok = results.count(200)
print(f"\n--- TEST RESULTS ---")
print(f"⏱️  Total time: {end_time - start_time:.2f} segundos")
print(f"✅ Successful (200 OK): {total_ok}")
print(f"❌ Failed: {1000 - total_ok}")
