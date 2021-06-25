import random

password = ""
ui = "abcdefghijklmnopqrstuvwxyz"
a = ui + ui.upper() + "0123456789"

for i in range(12):
    re = random.choice(a)
    password += re
    if i == 2 or i == 5 or i == 8:
        password += "-"

print(password)

input()
