import requests

# URL ของ API endpoint
url = "http://10.53.99.234:80/publish/"

# ข้อมูลที่จะส่ง
data = {
    "message": "Teast"
}

# ทำการส่ง POST request
response = requests.post(url, json=data)

# แสดง response
print(response.status_code)
print(response.json())
