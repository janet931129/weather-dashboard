import requests
import streamlit as st
import pandas as pd
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.title("🌤 台灣氣象資料 Dashboard")

API_KEY = st.secrets["CWA_API_KEY"]
CITY = st.selectbox("選擇城市", ["Taipei", "Taichung", "Kaohsiung"])

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
