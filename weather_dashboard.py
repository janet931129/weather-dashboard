import requests

API_KEY = "你的API_KEY"
CITY = "Taipei"
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

res = requests.get(url, verify=False)

print("HTTP 狀態碼:", res.status_code)
print("前500字回傳內容:", res.text[:500])
