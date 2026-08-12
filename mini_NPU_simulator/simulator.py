from mini_NPU_simulator.matrix import Matrix

# 두 행렬의 원소별 곱을 누적하는 연산(MAC) 함수. only 반복문
def mac_operation(pattern: Matrix, filter_matrix: Matrix) -> float:
    n = pattern.size
    if n != filter_matrix.size:
        raise ValueError("⚠️ 패턴과 필터의 크기가 일치하지 않습니다.\n")


    total = 0.0
    for r in range(0,n):
        for c in range(0,n):
            total += (pattern.get(r,c) * filter_matrix.get(r,c))

    return total
    


# 두 필터의 점수 비교하여 더 큰 필터의 이름 반환 함수. 허용 오차 처리해야 함
# abs(score_a - score_b) < 1e-9 이면 동점으로 간주
def compare_scores(score_a: float, score_b: float) -> str:
    '''
    score_a: Cross 필터의 점수
    score_b: X 필터의 점수
    '''

    diff = abs(score_a - score_b)
    if (diff < 1e-9):
        return 'UNDECIDED'
    elif (score_a > score_b):
        return 'Cross'
    else:
        return 'X'