import os
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. ตั้งค่าหน้าเว็บแบบ Wide Mode
st.set_page_config(
    page_title="SCOMS Proactive Dashboard",
    page_icon="🟢",
    layout="wide"
)

# 2. Custom CSS ตกแต่ง UI
st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
        color: #1A1A1A;
        font-family: 'Inter', 'Kanit', sans-serif;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    .full-width-banner {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        margin-top: -3.5rem;
        background: linear-gradient(135deg, #0F3822 0%, #1B5636 50%, #2D6A4F 100%);
        padding: 12px 0;
        box-shadow: 0 10px 30px rgba(15, 56, 34, 0.35);
        margin-bottom: 25px;
        border-bottom: 3px solid rgba(163, 230, 53, 0.4);
    }
    
    .dashboard-content {
        padding: 0 2rem;
    }

    div[data-testid="stColumn"] > div,
    div[data-testid="stColumn"] div[data-testid="stVerticalBlock"],
    div[data-testid="stColumn"] div[data-testid="stVerticalBlockBorderWrapper"] {
        gap: 0px !important;
    }
    div[data-testid="stColumn"] [data-testid="stElementContainer"] {
        margin-bottom: 0px !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #EAECEF;
        border-bottom: none;
        padding: 16px 18px 8px 18px;
        border-top-left-radius: 14px !important;
        border-top-right-radius: 14px !important;
        border-bottom-left-radius: 0px !important;
        border-bottom-right-radius: 0px !important;
    }
    div[data-testid="stMetric"] label {
        color: #6C757D !important;
        font-size: 0.85rem !important;
        font-weight: 500;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0F3822 !important;
        font-weight: 700 !important;
        font-size: 1.9rem !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #0F3822 0%, #1B5636 100%);
        color: white;
        padding: 14px 18px 8px 18px;
        border-top-left-radius: 14px !important;
        border-top-right-radius: 14px !important;
        border-bottom-left-radius: 0px !important;
        border-bottom-right-radius: 0px !important;
    }
    .hero-card h3 {
        color: #A3E635 !important;
        margin: 0 0 2px 0;
        font-size: 0.9rem;
    }
    .hero-card h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .hero-card p {
        color: #D1E7DD;
        margin-top: 2px;
        margin-bottom: 0px;
        font-size: 0.75rem;
    }

    .aging-card {
        background-color: #FFFFFF;
        border: 1px solid #EAECEF;
        border-bottom: none;
        padding: 12px 4px 12px 4px !important;
        text-align: center;
        border-top-left-radius: 12px !important;
        border-top-right-radius: 12px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .aging-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 4px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
        white-space: nowrap;
    }
    .aging-value {
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.0 !important;
        margin: 2px 0 0 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stColumn"] .stButton > button {
        border-top-left-radius: 0px !important;
        border-top-right-radius: 0px !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        border: 1px solid #EAECEF !important;
        border-top: 1px solid #F1F3F5 !important;
        background-color: #FFFFFF !important;
        color: #495057 !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        margin-top: 0px !important;
        padding: 3px 4px !important;
        min-height: 28px !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stColumn"] .stButton > button:hover {
        background-color: #E8F5E9 !important;
        color: #0F3822 !important;
        border-color: #A3E635 !important;
    }

    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #111827;
        margin-top: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

SUMMARY_CSV = "summary_report.csv"

if not os.path.exists(SUMMARY_CSV):
    st.error(f"❌ ไม่พบไฟล์ `{SUMMARY_CSV}` กรุณารัน `py fetch_scoms.py` ใน PowerShell ก่อน")
    st.stop()

# กำหนดชื่อกองงานแบบไม่มีคำว่าโซนสี
TEAM_1 = "สมุทรสาคร กองงานที่ 1 : เกียรติศักดิ์ 0900033226 - ณรงค์ฤทธิ์ 0804285632 - พลพล 0840018669"
TEAM_2 = "สมุทรสาคร กองงานที่ 2 : ชานนท์ 0875775205 - อนุพงษ์ 0972753428 - สุศคาม 0639705127 - ณรงค์ฤทธิ์ 0804285632"

# ฟังก์ชันย่อชื่อ OLT ให้กระชับขึ้น
def shorten_olt_name(name):
    s = str(name).strip()
    if "NT1_SiteNT2_" in s:
        s = s.replace("NT1_SiteNT2_", "IP:")
    if len(s) > 28:
        return s[:25] + "..."
    return s

# ฟังก์ชันแยก OLT ตามพื้นที่
def assign_team_by_olt(olt):
    olt_str = str(olt).lower()
    
    team1_specific = [
        'ยกกระบัตร', 'ฮาแพง', 'กาหลง', 'บ้านแพ้ว คลอง', 'บ้านแพ้ว_คลอง', 
        'ชัยมงคล', 'วัดหนองสองห้อง'
    ]
    if any(k in olt_str for k in team1_specific):
        return TEAM_1
        
    team2_keywords = [
        'อ้อมน้อย', 'กระทุ่มแบน', 'บางปลา', 'วิเศษสุข', 
        'สินสาคร', 'สมุทรสาคร_c600', 'สมุทรสาคร2',
        'คอกกระบือ', 'บางปิ้ง', 'สค.สมุทรสาคร', 'พันท้าย', 
        'หรรษา', 'เอเชียนคร', 'หนองนกไข่',
        'olt outdoor', 
        'om noi', 'krathum', 'bang pla'
    ]
    
    if any(k in olt_str for k in team2_keywords):
        return TEAM_2
    else:
        return TEAM_1

# --- Dialog: แสดงรายละเอียดวงจรทั่วไป ---
@st.dialog("📋 รายละเอียดวงจร", width="large")
def show_details_dialog(title, detail_df):
    st.markdown(f"### รายการ: **{title}**")
    
    search_kw = st.text_input("🔍 ค้นหาหมายเลข / OLT / ข้อมูลในตาราง:", placeholder="พิมพ์ค้นหา...", key=f"search_{title}")
    
    filtered_df = detail_df.copy()
    if search_kw:
        filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_kw, case=False)).any(axis=1)]

    st.markdown(f"พบทั้งหมด **{len(filtered_df)}** รายการ")
    
    calc_height = min(450, max(130, (len(filtered_df) + 1) * 38 + 20))
    
    display_df = filtered_df.copy()
    display_df['ลำดับ'] = range(1, len(display_df) + 1)

    cols_order = ['ลำดับ', 'หมายเลขวงจร', 'กองงาน', 'Rx (dBm)', 'สถานะงาน', 'OLT', 'วันที่', 'สถานะสัญญาณ']
    available_cols = [c for c in cols_order if c in display_df.columns]

    st.dataframe(
        display_df[available_cols],
        use_container_width=True,
        hide_index=True,
        height=calc_height,
        column_config={
            "ลำดับ": st.column_config.NumberColumn("ลำดับ", width="small"),
            "หมายเลขวงจร": st.column_config.TextColumn("หมายเลขวงจร", width="medium"),
            "กองงาน": st.column_config.TextColumn("กองงานผู้รับผิดชอบ", width="large"),
            "Rx (dBm)": st.column_config.NumberColumn("Rx (dBm)", format="%.2f dBm", width="small"),
            "สถานะงาน": st.column_config.TextColumn("สถานะการดำเนินงาน", width="medium"),
            "OLT": st.column_config.TextColumn("OLT", width="medium"),
            "วันที่": st.column_config.TextColumn("วันที่", width="medium"),
            "สถานะสัญญาณ": st.column_config.TextColumn("สถานะสัญญาณ", width="small"),
        }
    )

