def mac_operation(input_matrix, filter_matrix):
    """
    외부 라이브러리 없이 구현하는 MAC 연산 (Multiply-Accumulate)
    점수 = Σ (입력[i][j] * 필터[i][j])
    """
    score = 0.0
    size = len(input_matrix)
    
    for i in range(size):
        for j in range(size):
            score += input_matrix[i][j] * filter_matrix[i][j]
            
    return score

# 테스트용 더미 데이터
test_input = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
test_filter = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

print(f"결과 점수: {mac_operation(test_input, test_filter)}")
