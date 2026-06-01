questions = [
    {
        "question": "Which keyword is used to create a function in Python?",
        "options": ("A. func", "B. def", "C. function", "D. define"),
        "answer": "B",
        "topic": "Functions"
    },
    {
        "question": "Which data type stores multiple values in square brackets []?",
        "options": ("A. Tuple", "B. Set", "C. List", "D. Dictionary"),
        "answer": "C",
        "topic": "Lists"
    },
    {
        "question": "Which loop is used to iterate over a sequence?",
        "options": ("A. if", "B. while", "C. switch", "D. for"),
        "answer": "D",
        "topic": "Loops"
    },
    {
        "question": "What is the output of 10 // 3?",
        "options": ("A. 3", "B. 3.33", "C. 4", "D. 1"),
        "answer": "A",
        "topic": "Operators"
    },
    {
        "question": "Which data structure stores key-value pairs?",
        "options": ("A. List", "B. Tuple", "C. Dictionary", "D. Set"),
        "answer": "C",
        "topic": "Dictionary"
    }
]

def ask_question(question):
    print("\n" + question["question"])

    for option in question["options"]:
        print(option)

    answer = input("Enter your answer (A/B/C/D): ").upper()
    return answer

def show_scorecard(results, score, topics):
    print("\n===== SCORECARD =====")

    for i in range(len(results)):
        print("Question", i + 1, ":", results[i])

    print("\nTopics Covered:")
    for topic in topics:
        print(topic)

    print("\nFinal Score =", score)

score = 0
streak = 0

results = []

topics_attempted = set()

print("===== PYTHON QUIZ APP =====")

for question in questions:

    user_answer = ask_question(question)

    topics_attempted.add(question["topic"])

    if user_answer == question["answer"]:
        print("Correct!")

        score += 10
        streak += 1

        if streak >= 3:
            print("Streak Bonus +5")
            score += 5

        results.append("Correct")

    else:
        print("Wrong!")
        streak = 0
        results.append("Wrong")

show_scorecard(results, score, topics_attempted)
