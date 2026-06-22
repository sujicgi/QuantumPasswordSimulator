import streamlit as st
import math
import pandas as pd

from classical import classical_search
from grover_demo import run_grover_demo

# 제목

st.title("양자 vs 고전 컴퓨터")
st.subheader("암호 해독 성능 비교 시뮬레이터")

# 탭 생성

tab1, tab2 = st.tabs(
    ["성능 비교", "Grover 실험"]
)
# 탭1 : 성능 비교
with tab1:

    password = st.text_input(
        "2진수 암호 입력",
        value="10110110"
    )

    if st.button("시뮬레이션 시작"):

        if not all(c in "01" for c in password):

            st.error(
                "0과 1만 입력해주세요."
            )

        else:

            bits, total_cases, classical_attempts = (
                classical_search(password)
            )

            quantum_attempts = math.sqrt(
                total_cases
            )

            speedup = (
                classical_attempts
                /
                quantum_attempts
            )

            st.success("계산 완료")

            st.write(
                f"입력한 암호 : {password}"
            )

            st.write(
                f"암호 길이 : {bits} 비트"
            )

            st.write(
                f"가능한 경우의 수 : {total_cases:,}"
            )

            st.write(
                f"고전 컴퓨터 평균 탐색 횟수 : {int(classical_attempts):,}"
            )

            st.write(
                f"양자 컴퓨터 평균 탐색 횟수 : {int(quantum_attempts):,}"
            )

            st.write(
                f"성능 향상 : 약 {speedup:.1f}배"
            )

            # 초당 1000회 시도 가능하다고 가정
            attempt_per_sec = 1000

            classical_time = classical_attempts / attempt_per_sec
            quantum_time = quantum_attempts / attempt_per_sec

            st.write(
                f"고전 컴퓨터 예상 시간 : {classical_time:.3f}초"
            )

            st.write(
                f"양자 컴퓨터 예상 시간 : {quantum_time:.3f}초"
            )

            def format_time(seconds):

             if seconds < 60:
                return f"{seconds:.2f}초"

             elif seconds < 3600:
                return f"{seconds/60:.2f}분"

             elif seconds < 86400:
                return f"{seconds/3600:.2f}시간"

             else:
                return f"{seconds/86400:.2f}일"
        
            st.write(
                f"고전 컴퓨터 예상 시간 : {format_time(classical_time)}"
            )

            st.write(
                f"양자 컴퓨터 예상 시간 : {format_time(quantum_time)}"
            )

            chart_data = {
                "고전": [classical_attempts],
                "양자": [quantum_attempts]
            }

            st.bar_chart(chart_data)
            
            st.subheader(
                "암호 길이에 따른 탐색 횟수 변화"
            )

            bit_range = list(range(2, 25))

            classical_values = []
            quantum_values = []

            for n in bit_range:

                classical_values.append(
                    (2 ** n) / 2
                )

                quantum_values.append(
                    math.sqrt(2 ** n)
                )

            graph_df = pd.DataFrame(
                {
                    "고전 컴퓨터": classical_values,
                    "양자 컴퓨터": quantum_values
                },
                index=bit_range
            )

            st.line_chart(graph_df)
            st.latex(r"O(2^n)")
            st.latex(r"O(\sqrt{N})")

# 탭2 : Grover 실험

with tab2:

    st.subheader(
        "실제 Grover 알고리즘 실험"
    )

    target = st.selectbox(
        "찾을 암호 선택",
        ["00", "01", "10", "11"]
    )

    if st.button("Grover 실행"):

        counts = run_grover_demo(target)

        st.image(
            "grover_circuit.png",
            caption="Grover 알고리즘 양자 회로"
        )

        full_counts = {
            "00": counts.get("00", 0),
            "01": counts.get("01", 0),
            "10": counts.get("10", 0),
            "11": counts.get("11", 0)
        }

        st.write(
            f"선택한 정답 : {target}"
        )

        st.write(full_counts)

        st.bar_chart(full_counts)