import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Streamlit Data Visualization", page_icon="📊", layout="wide")

st.title("📊 แบบฝึกหัด Streamlit Data Visualization & Deployment")

# 1. จัดเตรียม Dataset
@st.cache_data
def load_data():
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Category': ['Electronics', 'Clothing', 'Electronics', 'Clothing', 'Food', 'Food', 'Electronics', 'Clothing', 'Food', 'Electronics', 'Clothing', 'Food'],
        'Sales': [15000, 12000, 18000, 13000, 9000, 11000, 22000, 15000, 10500, 25000, 19000, 14000],
        'Profit': [3000, 2000, 4000, 2500, 1500, 1800, 5000, 3200, 2000, 6000, 4500, 3000]
    }
    return pd.DataFrame(data)

df = load_data()

# แสดงตารางข้อมูลเบื้องต้น
st.subheader("📋 ตารางข้อมูลตัวอย่าง (Dataset)")
st.table(df)

# 2. Interactive Widget (ตัวกรองข้อมูล - ทำงานร่วมกับ Sidebar)
st.sidebar.header("⚙️ Interactive Controls")
selected_category = st.sidebar.selectbox(
    "เลือกหมวดหมู่สินค้า (Category):",
    options=['All'] + list(df['Category'].unique())
)

# กรองข้อมูลตาม Widget ที่ผู้ใช้เลือก
if selected_category != 'All':
    filtered_df = df[df['Category'] == selected_category]
else:
    filtered_df = df

st.write(f"แสดงข้อมูลสำหรับหมวดหมู่: **{selected_category}**")
st.table(filtered_df)

# 3. สร้างกราฟอย่างน้อย 2 กราฟ
st.subheader("📈 ส่วนแสดงผลกราฟวิเคราะห์ข้อมูล")

col1, col2 = st.columns(2)

with col1:
    st.write("**กราฟที่ 1: เปรียบเทียบยอดขาย (Sales) ในแต่ละเดือน**")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=filtered_df, x='Month', y='Sales', marker='o', color='blue', ax=ax1, linewidth=2.5)
    ax1.set_title("Sales Trend")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with col2:
    st.write("**กราฟที่ 2: เปรียบเทียบกำไร (Profit) แยกตามเดือน**")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=filtered_df, x='Month', y='Profit', palette='viridis', ax=ax2, hue='Month', legend=False)
    ax2.set_title("Profit by Month")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Profit ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
