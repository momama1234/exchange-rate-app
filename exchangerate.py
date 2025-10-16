import streamlit as st
import requests

st.set_page_config(page_title="อัตราแลกเปลี่ยนจาก USD", page_icon="💱", layout="centered")
st.title("อัตราแลกเปลี่ยนจาก USD")

# ดึง API Key จาก Secrets
API_KEY = st.secrets["EXCHANGE_API_KEY"]

BASE = "USD"
currencies = ["THB", "JPY", "EUR", "GBP", "AED"]

# เรียก API
def fetch_rates(base):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data

try:
    data = fetch_rates(BASE)
    rates = data["conversion_rates"]
    last_update = data.get("time_last_update_utc", "")

    # แสดงค่า USD → THB ใต้หัวข้อ
    thb_rate = rates.get("THB")
    if thb_rate:
        st.subheader(f"1 USD = {thb_rate:.2f} THB")

    st.divider()

    # ให้ผู้ใช้เลือกสกุลเงินอื่น
    target = st.selectbox("เลือกสกุลเงินอื่น", currencies, index=1)
    rate = rates.get(target)
    if rate:
        st.subheader(f"1 USD = {rate:.2f} {target}")
        st.caption(f"อัปเดตล่าสุด: {last_update}")

except Exception as e:
    st.error(f"ไม่สามารถดึงข้อมูลได้: {e}")
