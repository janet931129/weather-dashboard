import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "你的API_KEY"
CITY = "Taipei"

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

res = requests.get(url, verify=False)
data = res.json()

print("=== API 測試回傳 ===")
print(data)
