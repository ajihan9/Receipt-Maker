import streamlit as st
import datetime

# 1. 세션 상태 초기화 (입력한 영수증 항목들을 저장하는 공간)
if 'receipt_items' not in st.session_state:
    st.session_state.receipt_items = []

# 2. 메인 타이틀
st.title("🧾 가상 영수증 제조기")
st.write("이번 달 나의 소비, 혹은 감정을 영수증으로 뽑아보세요!")

# 3. 데이터 입력 폼 (Streamlit UI)
with st.form("input_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        item_name = st.text_input("항목 이름", placeholder="예: 퇴사 충동 억제 비용")
    with col2:
        item_price = st.number_input("금액 (원)", min_value=0, step=1000)
    
    submitted = st.form_submit_button("항목 추가하기")
    
    if submitted and item_name:
        # 입력된 데이터를 세션 상태에 추가
        st.session_state.receipt_items.append({"이름": item_name, "금액": item_price})
        st.success(f"'{item_name}' 항목이 추가되었습니다.")

st.write("---")

# 4. 영수증 디자인 및 출력 구역
if st.session_state.receipt_items:
    
    # 영수증 감성을 살리는 커스텀 CSS
    receipt_style = """
    <style>
    .receipt-box {
        background-color: white;
        padding: 30px 20px;
        width: 320px;
        margin: 0 auto;
        border: 1px solid #ccc;
        box-shadow: 2px 4px 15px rgba(0,0,0,0.1);
        font-family: 'Courier New', Courier, monospace;
        color: black;
        /* 영수증 하단 지그재그 패턴 효과 */
        background-image: radial-gradient(circle at 10px 0, transparent 10px, white 11px);
        background-size: 20px 20px;
        background-repeat: repeat-x;
        background-position: bottom;
    }
    .receipt-header {
        text-align: center;
        border-bottom: 2px dashed black;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }
    .receipt-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .receipt-total {
        border-top: 2px dashed black;
        margin-top: 15px;
        padding-top: 15px;
        font-weight: bold;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
    }
    .barcode {
        text-align: center;
        margin-top: 20px;
        font-size: 24px;
        letter-spacing: 2px;
    }
    </style>
    """
    
    # 현재 날짜 가져오기
    today = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    
    # HTML 뼈대 조립하기
    html_content = f"<div class='receipt-box'>"
    html_content += f"<div class='receipt-header'><h2>MY RECEIPT</h2><p>{today}</p></div>"
    
    total_sum = 0
    # 추가된 항목들을 반복문으로 출력
    for item in st.session_state.receipt_items:
        formatted_price = f"{item['금액']:,}" # 천 단위 콤마 추가
        html_content += f"<div class='receipt-item'><span>{item['이름']}</span><span>{formatted_price}</span></div>"
        total_sum += item['금액']
        
    formatted_total = f"{total_sum:,}"
    html_content += f"<div class='receipt-total'><span>TOTAL</span><span>{formatted_total}</span></div>"
    
    # 바코드 느낌의 장식 추가
    html_content += "<div class='barcode'>|||||| ||| || ||||</div>"
    html_content += "<div style='text-align:center; font-size:12px; margin-top:5px;'>THANK YOU</div>"
    html_content += "</div>"
    
    # 완성된 영수증 렌더링 (CSS 포함)
    st.markdown(receipt_style + html_content, unsafe_allow_html=True)
    
    # 초기화 버튼
    st.write("")
    if st.button("모두 지우기"):
        st.session_state.receipt_items = []
        st.rerun()

else:
    st.info("👆 위에서 항목을 추가하면 여기에 예쁜 영수증이 완성됩니다.")
