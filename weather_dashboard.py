import requests
import streamlit as st
import pandas as pd

st.title("🌤 台灣氣象資料 Dashboard")

API_KEY = st.secrets["CWA_API_KEY"]
cities = [
    "嘉義縣","新北市","嘉義市","新竹縣","新竹市","臺北市","臺南市","宜蘭縣",
    "苗栗縣","雲林縣","花蓮縣","臺中市","臺東縣","桃園市","南投縣","高雄市",
    "金門縣","屏東縣","基隆市","澎湖縣","彰化縣","連江縣"
]
CITY = st.selectbox("選擇城市", cities)

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

def fetch_weather(url, retries=3):
    for _ in range(retries):
        try:
            res = requests.get(url, verify=False, timeout=5)
            if res.status_code == 200:
                return res.json()
        except requests.RequestException:
            continue
    return {}

data = fetch_weather(url)
locations = data.get("records", {}).get("location", [])
if not locations:
    locations = [{}]  # 空資料也不會報錯

location = locations[0]

st.subheader(f"{location.get('locationName','')} — 36 小時天氣預報")

df = pd.DataFrame([
    {"項目": el.get("elementName", ""),
     "值": el.get("time", [{}])[0].get("parameter", {}).get("parameterName", "")}
    for el in location.get("weatherElement", [])
])
st.table(df)
