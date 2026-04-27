import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="금융투자성향 퀴즈",
    page_icon="💰"
)

# =========================
# 세션 상태 초기화
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "menu" not in st.session_state:
    st.session_state.menu = "소개"


# =========================
# 캐싱 함수
# =========================
@st.cache_data(
    ttl=60 * 5,
    max_entries=3,
    show_spinner="퀴즈 데이터를 불러오는 중입니다..."
)
def load_quiz_data(file_path):
    data = pd.read_csv(file_path)
    return data


# =========================
# 함수
# =========================
def reset_quiz():
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.answers = {}


def logout():
    st.session_state.login = False
    st.session_state.username = ""
    st.session_state.menu = "소개"
    reset_quiz()


def go_page(page_name):
    st.session_state.menu = page_name


def calculate_result(score):
    if score <= 18:
        return "안정형", "원금 손실을 매우 싫어하며 안정적인 금융상품을 선호하는 유형입니다.", ["예금", "적금", "채권", "저위험 상품"]
    elif score <= 27:
        return "안정추구형", "안정성을 중요하게 생각하지만 일정 수준의 수익도 기대하는 유형입니다.", ["채권형 펀드", "배당주", "우량주", "분산투자"]
    elif score <= 36:
        return "위험중립형", "안정성과 수익성을 균형 있게 고려하는 유형입니다.", ["ETF", "우량주", "인덱스 펀드", "장기투자"]
    elif score <= 44:
        return "적극투자형", "어느 정도 손실을 감수하면서 높은 수익을 추구하는 유형입니다.", ["성장주", "해외주식", "테마 ETF", "포트폴리오 투자"]
    else:
        return "공격투자형", "큰 변동성을 감수하더라도 높은 수익을 추구하는 유형입니다.", ["기술주", "성장주", "고위험 ETF", "글로벌 주식"]


# =========================
# 사이드바
# =========================
st.sidebar.title("💰 투자성향 퀴즈")
st.sidebar.write("Streamlit 미니 프로젝트")
st.sidebar.divider()

if st.sidebar.button("💵소개"):
    go_page("소개")

if st.sidebar.button("📝퀴즈"):
    go_page("퀴즈")

if st.sidebar.button("📊결과"):
    go_page("결과")

st.sidebar.divider()

if st.session_state.login:
    #st.sidebar.success(f"{st.session_state.username}님 로그인 중")
    if st.sidebar.button("🔓로그아웃"):
        logout()
        st.rerun()
else:
    st.sidebar.warning("로그인이 필요합니다.")


# =========================
# 오른쪽 위 로그인 버튼
# =========================
top_col1, top_col2 = st.columns([5, 1.5])

with top_col2:
    if st.session_state.login:
        st.success(f"{st.session_state.username}님 로그인 중")
    else:
        if st.button("Login"):
            go_page("로그인")
            st.rerun()

menu = st.session_state.menu


