import requests
import streamlit as st
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


st.set_page_config(page_title="台灣氣象 Dashboard", layout="centered")
st.title("🌤 台灣氣象資料 Dashboard")

API_KEY = st.secrets["CWA_API_KEY"]

# 建議改成完整的縣市清單，這裡只示範三個
LOCATION = st.selectbox("選擇城市", ["Taipei", "Taichung", "Kaohsiung"])

url = (
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    f"?Authorization={API_KEY}&locationName={LOCATION}"
)

res = requests.get(url, verify=False)
data = res.json()

try:
    location = data["records"]["location"][0]
    st.subheader(f"{location['locationName']} — 36 小時天氣預報")
    rows = []
    for element in location["weatherElement"]:
        name = element["elementName"]
        # 取第一個 time 的 parameter 作示範
        value = element["time"][0]["parameter"]["parameterName"]
        rows.append({"項目": name, "值": value})
    df = pd.DataFrame(rows)
    st.table(df)
except Exception as e:
    st.error("資料解析錯誤，請檢查 API KEY 或格式。")
    st.write(e)
