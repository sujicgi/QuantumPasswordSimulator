# 암호 길이(bits)를 받아
# 고전 컴퓨터의 탐색 횟수를 계산

def classical_search(password):

    # 입력된 암호 길이
    bits = len(password)

    # 가능한 경우의 수
    total_cases = 2 ** bits

    # 평균 탐색 횟수
    average_attempts = total_cases / 2

    return bits, total_cases, average_attempts