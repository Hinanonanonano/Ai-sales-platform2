import streamlit as st
from openai import OpenAI  # 用 openai library 兼容 Grok

# ===== 設定頁面 =====
st.set_page_config(page_title="AI Sales Outsourcing Platform", page_icon="🚀")
st.title("🚀 AI-Powered Sales Outsourcing Service")
st.markdown("### 提交你的銷售需求，Grok AI 即刻生成完整 outreach 方案（低成本、高轉化）")

# ===== Grok API 設定 =====
client = OpenAI(
    api_key=st.secrets["GROK_API_KEY"],  # 你嘅 Grok key
    base_url="https://api.x.ai/v1"
)

# ===== 客戶輸入表單 =====
with st.form("sales_request"):
    st.subheader("1. 你的產品/服務資料")
    product_name = st.text_input("產品/服務名稱")
    product_desc = st.text_area("詳細描述（越詳細 Grok 生成越準）")
    price_range = st.text_input("價格範圍（e.g. HK$500-2000）")
    
    st.subheader("2. 目標客戶")
    target_industry = st.text_input("目標行業（e.g. 餐飲、電商、地產）")
    target_location = st.text_input("目標地區（e.g. 香港、廣東、上海）")
    target_company_size = st.selectbox("公司規模", ["1-10人", "11-50人", "51-200人", "200人以上"])
    monthly_leads_goal = st.number_input("每月想要幾多 qualified leads？", min_value=10, max_value=1000, value=50)
    
    contact_name = st.text_input("你的姓名")
    contact_email = st.text_input("你的 Email（會記錄方便跟進）")
    contact_phone = st.text_input("電話（可選）")
    
    submitted = st.form_submit_button("提交需求 → Grok AI 即刻生成方案")

# ===== Grok AI 生成邏輯 =====
if submitted:
    if not product_desc or not target_industry or not contact_email:
        st.error("請填晒必填項目！")
    else:
        with st.spinner("Grok 喺度生成緊完整 sales scheme...（30-60秒）"):
            prompt = f"""
            你係專業 B2B sales outsourcing expert，用繁體中文回應。
            客戶產品：{product_name}
            描述：{product_desc}
            價格：{price_range}
            目標客戶：{target_industry} 行業，位於 {target_location}，公司規模 {target_company_size}
            每月目標：{monthly_leads_goal} 個 qualified leads
            
            請生成：
            1. 5 封 cold email 序列（第1封介紹，第2-5封 follow-up），每封 personalized、價值導向、短小精悍。
            2. 一份電話 sales script（開場、白話、處理異議、closing）。
            3. Lead generation 建議（LinkedIn search queries、網站來源）。
            4. 預計成本同時間表（每月 HK$XXXX，首月 setup）。
            用 markdown 格式輸出，內容實用、轉化率高。
            """
            
            response = client.chat.completions.create(
                model="grok-4-fast-reasoning",  # SuperGrok 用戶可以用 grok-4，如果唔得試 grok-3 或 grok-beta
                messages=[
                    {"role": "system", "content": "你係頂尖 B2B sales expert，用繁體中文回應。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
        
        st.success("方案生成完成！")
        st.markdown("### 📧 Grok 生成嘅 Sales Scheme")
        st.markdown(result)
        
        st.info(f"客戶資料已記錄：{contact_name} ({contact_email})")
        st.balloons()  # 加個慶祝效果

# ===== Sidebar 公司資訊 =====
with st.sidebar:
    st.markdown("### 關於我哋")
    st.write("AI-first Sales Outsourcing Agency")
    st.write("💼 Virtual office + 全 Grok AI 團隊")
    st.write("📈 專攻 cold outreach & lead gen")
    st.write("💰 低成本起步，scale 無上限")
    st.write("聯絡：your@email.com")

st.caption("Powered by Grok API | 2026 MVP v2.0 - 專為香港用戶優化")
