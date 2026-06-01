import random
from flashcards import flashcards

mastered = {}
weak_cards = flashcards.copy()
rounds = 3

for round_no in range(1,rounds+1):
    if not weak_cards:
        break

    print(f"\n=======================Round {round_no}=======================")
    new_weak = {}
    questions = list(weak_cards.items())
    random.shuffle(questions)

    for question,answer in questions:
        user_answer = input(question + ":")
        if user_answer.strip().lower() == answer.strip().lower():
            mastered[question] = answer
            print("Correct!!")
        else:
            new_weak[question] = answer
            print("Wrong!!")
    weak_cards = new_weak

    print("\n-------Progress---------")
    print("\nRight answers: ",len(mastered))
    print("Weak answers: ",len(weak_cards))     

    print("\n====================FINAL RESULT=======================")

    print("\nTotal cards: ",len(flashcards))
    print("Mastered: ",len(mastered))
    print("Weak: ",len(weak_cards))

    if weak_cards:
        print("\nTry again!!") 
        for question,answer in weak_cards.items():
            print(f"\nQuestion: {question}\nAnswer: {answer}")
    else:
        print("\nCongratulations!! You've mastered all the flashcards!!")