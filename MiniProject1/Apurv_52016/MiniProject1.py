passi = input("Enter a password :: ")

result = []

# Store password characters in list
for i in passi:
    if i.isdigit():
        result.append(int(i))
    else:
        result.append(i)

#print("\nPassword List:", result)

score = 0

# Boolean checks
has_upper = False
has_lower = False
has_digit = False
has_special = False

special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '~']

# Length Check
if len(result) >= 8:
    score += 1
else:
    print("TIP: Password should contain at least 8 characters")

# Character Analysis
for i in result:

    if isinstance(i, str) and i.isupper():
        has_upper = True

    elif isinstance(i, str) and i.islower():
        has_lower = True

    elif isinstance(i, int):
        has_digit = True

    elif i in special_chars:
        has_special = True

# Uppercase Check
if has_upper==True:
    score += 1
else:
    print("TIP: Add at least one CAPITAL letter")

# Lowercase Check
if has_lower:
    score += 1
else:
    print("TIP: Add at least one small letter")

# Digit Check
if has_digit:
    score += 1
else:
    print("TIP: Add at least one number")

# Special Character Check
if has_special:
    score += 1
else:
    print("TIP: Add at least one special character")

# Final Score
print("\nPassword Score:", score, "/ 5")

# Strength Rating
if score == 5:
    print("★★★★★ Strong Password")

elif score == 4:
    print("★★★★ Good Password")

elif score == 3:
    print("★★★ Average Password")

elif score == 2:
    print("★★ Weak Password")

else:
    print("★ Very Weak Password")