# --- Dialog: แสดงข้อมูลกองงานผู้รับผิดชอบ (WOCODE) พร้อมกราฟ OLT แนวตั้ง ---
@st.dialog("👷 รายละเอียดข้อมูลกองงานผู้รับผิดชอบ (WOCODE)", width="large")
def show_wocode_dialog(df):
    st.markdown("### 📋 ตรวจสอบกองงานและระยะเวลาจ่ายงานตามพื้นที่")

    unique_teams = [TEAM_1, TEAM_2]
    selected_team = st.selectbox("📌 เลือกกองงาน:", unique_teams, key="dlg_select_team")

    if selected_team:
        st.markdown(f'<div style="background:#E8F5E9; padding:10px; border-radius:8px; margin-bottom:10px; color:#0F3822;"><b>ข้อมูลกองงาน</b><br>{selected_team}</div>', unsafe_allow_html=True)

        team_df = df[df['กองงาน'] == selected_team].copy()

        st.write(f"จำนวนวงจรในความรับผิดชอบ: **{len(team_df)}** รายการ")

        if not team_df.empty and 'OLT' in team_df.columns:
            st.markdown("##### 📊 สรุป OLT ทั้งหมดที่พบปัญหาในพื้นที่นี้ (แนวตั้ง)")
            olt_counts = team_df['OLT'].value_counts().reset_index()
            olt_counts.columns = ['OLT', 'จำนวนวงจร']
            olt_counts['Short_OLT'] = olt_counts['OLT'].apply(shorten_olt_name)
            
            fig = px.bar(olt_counts, x='Short_OLT', y='จำนวนวงจร',
                         color_discrete_sequence=['#1B5636'], text='จำนวนวงจร',
                         hover_data={'OLT': True, 'Short_OLT': False})
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_title="", yaxis_title="",
                xaxis={'categoryorder':'total descending', 'tickangle': -45},
                margin=dict(t=30, b=50, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        show_cols = ['ลำดับ', 'หมายเลขวงจร', 'สถานะงาน', 'Rx (dBm)', 'OLT', 'วันที่']
        avail = [c for c in show_cols if c in team_df.columns]
        if not avail:
            avail = list(team_df.columns)

        display_team_df = team_df.copy()
        display_team_df['ลำดับ'] = range(1, len(display_team_df) + 1)

        st.dataframe(
            display_team_df[avail],
            use_container_width=True,
            hide_index=True,
            height=280,
            column_config={
                "ลำดับ": st.column_config.NumberColumn("ลำดับ", width="small"),
                "หมายเลขวงจร": st.column_config.TextColumn("หมายเลขวงจร", width="medium"),
                "สถานะงาน": st.column_config.TextColumn("สถานะงาน", width="medium"),
                "Rx (dBm)": st.column_config.NumberColumn("Rx (dBm)", format="%.2f dBm", width="small"),
                "OLT": st.column_config.TextColumn("OLT", width="medium"),
                "วันที่": st.column_config.TextColumn("วันที่", width="medium"),
            }
        )

try:
    df = pd.read_csv(SUMMARY_CSV, encoding="utf-8-sig")
    df = df.dropna(how='all').dropna(how='all', axis=1)

    cols = list(df.columns)

    col_circuit = cols[2] if len(cols) > 2 else cols[0]
    
    col_rx_power = None
    for col in cols:
        s = df[col].astype(str).str.extract(r'(-?\d+\.?\d*)')[0]
        num_s = pd.to_numeric(s, errors='coerce')
        valid_count = ((num_s >= -45) & (num_s <= 0)).sum()
        if valid_count > len(df) * 0.3:
            col_rx_power = col
            break

    if col_rx_power is None:
        col_rx_power = cols[3] if len(cols) > 3 else cols[0]

    col_olt = None
    for col in cols:
        if any(k in str(col).lower() for k in ["olt", "โหนด", "node"]):
            col_olt = col
            break
    if col_olt is None:
        col_olt = cols[5] if len(cols) > 5 else (cols[4] if len(cols) > 4 else cols[0])

    col_date = cols[6] if len(cols) > 6 else (cols[3] if len(cols) > 3 else cols[0])

    extracted_rx = df[col_rx_power].astype(str).str.extract(r'(-?\d+\.?\d*)')[0]
    df['Rx_Num'] = pd.to_numeric(extracted_rx, errors='coerce')

    def get_signal_status(val):
        if pd.isna(val): 
            return None
        if val > -11.0:
            return "ต่ำกว่ามาตรฐาน"
        elif -30.0 <= val < -28.0:
            return "เกินมาตรฐาน"
        elif val < -30.0:
            return "วิกฤต (<= -30)"
        else:
            return None

    df['สถานะสัญญาณ'] = df['Rx_Num'].apply(get_signal_status)
    df = df[df['สถานะสัญญาณ'].notna()].copy()

    col_work_status = None
    for col in cols:
        if any(k in str(col).lower() for k in ["สถานะงาน", "work_status", "job_status", "คืนงาน", "ปิดงาน"]):
            col_work_status = col
            break

    if col_work_status and col_work_status in df.columns:
        def standardize_status(val):
            val_str = str(val).strip()
            if "คืน" in val_str:
                return "คืนงาน"
            elif "ปิด" in val_str:
                return "ปิดงาน"
            elif "> 4" in val_str or "มากกว่า 4" in val_str:
                return "จ่ายงาน > 4 วัน"
            elif "4" in val_str:
                return "จ่ายงาน 4 วัน"
            elif "3" in val_str:
                return "จ่ายงาน 3 วัน"
            elif "2" in val_str:
                return "จ่ายงาน 2 วัน"
            elif "1" in val_str:
                return "จ่ายงาน 1 วัน"
            return val_str

        df['สถานะงาน'] = df[col_work_status].apply(standardize_status)
    else:
        parsed_dates = pd.to_datetime(df[col_date], errors='coerce', dayfirst=True)
        max_dt = parsed_dates.max() if not parsed_dates.isna().all() else pd.Timestamp.now()
        days_diff = (max_dt - parsed_dates).dt.days.fillna(0).astype(int) + 1

        def assign_aging(d):
            if d == 1:
                return "จ่ายงาน 1 วัน"
            elif d == 2:
                return "จ่ายงาน 2 วัน"
            elif d == 3:
                return "จ่ายงาน 3 วัน"
            elif d == 4:
                return "จ่ายงาน 4 วัน"
            elif d > 4:
                return "จ่ายงาน > 4 วัน"
            else:
                return "จ่ายงาน 1 วัน"

        df['สถานะงาน'] = days_diff.apply(assign_aging)

    total_count = len(df)
    low_count = len(df[df['สถานะสัญญาณ'] == "ต่ำกว่ามาตรฐาน"])
    range_count = len(df[df['สถานะสัญญาณ'] == "เกินมาตรฐาน"])
    crit_count = len(df[df['สถานะสัญญาณ'] == "วิกฤต (<= -30)"])

    clean_table = pd.DataFrame()
    clean_table['ลำดับ'] = range(1, len(df) + 1)
    clean_table['หมายเลขวงจร'] = df[col_circuit].values
    
    clean_table['OLT'] = df[col_olt].values
    clean_table['กองงาน'] = clean_table['OLT'].apply(assign_team_by_olt)

    clean_table['Rx (dBm)'] = df['Rx_Num'].values
    clean_table['สถานะงาน'] = df['สถานะงาน'].values
    clean_table['วันที่'] = df[col_date].values
    clean_table['สถานะสัญญาณ'] = df['สถานะสัญญาณ'].values

    banner_filename = "S__4702368.jpg"
    downloads_banner = os.path.join(os.path.expanduser('~'), 'Downloads', banner_filename)
    
    active_banner = None
    if os.path.exists(banner_filename):
        active_banner = banner_filename
    elif os.path.exists(downloads_banner):
        active_banner = downloads_banner

    st.markdown('<div class="full-width-banner">', unsafe_allow_html=True)
    if active_banner:
        st.image(active_banner, use_container_width=True)
    else:
        uploaded_banner = st.file_uploader("🖼️ อัปโหลดรูปแบนเนอร์:", type=['jpg', 'jpeg', 'png'])
        if uploaded_banner is not None:
            st.image(uploaded_banner, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)

    col_btn_wocode, _ = st.columns([1.5, 4])
    with col_btn_wocode:
        if st.button("👷 ตรวจสอบข้อมูลกองงาน (WOCODE)", use_container_width=True, type="primary"):
            show_wocode_dialog(clean_table)

    st.markdown("<br>", unsafe_allow_html=True)

    m_hero, m1, m2, m3 = st.columns([1.2, 1, 1, 1])

    with m_hero:
        st.markdown(f"""
        <div class="hero-card">
            <h3>วงจรที่ไม่ผ่านเกณฑ์</h3>
            <h1>{total_count}</h1>
            <p>รายการที่ต้องติดตามแก้ไข</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("รายละเอียด", key="btn_all", use_container_width=True):
            show_details_dialog("วงจรที่ไม่ผ่านเกณฑ์ทั้งหมด", clean_table)

    with m1:
        pct_low = (low_count / total_count * 100) if total_count > 0 else 0
        st.metric("ต่ำกว่ามาตรฐาน (> -11)", f"{low_count}", f"{pct_low:.1f}%")
        if st.button("รายละเอียด", key="btn_low", use_container_width=True):
            sub_df = clean_table[clean_table['สถานะสัญญาณ'] == "ต่ำกว่ามาตรฐาน"]
            show_details_dialog("ต่ำกว่ามาตรฐาน (> -11)", sub_df)

    with m2:
        pct_range = (range_count / total_count * 100) if total_count > 0 else 0
        st.metric("เกินมาตรฐาน (-28 ถึง -30)", f"{range_count}", f"{pct_range:.1f}%")
        if st.button("รายละเอียด", key="btn_range", use_container_width=True):
            sub_df = clean_table[clean_table['สถานะสัญญาณ'] == "เกินมาตรฐาน"]
            show_details_dialog("เกินมาตรฐาน (-28 ถึง -30)", sub_df)

    with m3:
        pct_crit = (crit_count / total_count * 100) if total_count > 0 else 0
        st.metric("วิกฤต (<= -30)", f"{crit_count}", f"{pct_crit:.1f}%", delta_color="inverse")
        if st.button("รายละเอียด", key="btn_crit", use_container_width=True):
            sub_df = clean_table[clean_table['สถานะสัญญาณ'] == "วิกฤต (<= -30)"]
            show_details_dialog("วิกฤต (<= -30)", sub_df)

    st.markdown('<div class="section-header">📌 สถานะการติดตามงาน (Aging Work Status)</div>', unsafe_allow_html=True)

    aging_configs = [
        {"key": "จ่ายงาน 1 วัน", "label": "จ่ายงาน 1 วัน", "dot": "●", "dot_color": "#FFD8A8", "val_color": "#E67E22"},
        {"key": "จ่ายงาน 2 วัน", "label": "จ่ายงาน 2 วัน", "dot": "●", "dot_color": "#FFA94D", "val_color": "#E67E22"},
        {"key": "จ่ายงาน 3 วัน", "label": "จ่ายงาน 3 วัน", "dot": "●", "dot_color": "#FF922B", "val_color": "#D35400"},
        {"key": "จ่ายงาน 4 วัน", "label": "จ่ายงาน 4 วัน", "dot": "●", "dot_color": "#E8590C", "val_color": "#C0392B"},
        {"key": "จ่ายงาน > 4 วัน", "label": "จ่ายงาน > 4 วัน", "dot": "●", "dot_color": "#8A2500", "val_color": "#8A2500"},
        {"key": "คืนงาน", "label": "คืนงาน", "dot": "●", "dot_color": "#1C7ED6", "val_color": "#1C7ED6"},
        {"key": "ปิดงาน", "label": "ปิดงาน", "dot": "●", "dot_color": "#2F9E44", "val_color": "#2F9E44", "suffix": " ✔"},
    ]

    ag_cols = st.columns(7)

    for idx, cfg in enumerate(aging_configs):
        cnt = (clean_table['สถานะงาน'] == cfg["key"]).sum()
        suffix = cfg.get("suffix", "")

        with ag_cols[idx]:
            st.markdown(f"""
            <div class="aging-card">
                <div class="aging-title">
                    <span style="color: {cfg['dot_color']}; font-size: 1.0rem;">{cfg['dot']}</span>
                    <span>{cfg['label']}</span>
                </div>
                <div class="aging-value" style="color: {cfg['val_color']};">
                    {cnt}{suffix}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("รายละเอียด", key=f"btn_ag_{idx}", use_container_width=True):
                sub_df = clean_table[clean_table['สถานะงาน'] == cfg["key"]]
                show_details_dialog(f"สถานะ: {cfg['label']}", sub_df)

    st.markdown("<br>", unsafe_allow_html=True)

    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.subheader("📊 สัดส่วนวงจรที่ไม่ผ่านเกณฑ์")
        fig_donut = px.pie(
            df, 
            names='สถานะสัญญาณ', 
            hole=0.6,
            color='สถานะสัญญาณ',
            color_discrete_map={
                "ต่ำกว่ามาตรฐาน": "#3B82F6",
                "เกินมาตรฐาน": "#F59E0B",
                "วิกฤต (<= -30)": "#EF4444"
            }
        )
        fig_donut.update_traces(textinfo='percent+label', hoverinfo='label+value')
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c_right:
        st.subheader("📊 OLT ทั้งหมดที่พบปัญหา (แนวตั้ง)")
        if col_olt in df.columns:
            olt_df = df[col_olt].value_counts().reset_index()
            olt_df.columns = ['OLT', 'จำนวนวงจร']
            olt_df['Short_OLT'] = olt_df['OLT'].apply(shorten_olt_name)

            fig_bar = px.bar(
                olt_df, 
                x='Short_OLT', 
                y='จำนวนวงจร',
                color_discrete_sequence=['#EF4444'],
                text='จำนวนวงจร',
                hover_data={'OLT': True, 'Short_OLT': False}
            )
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(
                xaxis_title="",
                yaxis_title="",
                xaxis={'categoryorder':'total descending', 'tickangle': -45},
                margin=dict(t=30, b=50, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=380
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")