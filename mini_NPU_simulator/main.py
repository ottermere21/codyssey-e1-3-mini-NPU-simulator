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
            print("처음부터 다시 입력해주세요.\n")

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
    try:
        with open(data_file_path, "r", encoding="UTF-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 에러: {data_file_path} 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print(f"⚠️ 에러: {data_file_path} 파일의 JSON 형식이 올바르지 않습니다.")
        return

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    # 필터 미리 로드
    load_filters = {}
    print("\n# 필터 로드 중...")
    for size_N, filter_pair in filters.items():
        try:
            cross_matrix = Matrix(filter_pair["cross"])
            x_matrix = Matrix(filter_pair["x"])
            load_filters[size_N] = {
                "Cross": cross_matrix,
                "X": x_matrix
            }
            print(f"{size_N} 필터 로드 완료 (Cross, X)")
        except Exception as e:
            print(f"⚠️ {size_N} 필터 로드 실패: {e}")

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    failed_cases = []

    print("\n# 패턴 분석 중...(라벨 정규화 적용)")
    for pattern_N, pattern_info in patterns.items():
        total_tests += 1
        expected_raw = pattern_info.get("expected", "")
        
        # expected 값 정규화 적용
        try:
            expected_normalized = normalize_label(expected_raw)
        except Exception as e:
            expected_normalized = "INVALID"

        try:
            pattern_matrix = Matrix(pattern_info.get("input", []))
            
            # 패턴 키에서 크기 문자열 추출 (예: "size_5_1" -> "size_5")
            parts = pattern_N.split("_")
            size_N = f"size_{parts[1]}"
            
            if size_N not in load_filters:
                raise KeyError(f"해당 크기({size_N})의 필터가 로드되지 않았습니다.")
                
            filter_cross = load_filters[size_N]["Cross"]
            filter_x = load_filters[size_N]["X"]
            
            # 크기 검증
            if pattern_matrix.size != filter_cross.size:
                raise ValueError(f"필터 크기({filter_cross.size})와 패턴 크기({pattern_matrix.size})가 다릅니다.")
            
            # MAC 연산 수행
            score_cross = mac_operation(pattern_matrix, filter_cross)
            score_x = mac_operation(pattern_matrix, filter_x)
            
            # 판정 도출
            decision = compare_scores(score_cross, score_x)
            
            # 결과 검증
            if decision == expected_normalized:
                status = "PASS"
                passed_tests += 1
            else:
                status = "FAIL"
                failed_tests += 1
                failed_cases.append((pattern_N, f"판정 불일치 (결과: {decision} vs 정답: {expected_normalized})"))
                
            print(f"-- {pattern_N} --")
            print(f"Cross 점수 : {score_cross:.16f}")
            print(f"X 점수 : {score_x:.16f}")
            print(f"판정: {decision} | expected: {expected_normalized} | {status}")
            
        except Exception as e:
            failed_tests += 1
            failed_cases.append((pattern_N, f"에러 (사유: {e})"))
            print(f"-- {pattern_N} --")
            print(f"판정: ERROR | expected: {expected_normalized} | FAIL (사유: {e})")

    # 성능 분석 테이블 출력
    measure_performance()

    # 결과 요약
    print("\n# 결과 요약")
    print(f"총 테스트: {total_tests}개")
    print(f"통과: {passed_tests}개")
    print(f"실패: {failed_tests}개")
    if failed_cases:
        print("\n실패 케이스 목록:")
        for name, reason in failed_cases:
            print(f"- {name}: {reason}")


def measure_performance():
    """
    성능 분석 및 결과 테이블 출력
    - 각 크기(3x3, 5x5, 13x13, 25x25)에 대해 MAC 연산을 10회 반복 측정하여
      평균 연산 시간(ms)과 연산 횟수(N^2)를 계산하여 테이블 형태로 출력합니다.
    """
    sizes = [3, 5, 13, 25]
    print("\n# 성능 분석 (평균/10회)")
    print(f"{'크기':<10} | {'평균 시간 (ms)':<18} | {'연산 횟수 (N^2)'}")
    print("-" * 50)
    
    for n in sizes:
        # 더미 데이터 생성 (N x N)
        dummy_pattern = Matrix([[1.0] * n for _ in range(n)])
        dummy_filter = Matrix([[1.0] * n for _ in range(n)])
        
        # 10회 측정
        start_time = time.perf_counter()
        for _ in range(10):
            mac_operation(dummy_pattern, dummy_filter)
        end_time = time.perf_counter()
        
        avg_time_ms = ((end_time - start_time) / 10) * 1000
        op_count = n * n
        print(f"{f'{n}x{n}':<10} | {avg_time_ms:<18.6f} | {op_count}")


def main():
    """
    전체 프로그램 실행 제어
    1. 사용자가 모드 1(사용자 입력 3x3) 또는 모드 2(data.json 분석) 중 선택하도록 유도합니다.
    2. 선택에 따라 run_mode1() 또는 run_mode2()를 작동시킵니다.
    """
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            run_mode1()
            break
        elif choice == "2":
            run_mode2("data.json")
            break
        else:
            print("⚠️ 올바른 번호(1 또는 2)를 선택해주세요.")


if __name__ == "__main__":
    main()
