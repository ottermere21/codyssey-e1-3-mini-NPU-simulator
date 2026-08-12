class Matrix:
    def __init__(self, matrix):
        # 1. 2차원 배열인지 검증
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("⚠️ 입력 데이터는 2차원 리스트 형태여야 합니다.\n")

        # 2. 행,열 크기가 일치하는지 (N*N) 검증
        n = len(matrix)
        if not all(len(row) == n for row in matrix):
            raise ValueError("⚠️ 입력 데이터는 N × N 정방행렬이어야 합니다.\n")

        self.matrix = matrix 
        self.size = n

    # 특정 위치(r행,c열) 값을 가져오는 함수
    def get(self, r: int, c: int) -> float:
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            raise IndexError("⚠️ 인덱스 범위를 벗어났습니다.")
        return self.matrix[r][c]

    # 특정 위치(r행,c열)의 값을 설정하는 함수
    def set(self, r: int, c: int, value: float):
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            raise IndexError("⚠️ 인덱스 범위를 벗어났습니다.")
        self.matrix[r][c] = value

# 입력받은 라벨(+,cross,x 등)을 표준 라벨(Cross, X)로 정규화하는 함수
def normalize_label(label: str) -> str:
    cleaned = str(label).strip().lower()

    if cleaned in ['+','cross']:
        return 'Cross'
    elif cleaned in ['x']:
        return 'X'
    else:
        raise ValueError(f"⚠️ 올바르지 않은 라벨 이름입니다: {label}")
