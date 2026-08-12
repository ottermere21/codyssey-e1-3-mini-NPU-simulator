import time
import json
from mini_NPU_simulator.matrix import Matrix, normalize_label
from mini_NPU_simulator.simulator import mac_operation, compare_scores

def input_3x3_matrix(name: str) -> Matrix:
    print(f"\n{name} 입력: 각 줄에 3개의 숫자를 공백으로 구분하여 입력해주세요")
    while True:
        try:
            matrix_data = []
            for i in range(3):
                row = list(map(float, input(f"{i+1}행: ").split()))
                if len(row) != 3:
                    raise ValueError("⚠️ 행 개수가 맞지 않습니다. 3개의 행을 입력하세요\n")
                matrix_data.append(row)
            return Matrix(matrix_data)
        except ValueError:
            print("⚠️ 입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
            print("처음부터 다시 입력받습니다.\n")

def run_mode1():
    """
    [모드 1] 사용자 직접 입력 (3x3)
    1. 사용자로부터 3x3 크기의 필터 A, 필터 B, 패턴 데이터를 한 줄씩 입력받습니다.
       - 잘못된 입력 형식일 때 에러 안내를 출력하고 재입력을 받도록 루프를 작성해줍니다.
    2. 패턴과 각 필터 간의 MAC 연산을 수행합니다.
    3. 판정 및 연산 속도(ms)를 계산하여 콘솔에 출력합니다.
    """

    filter_a = input_3x3_matrix("Filter A")
    filter_b = input_3x3_matrix("Filter B")
    pattern = input_3x3_matrix("Pattern")

    # 10회 반복하여 평균 연산 시간 측정
    start_time = float(time.perf_counter())
    for _ in range(10):
        score_a = mac_operation(pattern, filter_a)
        score_b = mac_operation(pattern, filter_b)
    end_time = float(time.perf_counter())

    avg_time_ms = ((end_time - start_time) / 10) * 1000
    decision = compare_scores(score_a, score_b)

    print("\n[MAC 결과]")
    print(f"Filter A Score: {score_a:.4f}")
    print(f"Filter B Score: {score_b:.4f}")
    print(f"연산 시간(평균/10회): {avg_time_ms:.6f} ms")

    print("\n[판정 결과]")
    print(f"판정: {decision}")


def run_mode2(data_file_path: str):
    """
    [모드 2] data.json 파일 로드 및 배치 분석
    1. data_file_path 경로에 있는 JSON 파일을 읽어옵니다.
    2. JSON 내의 filters와 patterns 데이터를 가져와 크기가 일치하는지 검증합니다.
       - 크기가 맞지 않거나 에러 발생 시 프로그램이 멈추지 않고 해당 케이스만 'FAIL' 처리하게 하세요.
    3. 라벨을 정규화하여 expected와 결과를 비교하고 PASS / FAIL 여부를 판단합니다.
    4. 분석 결과를 화면에 출력하고 결과 리포트용 요약 통계를 준비합니다.
    """
    pass


def measure_performance():
    """
    성능 분석 및 결과 테이블 출력
    - 각 크기(3x3, 5x5, 13x13, 25x25)에 대해 MAC 연산을 10회 반복 측정하여
      평균 연산 시간(ms)과 연산 횟수(N^2)를 계산하여 테이블 형태로 출력합니다.
    """
    pass


def main():
    """
    전체 프로그램 실행 제어
    1. 사용자가 모드 1(사용자 입력 3x3) 또는 모드 2(data.json 분석) 중 선택하도록 유도합니다.
    2. 선택에 따라 run_mode1() 또는 run_mode2()를 작동시킵니다.
    """
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    # 여기에 모드 선택 입력을 처리하는 로직을 작성해보세요.
    pass


if __name__ == "__main__":
    main()
