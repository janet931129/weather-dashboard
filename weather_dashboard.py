import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "你的API_KEY"
CITY = "Taipei"

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

res = requests.get(url, verify=False)

print("HTTP Status:", res.status_code)
print("Response Text:", res.text[:500])  # 只印前500字
