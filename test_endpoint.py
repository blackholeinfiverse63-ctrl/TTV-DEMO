import urllib.request
import json

# Test the /generate-video endpoint
url = 'http://127.0.0.1:5000/generate-video'
data = json.dumps({'prompt': 'A cat playing in a garden'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print('Status Code:', response.getcode())
        print('Response:', json.loads(response.read().decode('utf-8')))
except Exception as e:
    print('Error:', e)