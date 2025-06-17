import json
import threading
import os
import datetime

time_limit = 15

def load_questions(filename):
    try:
        with open(filename, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print("⚠️ Could not find the questions file")
        return []

def answer(prompt, timeout):
    answer = [None]

    def ask_input():
        answer[0] = input(prompt)

    thread = threading.Thread(target=ask_input)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("\n⏰ Time’s up!")
        return None
    return answer[0]

def run_quiz(questions):
    score = 0
    for index, q in enumerate(questions):
        print(f"\nQ{index + 1}: {q['question']}")
        for i, option in enumerate(q['options'], start=1):
            print(f"{i}. {option}")
        
        user_input = answer("Your answer (1-4): ", time_limit)

        if user_input is None:
            print("❌ No answer given.")
            continue

        try:
            user_choice = int(user_input)

            if user_choice == q['answer']:
                print("✅ Correct!")
                score += 1
            else:
                correct_option = q['options'][q['answer'] - 1]
                print(f"❌ Wrong. Correct answer: {correct_option}")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number")

    return score, len(questions)

def result(score, total):
    print("\n🎯 Quiz finished!")
    print(f"Your score: {score} / {total}")
    percentage = (score / total) * 100

    if percentage == 100:
        print("You're perfect, All questions are correct 🎉")
    elif percentage >= 70:
        print("Great Job! You are doing well🔥")
    elif percentage >= 50:
        print("Keep improving, Not so bad😊")
    else:
        print("👍Keep Practicing, Practice makes a man perfect")

def save_result(name, age, score, total):
    log = {
        "name": name,
        "age": age,
        "score": f"{score}/{total}",
        "percentage": round((score / total) * 100, 2),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("quiz_results.txt", "a") as f:
        f.write(json.dumps(log) + "\n")
    print("📁 Your result has been saved successfully!")

# ===== Main Program Starts Here =====
if __name__ == "__main__":
    print("Looking in: ", os.getcwd())
    print("🧠 Welcome to the Quiz Game!\n")

    # Collect user details
    name = input("Enter your name: ")
    age = input("Enter your age: ")

    # Load questions and run quiz
    questions = load_questions("questions.json")
    if questions:
        score, total = run_quiz(questions)
        result(score, total)
        save_result(name, age, score, total)
