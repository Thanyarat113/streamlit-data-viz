import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Dashboard ปริมาณขยะมูลฝอย", page_icon="🗑️", layout="wide")

st.title("🗑️ Dashboard แสดงปริมาณขยะมูลฝอย")
st.markdown("วิเคราะห์และแสดงผลข้อมูลจากระบบสถิติกลมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช (data.go.th)")

# 1. โหลดข้อมูลจริงจากไฟล์ Excel ที่อัปโหลดไว้
@st.cache_data
def load_data():
    # อ่านไฟล์ Excel ชื่อ untitled.xlsx ที่เราอัปขึ้น GitHub
    df = pd.read_excel('untitled.xlsx')
    return df

try:
    df = load_data()
    
    # แสดงตารางข้อมูลเบื้องต้น
    st.subheader("📋 ตารางข้อมูลปริมาณขยะมูลฝอย (Dataset)")
    st.dataframe(df, use_container_width=True)

    # 2. Interactive Widget (ตัวกรองข้อมูล)
    column_list = df.columns.tolist()
    
    st.sidebar.header("⚙️ Interactive Controls")
    selected_col = st.sidebar.selectbox("เลือกคอลัมน์สำหรับกรองข้อมูล:", options=column_list)
    unique_vals = df[selected_col].dropna().unique()
    selected_val = st.sidebar.selectbox(f"เลือกค่าใน {selected_col}:", options=['All'] + list(unique_vals))

    if selected_val != 'All':
        filtered_df = df[df[selected_col] == selected_val]
    else:
        filtered_df = df

    st.write(f"แสดงข้อมูลที่กรองจาก **{selected_col} = {selected_val}**")
    st.dataframe(filtered_df, use_container_width=True)

    # 3. สร้างกราฟอย่างน้อย 2 กราฟ
    st.subheader("📈 ส่วนแสดงผลกราฟวิเคราะห์ข้อมูล")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if len(numeric_cols) >= 1 and len(cat_cols) >= 1:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**กราฟที่ 1: เปรียบเทียบ {numeric_cols[0]} ตาม {cat_cols[0]}**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.barplot(data=filtered_df.head(10), x=cat_cols[0], y=numeric_cols[0], palette='viridis', ax=ax1, hue=cat_cols[0], legend=False)
            plt.xticks(rotation=45)
            st.pyplot(fig1)

        with col2:
            st.write(f"**กราฟที่ 2: แสดงการกระจายของข้อมูล {numeric_cols[0]}**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.histplot(data=filtered_df, x=numeric_cols[0], kde=True, color='crimson', ax=ax2)
            plt.xticks(rotation=45)
            st.pyplot(fig2)
    else:
        st.info("ไม่พบคอลัมน์ตัวเลขหรือข้อความที่เพียงพอสำหรับการสร้างกราฟอัตโนมัติ")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
