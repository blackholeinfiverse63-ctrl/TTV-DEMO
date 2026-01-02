import urllib.request
import json
import time

# Test the /generate-video endpoint with multiple requests
url = 'http://127.0.0.1:5000/generate-video'
prompts = ['A cat playing in a garden', 'A dog running in the park', 'A bird flying in the sky']
num_requests = 3

times = []

for i in range(num_requests):
    data = json.dumps({'prompt': prompts[i % len(prompts)]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            end_time = time.time()
            duration = end_time - start_time
            times.append(duration)
            print(f'Request {i+1}: Status Code: {response.getcode()}, Time: {duration:.2f}s')
            resp_data = json.loads(response.read().decode('utf-8'))
            print('Response:', resp_data)
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        times.append(duration)
        print(f'Request {i+1}: Error: {e}, Time: {duration:.2f}s')

if times:
    avg_time = sum(times) / len(times)
    print(f'Average loading time: {avg_time:.2f}s')
    print(f'Min time: {min(times):.2f}s, Max time: {max(times):.2f}s')
    success_rate = sum(1 for t in times if t < 10) / len(times) * 100  # Assuming <10s is success
    print(f'Reliability: {success_rate:.1f}% successful requests')