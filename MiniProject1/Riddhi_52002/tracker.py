print("Welcome to Cricket Score Tracker")
teamA = input("Enter Team 1 name:")
teamB = input("Enter Team2 name:")
total_overs = int(input("Enter number of overs per innings:"))

#Team A
print(f"\n{teamA}'s Innings")
teamA_runs = 0
teamA_wickets = 0

for current_over in range(1,total_overs+1):
    print(f"Over {current_over}")

    runs = int(input("Enter runs scored in this over:"))
    wickets = int(input("Enter wickets lost in this over:"))

    #Updates of Team A
    teamA_runs = teamA_runs + runs
    teamA_wickets = teamA_wickets + wickets

    #Runrate
    runrate = teamA_runs / current_over
    print(f"Current Score:{teamA_runs}/{teamA_wickets}")
    print(f"Current Run Rate:{runrate:.2f}")

    if (teamA_wickets >= 10):
        print(f"All OUT!!\n{teamA} lost all the wickets.:( )")
        break

#Team B
print(f"\n{teamB}'s Innings")
teamB_runs = 0
teamB_wickets = 0

for current_over in range(1,total_overs+1):
    print(f"Over {current_over}")

    runs = int(input("Enter the runs scored in this over:"))
    wickets = int(input("Enter wickets lost in this over:"))

    #Updates of Team B
    teamB_runs = teamB_runs + runs
    teamB_wickets = teamB_wickets + wickets

    #Runrate
    runrate = teamB_runs / current_over
    print(f"Current Score:{teamB_runs}/{teamB_wickets}")
    print(f"Current Run Rate:{runrate:.2f}")

    if(teamB_wickets >= 10):
        print(f"All OUT!!\n{teamB} lost all the wickets.:( \n)")
        break

#Results
print("Match Summary")
print(f"{teamA}:{teamA_runs}/{teamA_wickets}")
print(f"{teamB}:{teamB_runs}/{teamB_wickets}")

if teamA_runs > teamB_runs:
    diff = teamA_runs - teamB_runs
    print(f"{teamA} won the match by {diff} runs!\nCongratulations {teamA}!")

elif teamB_runs > teamA_runs:
    wickets_left = 10 - teamB_wickets
    print(f"{teamB} won the match by {wickets_left} wickets!\nCongratulations {teamB}!")

else:
    print("SUPER OVER!")