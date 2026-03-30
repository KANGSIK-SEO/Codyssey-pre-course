import json
import os
import sys

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index):
        print(f"\n[문제 {index}]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        return str(user_answer).strip() == str(self.answer)

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

class QuizGame:
    def __init__(self, file_path="state.json"):
        self.file_path = file_path
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.init_default_quizzes()
            self.save_data()
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        except (json.JSONDecodeError, KeyError):
            print("⚠️ 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            self.init_default_quizzes()
            self.save_data()

    def init_default_quizzes(self):
        self.quizzes = [
            Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "James Gosling", "Bjarne Stroustrup"], 1),
            Quiz("Python의 주요 특징이 아닌 것은?", ["인터프리터 언어", "강력한 커뮤니티", "엄격한 세미콜론 사용", "객체 지향"], 3),
            Quiz("목록(list)에 요소를 추가하는 메서드는?", ["add()", "push()", "append()", "insert_end()"], 3),
            Quiz("조건문 키워드가 아닌 것은?", ["if", "elif", "else", "then"], 4),
            Quiz("Python 파일의 확장자는?", [".py", ".pyt", ".python", ".txt"], 1)
        ]

    def save_data(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"⚠️ 파일 저장 오류: {e}")

    def display_menu(self):
        print("\n" + "="*40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("="*40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("="*40)

    def get_input(self, prompt, is_digit=False, min_val=None, max_val=None):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️ 입력을 다시 확인해주세요 (빈 입력 불가).")
                    continue
                
                if is_digit:
                    if not user_input.isdigit():
                        print("⚠️ 숫자만 입력 가능합니다.")
                        continue
                    val = int(user_input)
                    if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                        print(f"⚠️ {min_val}~{max_val} 범위의 숫자를 입력하세요.")
                        continue
                    return val
                return user_input
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 프로그램을 종료합니다.")
                self.save_data()
                sys.exit(0)


    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0
        for i, quiz in enumerate(self.quizzes, 1):
            print("-" * 40)
            quiz.display(i)
            user_ans = self.get_input("정답 입력 (1-4): ", is_digit=True, min_val=1, max_val=4)
            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer})")

        print("\n" + "="*40)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({score*20 if len(self.quizzes)==5 else score}점)")
        if score*20 > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score*20
            self.save_data()
        print("="*40)

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.get_input("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(self.get_input(f"선택지 {i}: "))
        answer = self.get_input("정답 번호 (1-4): ", is_digit=True, min_val=1, max_val=4)
        
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self):
        print(f"\n🏆 현재 최고 점수: {self.best_score}점")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_input("선택: ", is_digit=True, min_val=1, max_val=5)
            if choice == 1: self.play_quiz()
            elif choice == 2: self.add_quiz()
            elif choice == 3: self.list_quizzes()
            elif choice == 4: self.show_best_score()
            elif choice == 5:
                print("👋 프로그램을 종료합니다.")
                break

if __name__ == "__main__":
    game = QuizGame("mission2/state.json")
    game.run()
# Extra comment
