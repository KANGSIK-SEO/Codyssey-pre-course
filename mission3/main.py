import json
import time
import os

class NPUSimulator:
    def __init__(self, epsilon=1e-9):
        self.epsilon = epsilon
        self.standard_labels = {"+": "Cross", "cross": "Cross", "x": "X"}

    def normalize_label(self, label):
        """정규화된 라벨(Cross/X) 반환"""
        low_label = str(label).lower()
        return self.standard_labels.get(low_label, "UNDECIDED")

    def mac_operation(self, pattern, filter_data):
        """MAC (Multiply-Accumulate) 연산 수행"""
        if not pattern or not filter_data:
            return 0.0
        
        rows = len(pattern)
        cols = len(pattern[0])
        score = 0.0
        
        for r in range(rows):
            for c in range(cols):
                score += pattern[r][c] * filter_data[r][c]
        return float(score)

    def judge(self, score_cross, score_x):
        """점수 비교를 통한 판정 (epsilon 기반)"""
        if abs(score_cross - score_x) < self.epsilon:
            return "UNDECIDED"
        return "Cross" if score_cross > score_x else "X"

    def measure_performance(self, n, pattern, filter_data, iterations=10):
        """MAC 연산 성능 측정 (ms 단위)"""
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.mac_operation(pattern, filter_data)
        end_time = time.perf_counter()
        
        avg_time_ms = ((end_time - start_time) / iterations) * 1000
        return avg_time_ms

def run_mode_1():
    print("\n" + "#"*40)
    print("# [모드 1] 사용자 입력 (3x3)")
    print("#"*40)
    
    sim = NPUSimulator()
    
    def get_3x3_input(name):
        print(f"\n{name} (3줄 입력, 공백 구분):")
        matrix = []
        while len(matrix) < 3:
            try:
                line = input().strip()
                nums = [float(x) for x in line.split()]
                if len(nums) != 3:
                    print("⚠️ 입력 형식 오류: 각 줄에 3개의 숫자를 입력하세요.")
                    continue
                matrix.append(nums)
            except ValueError:
                print("⚠️ 입력 형식 오류: 숫자만 입력 가능합니다.")
        return matrix

    filter_a = get_3x3_input("필터 A")
    filter_b = get_3x3_input("필터 B")
    pattern = get_3x3_input("패턴")

    score_a = sim.mac_operation(pattern, filter_a)
    score_b = sim.mac_operation(pattern, filter_b)
    
    avg_time = sim.measure_performance(3, pattern, filter_a)
    
    print("\n" + "-"*40)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
    
    diff = abs(score_a - score_b)
    if diff < sim.epsilon:
        print(f"판정: 판정 불가 (|A-B| < {sim.epsilon})")
    else:
        print(f"판정: {'A' if score_a > score_b else 'B'}")

def run_mode_2(file_path):
    print("\n" + "#"*40)
    print("# [모드 2] data.json 분석")
    print("#"*40)
    
    if not os.path.exists(file_path):
        print(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sim = NPUSimulator()
    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    print("\n# [1] 필터 로드")
    for size_key in filters.keys():
        print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")

    print("\n# [2] 패턴 분석 (라벨 정규화 적용)")
    stats = {"total": 0, "pass": 0, "fail": 0, "failures": []}
    
    performance_data = []

    for p_key, p_val in patterns.items():
        # p_key format: size_N_idx
        parts = p_key.split("_")
        n = int(parts[1])
        size_key = f"size_{n}"
        
        current_pattern = p_val.get("input", [])
        expected_raw = p_val.get("expected", "")
        expected = sim.normalize_label(expected_raw)
        
        filter_group = filters.get(size_key, {})
        # Filter keys are normalized
        f_cross = filter_group.get("cross") or filter_group.get("+")
        f_x = filter_group.get("x") or filter_group.get("X")

        if not f_cross or not f_x or not current_pattern:
            print(f"- -- {p_key} --- [FAIL: 데이터 누락 또는 크기 불일치]")
            stats["total"] += 1
            stats["fail"] += 1
            stats["failures"].append(f"{p_key}: 데이터 누락")
            continue

        score_cross = sim.mac_operation(current_pattern, f_cross)
        score_x = sim.mac_operation(current_pattern, f_x)
        
        result = sim.judge(score_cross, score_x)
        is_pass = (result == expected)
        
        print(f"- -- {p_key} ---")
        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {result} | expected: {expected} | {'PASS' if is_pass else 'FAIL'}")
        
        stats["total"] += 1
        if is_pass: stats["pass"] += 1
        else:
            stats["fail"] += 1
            stats["failures"].append(f"{p_key}: 판정 불일치 (결과:{result}, 기대:{expected})")

        # Performance for this size (once per size group ideally, but here per pattern)
        avg_time = sim.measure_performance(n, current_pattern, f_cross)
        performance_data.append((n, avg_time))

    # Performance Table (Group by size)
    print("\n# [3] 성능 분석 (평균/10회)")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    print("-" * 40)
    
    # Sort and unique by size for display
    unique_sizes = sorted(list(set([d[0] for d in performance_data])))
    for sz in unique_sizes:
        times = [d[1] for d in performance_data if d[0] == sz]
        avg = sum(times) / len(times)
        print(f"{sz}x{sz:<8} {avg:<15.6f} {sz*sz}")

    print("\n# [4] 결과 요약")
    print(f"총 테스트: {stats['total']}개")
    print(f"통과: {stats['pass']}개")
    print(f"실패: {stats['fail']}개")
    
    if stats["failures"]:
        print("\n실패 케이스:")
        for f in stats["failures"]:
            print(f"- {f}")

def main():
    print("\n=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    while True:
        try:
            choice = input("선택: ").strip()
            if choice == "1":
                run_mode_1()
                break
            elif choice == "2":
                run_mode_2("mission3/data.json")
                break
            else:
                print("⚠️ 1 또는 2를 입력하세요.")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 종료합니다.")
            break

if __name__ == "__main__":
    main()
