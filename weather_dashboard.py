import requests
import streamlit as st
import pandas as pd
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.title("🌤 台灣氣象資料 Dashboard")

API_KEY = st.secrets["CWA_API_KEY"]
cities = [
    "嘉義縣","新北市","嘉義市","新竹縣","新竹市","臺北市","臺南市","宜蘭縣",
    "苗栗縣","雲林縣","花蓮縣","臺中市","臺東縣","桃園市","南投縣","高雄市",
    "金門縣","屏東縣","基隆市","澎湖縣","彰化縣","連江縣"
]

CITY = st.selectbox("選擇城市", cities)

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

# 重試機制
for i in range(3):
    try:
        res = requests.get(url, verify=False, timeout=5)
        if res.status_code == 200:
            break
    except requests.RequestException:
        pass
    time.sleep(1)
else:
    st.error("❌ API 連線失敗，請稍後再試")
    st.stop()

# 安全解析 JSON
try:
    data = res.json()
except ValueError:
    st.error("❌ API 回傳非 JSON，請檢查 API Key 或網路")
    st.stop()

records = data.get("records", {})
locations = records.get("location", [])

if not locations:
    st.error("❌ API 回傳空資料，請檢查 API Key 或城市名稱")
    st.stop()

location = locations[0]

st.subheader(f"{location['locationName']} — 36 小時天氣預報")

rows = []
for element in location.get("weatherElement", []):
    name = element.get("elementName", "")
    value = element.get("time", [{}])[0].get("parameter", {}).get("parameterName", "")
    rows.append({"項目": name, "值": value})

df = pd.DataFrame(rows)
st.table(df)
