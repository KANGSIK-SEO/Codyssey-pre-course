import json

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        try:
            with open('state.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_score = data.get('best_score', 0)
        except FileNotFoundError:
            print("데이터 파일이 없어 새로 생성합니다.")

    def run(self):
        print("=== 나만의 퀴즈 게임 ===")
        # 여기에 메뉴 로직 추가 예정
        pass

if __name__ == "__main__":
    game = QuizGame()
    game.run()
