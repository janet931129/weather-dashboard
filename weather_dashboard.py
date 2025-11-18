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

# ---- UI Section ----
st.markdown(f"<h2 style='text-align:center;'>{CITY} — 36 小時天氣預報</h2>", unsafe_allow_html=True)
st.write("")

# 轉成字典方便取值
weather_dict = {item["elementName"]: item["time"][0]["parameter"]["parameterName"]
                for item in weather_data}

Wx = weather_dict.get("Wx", "—")
PoP = weather_dict.get("PoP", "—")
MinT = weather_dict.get("MinT", "—")
MaxT = weather_dict.get("MaxT", "—")
CI = weather_dict.get("CI", "—")

# ---- Weather Display Cards ----
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="padding:18px;border-radius:10px;background:#F1F8FF">
        <h3>⛅️ 天氣狀況</h3>
        <p style="font-size:18px;">{Wx}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:18px;margin-top:15px;border-radius:10px;background:#FFF7E6">
        <h3>🌡 最高溫</h3>
        <p style="font-size:18px;">{MaxT} ℃</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="padding:18px;border-radius:10px;background:#E8FFF3">
        <h3>🌧 降雨機率</h3>
        <p style="font-size:18px;">{PoP}%</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:18px;margin-top:15px;border-radius:10px;background:#FFECEC">
        <h3>🌡 最低溫</h3>
        <p style="font-size:18px;">{MinT} ℃</p>
    </div>
    """, unsafe_allow_html=True)

# ---- Comfort Index ----
st.markdown("""
<div style="padding:18px;margin-top:20px;border-radius:10px;background:#F6F6F6">
    <h3>🧘‍♂️ 舒適度指數</h3>
    <p style="font-size:18px;">{CI}</p>
</div>
""".format(CI=CI), unsafe_allow_html=True)
