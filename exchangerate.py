import streamlit as st
import requests

st.set_page_config(page_title="อัตราแลกเปลี่ยนจาก USD", page_icon="💱", layout="centered")
st.title("อัตราแลกเปลี่ยนจาก USD")

API_KEY = "8f733be7ef8287a2b59f288f"
BASE = "USD"


currencies = ["THB", "JPY", "EUR", "GBP", "AED"]

# ดึงอัตราแลกเปลี่ยนของ BASE เพียงครั้งเดียว
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE}"
try:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()

    if data.get("result") != "success":
        st.error(f"API Error: {data}")
    else:
        rates = data.get("conversion_rates", {})

        # 1) แสดง 1 USD = THB 
        thb_rate = rates.get("THB")
        if thb_rate is not None:
            st.subheader(f"1 USD = {thb_rate:.2f} THB")
        else:
            st.warning("ไม่พบเรท THB ในข้อมูลที่ได้รับ")

        st.divider()

        # 2) เลือกสกุลเงินที่ต้องการดูเรทด้านล่าง (คงรูปแบบเดิม)
        target = st.selectbox("เลือกสกุลเงินอื่น", options=currencies, index=1)  # default JPY
        target_rate = rates.get(target)
        if target_rate is not None:
            st.subheader(f"1 USD = {target_rate:.2f} {target}")
            st.caption(f'อัปเดตล่าสุด: {data.get("time_last_update_utc","")}')
        else:
            st.error("ไม่พบข้อมูลสกุลเงินที่เลือก")

except requests.HTTPError as e:
    st.error(f"HTTP Error: {e}")
except requests.RequestException as e:
    st.error(f"Network Error: {e}")
except Exception as e:
    st.exception(e)
