def ask_question(question, options, correct_answer):
    print("\n" + question)

    for option in options:
        print(option)

    answer = input("Enter your answer (A/B/C/D): ").upper()

    if answer == correct_answer:
        return True
    else:
        return False


def show_scorecard(score, correct, total):
    print("\n===== SCORECARD =====")
    print("Total Questions :", total)
    print("Correct Answers :", correct)
    print("Wrong Answers :", total - correct)
    print("Final Score :", score)

    percentage = (correct / total) * 100
    print("Percentage :", percentage, "%")


questions = [
    ["Which datatype stores decimal numbers?",
     ["A. int", "B. float", "C. str", "D. bool"],
     "B"],

    ["Which operator is used for exponentiation?",
     ["A. *", "B. //", "C. **", "D. %"],
     "C"],

    ["Which keyword is used for decision making?",
     ["A. for", "B. if", "C. while", "D. break"],
     "B"],

    ["Which loop is used to iterate over a sequence?",
     ["A. if", "B. else", "C. for", "D. pass"],
     "C"],

    ["Which method converts a string to uppercase?",
     ["A. upper()", "B. lower()", "C. split()", "D. replace()"],
     "A"],

    ["Which data structure is mutable?",
     ["A. Tuple", "B. List", "C. String", "D. Integer"],
     "B"],

    ["Which data structure stores key-value pairs?",
     ["A. Set", "B. List", "C. Dictionary", "D. Tuple"],
     "C"],

    ["Which keyword is used to create a function?",
     ["A. function", "B. define", "C. fun", "D. def"],
     "D"]
]

score = 0
streak = 0
correct_answers = 0

print("===== PYTHON QUIZ APP =====")

for question in questions:
    result = ask_question(question[0], question[1], question[2])

    if result:
        print("Correct Answer!")
        score += 10
        correct_answers += 1
        streak += 1

        if streak == 3:
            print("Bonus! +5 points for 3 correct answers in a row")
            score += 5
            streak = 0
    else:
        print("Wrong Answer!")
        streak = 0

show_scorecard(score, correct_answers, len(questions))
