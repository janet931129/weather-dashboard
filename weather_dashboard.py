import requests
import streamlit as st
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="台灣天氣 Dashboard", layout="centered")

# ---- Title ----
st.markdown("<h1 style='text-align:center;'>🌤 台灣氣象資料 Dashboard</h1>", unsafe_allow_html=True)

API_KEY = st.secrets["CWA_API_KEY"]
cities = [
    "嘉義縣","新北市","嘉義市","新竹縣","新竹市","臺北市","臺南市","宜蘭縣",
    "苗栗縣","雲林縣","花蓮縣","臺中市","臺東縣","桃園市","南投縣","高雄市",
    "金門縣","屏東縣","基隆市","澎湖縣","彰化縣","連江縣"
]

CITY = st.selectbox("📍 選擇城市", cities)

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={CITY}"

def fetch_weather(url):
    try:
        res = requests.get(url, verify=False, timeout=8)
        return res.json() if res.status_code == 200 else {}
    except:
        return {}

data = fetch_weather(url)
locations = data.get("records", {}).get("location", [])
location = locations[0] if locations else {}

weather_data = location.get("weatherElement", [])

st.markdown(f"<h2 style='text-align:center;'>{CITY} — 36 小時天氣預報</h2>", unsafe_allow_html=True)
st.write("")

# ---- Parse Data ----
weather_dict = {
    item["elementName"]: item["time"][0]["parameter"]["parameterName"]
    for item in weather_data
}

Wx = weather_dict.get("Wx", "—")
PoP = weather_dict.get("PoP", "—")
MinT = weather_dict.get("MinT", "—")
MaxT = weather_dict.get("MaxT", "—")
CI = weather_dict.get("CI", "—")

# ------ UI Card Style (縮小版) ------
card_style = """
    padding:12px;
    border-radius:12px;
    margin-bottom:10px;
"""

title_style = "font-size:16px; margin-bottom:6px;"
value_style = "font-size:20px;"

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="{card_style} background:#F1F8FF">
        <h3 style="{title_style}">🌦 天氣狀況</h3>
        <p style="{
