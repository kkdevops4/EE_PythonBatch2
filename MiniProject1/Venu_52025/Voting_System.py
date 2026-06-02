# Voting System

# Register voters
voters = set()

# Candidates and votes
votes = {"Aman": 0, "Riya": 0, "Rahul": 0}

n = int(input("Enter number of voters: "))

# Cast votes
for i in range(n):

    voter_id = input("Enter voter ID: ")

    # Duplicate prevention using set
    if voter_id in voters:
        print("Duplicate vote not allowed")
        continue

    voters.add(voter_id)

    vote = input("Vote for Aman, Riya, Rahul: ")

    if vote in votes:
        votes[vote] += 1
        print("Vote casted")
    else:
        print("Invalid candidate. Please enter the correct choice!!!")

# Tally result
print("\nVote Count:")
for candidate in votes:
    print(candidate, "=", votes[candidate])

# Check winner or tie
max_votes = max(votes.values())

winners = []

for candidate in votes:
    if votes[candidate] == max_votes:
        winners.append(candidate)

if len(winners) == 1:
    print("\nWinner is:", winners[0])
else:
    print("\nIt's a tie between:" and ", ".join(winners))
