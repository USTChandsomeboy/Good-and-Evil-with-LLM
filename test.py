# 设置代理为http://127.0.0.1:10809
import os
import requests
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

try:
    response = requests.get('https://www.google.com')
    if response.status_code == 200:
        print("Successfully accessed Google.")
    else:
        print(f"Failed to access Google. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")