# =========================
# 소개 페이지
# =========================
if menu == "소개":
    st.title("💰 금융투자성향 퀴즈 앱")
    st.header("나에게 맞는 투자 스타일 알아보기")

    st.markdown("### 제출자 정보")
    st.write("학번: 2022204009")
    st.write("이름: 최주연")

    st.caption("이 앱은 투자 성향을 간단히 진단하고, 결과에 따라 적합한 투자 스타일을 안내합니다.")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["투자의 필요성", "투자 기본 개념", "앱 사용 방법"])

    with tab1:
        st.markdown("## 왜 투자가 필요할까❓")
        st.write(
            """
            투자는 단순히 돈을 많이 벌기 위한 활동이 아니라,
            미래의 경제적 안정성을 준비하기 위한 중요한 금융 활동입니다.
            """
        )

        st.markdown("### 📌 투자가 필요한 이유")

        st.markdown("""
    - **물가 상승 대비**
      → 시간이 지나면 돈의 가치가 떨어지기 때문에 투자로 자산을 지켜야 합니다.

    - **자산 증식**
      → 단순 저축보다 더 높은 수익을 기대할 수 있습니다.

    - **경제적 자유**
      → 꾸준한 투자를 통해 미래의 경제적 부담을 줄일 수 있습니다.

    - **노후 대비**
      → 연금 외에도 추가적인 자산 마련이 필요합니다.
    """)

        st.divider()
        st.markdown("### ⚠️ 투자 시 주의해야 할 점")
        st.warning("""
    - 모든 투자는 손실 가능성이 있습니다.
    - 수익률이 높을수록 위험도 커집니다.
    - 감정적인 투자(충동매수)는 피해야 합니다.
    - 검증되지 않은 정보는 반드시 확인해야 합니다.
    """)

        st.info("""
    ✔ 중요한 것은 "무조건 높은 수익"이 아니라  
    ✔ "나에게 맞는 투자"를 하는 것입니다.
    """)

        st.expander("쉽게 이해하는 투자 예시📖").write("""
    예를 들어, 은행에 돈을 맡기면 안전하지만 이자는 적습니다.
    반면 주식은 수익이 클 수 있지만 가격이 크게 변동합니다.

    따라서 자신의 성향에 맞는 투자 방식을 선택하는 것이 중요합니다.
    """)


    with tab2:
        st.markdown("## 투자 기본 개념")

        st.write("""
    투자는 다양한 방법이 있으며, 자신의 투자 성향에 맞게 선택하는 것이 중요합니다.
    아래는 대표적인 투자 유형들입니다.
    """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💵 예금 / 적금")
            st.write("원금이 보장되는 가장 안전한 투자 방식입니다. 수익은 낮지만 안정적입니다.")

            st.markdown("### 📈 주식")
            st.write("기업의 지분을 사는 투자입니다. 수익률이 높을 수 있지만 변동성이 큽니다.")

            st.markdown("### 📊 ETF")
            st.write("여러 종목을 한 번에 투자하는 상품으로 분산투자가 가능합니다.")


        with col2:
            st.markdown("### 🏦 채권")
            st.write("국가나 기업에 돈을 빌려주고 이자를 받는 방식으로 비교적 안정적입니다.")

            st.markdown("### 🌍 해외주식")
            st.write("글로벌 기업에 투자할 수 있으며 환율 영향도 받습니다.")

            st.markdown("### 🚀 성장주")
            st.write("앞으로 크게 성장할 가능성이 있는 기업에 투자하는 방식입니다.")

        st.divider()

        st.expander("투자 초보자를 위한 팁💡").write("""
    - 처음에는 예금, ETF처럼 안정적인 상품부터 시작하는 것이 좋습니다.
    - 한 종목에 몰아서 투자하지 말고 분산투자를 하세요.
    - 단기 수익보다는 장기적인 관점에서 투자하는 것이 중요합니다.
    """)
        
    with tab3:
        st.markdown("## 📱앱 사용 방법")
        st.text("1. 오른쪽 위 Login 버튼을 눌러 로그인합니다.")
        st.text("2. 사이드바에서 퀴즈 페이지로 이동합니다.")
        st.text("3. 모든 문항에 답하고 결과 제출 버튼을 누릅니다.")
        st.text("4. 결과보기 버튼 또는 사이드바 결과 메뉴에서 결과를 확인합니다.")

        st.success("로그인, 캐싱, 퀴즈, 세션 상태 관리 기능이 모두 포함됩니다.")


# =========================
# 로그인 페이지
# =========================
elif menu == "로그인":
    st.title("🔐 로그인")

    st.markdown("### 미리 정의된 계정")
    st.code("ID: user\nPW: 1234")

    user_id = st.text_input("아이디", key="login_id")
    user_pw = st.text_input("비밀번호", type="password", key="login_pw")

    if st.button("로그인"):
        if user_id == "user" and user_pw == "1234":
            st.session_state.login = True
            st.session_state.username = user_id
            st.session_state.menu = "소개"
            st.success("로그인 성공! 소개 페이지로 이동합니다.")
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    st.info("로그인 상태는 st.session_state를 통해 관리됩니다.")


# =========================
# 퀴즈 페이지
# =========================
elif menu == "퀴즈":
    st.title("📝 금융투자성향 퀴즈")

    if not st.session_state.login:
        st.warning("퀴즈를 풀기 전에 먼저 로그인해주세요.")
    else:
        uploaded_file = st.file_uploader("퀴즈 CSV 파일 업로드", type=["csv"])

        if uploaded_file is not None:
            quiz_data = pd.read_csv(uploaded_file)
            st.success("업로드한 CSV 파일을 사용합니다.")
        else:
            quiz_data = load_quiz_data("data/investment_quiz.csv")
            st.info("기본 퀴즈 데이터를 사용합니다.")

        st.caption("CSV 데이터는 st.cache_data를 이용해 캐싱됩니다.")

        progress_bar = st.progress(0)

        with st.status("퀴즈 준비 중...", expanded=True) as status:
            time.sleep(0.4)
            st.write("문항 데이터를 확인했습니다.")
            progress_bar.progress(35)

            time.sleep(0.4)
            st.write("선택지를 생성했습니다.")
            progress_bar.progress(70)

            time.sleep(0.4)
            st.write("퀴즈 준비가 완료되었습니다.")
            progress_bar.progress(100)

            status.update(label="퀴즈 준비완료", state="complete", expanded=False)

        st.divider()

        with st.form("quiz_form"):
            total_score = 0

            for idx, row in quiz_data.iterrows():
                st.markdown(f"### Q{idx + 1}. {row['question']}")

                options = {
                    row["option_a"]: row["score_a"],
                    row["option_b"]: row["score_b"],
                    row["option_c"]: row["score_c"],
                    row["option_d"]: row["score_d"],
                }

                selected = st.radio(
                    "답변을 선택하세요.",
                    list(options.keys()),
                    key=f"question_{idx}"
                )

                st.session_state.answers[f"Q{idx + 1}"] = selected
                total_score += int(options[selected])

            submitted = st.form_submit_button("결과 제출")

            if submitted:
                st.session_state.score = total_score
                st.session_state.submitted = True
                st.success("퀴즈 제출이 완료되었습니다!")
                st.balloons()

        if st.session_state.submitted:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("퀴즈 다시 풀기"):
                    reset_quiz()
                    st.rerun()

            with col2:
                if st.button("결과보기"):
                    st.session_state.menu = "결과"
                    st.rerun()


# =========================
# 결과 페이지
# =========================
elif menu == "결과":
    st.title("📊 투자성향 결과")

    if not st.session_state.login:
        st.warning("로그인 후 결과를 확인할 수 있습니다.")
    elif not st.session_state.submitted:
        st.info("아직 퀴즈를 제출하지 않았습니다.")
    else:
        score = st.session_state.score
        result_type, description, recommendations = calculate_result(score)

        st.metric(label="총점", value=f"{score}점")

        st.header(f"당신의 투자 성향은: {result_type}")

        if result_type in ["안정형", "안정추구형"]:
            st.info(description)
        elif result_type == "위험중립형":
            st.success(description)
        elif result_type == "적극투자형":
            st.warning(description)
        else:
            st.error(description)

        st.subheader("추천 투자 스타일")
        for item in recommendations:
            st.write(f"- {item}")

        with st.expander("내가 선택한 답변 보기"):
            st.write(st.session_state.answers)

        st.markdown("### 결과 해석")
        st.write(
            """
            이 결과는 사용자의 답변을 점수화하여 계산한 것입니다.
            점수가 높을수록 위험을 감수하고 높은 수익을 추구하는 성향이 강하다고 볼 수 있습니다.
            """
        )

        st.caption("본 결과는 학습용 프로젝트의 참고 자료이며 실제 투자 조언이 아닙니다.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("퀴즈 세션 초기화"):
                reset_quiz()
                st.success("퀴즈 관련 세션이 초기화되었습니다.")
                st.rerun()

        with col2:
            if st.button("전체 캐시 삭제"):
                st.cache_data.clear()
                st.success("전체 캐시가 삭제되었습니다.")