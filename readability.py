from cs50 import get_string
import re

wordcount = 0
charcount = 0
sentencecount = 0
readabilitygrade = 0

text = get_string("Enter your text: ")

# Splits input text into sentences, words and characters based on special characters and for loop iterations

for sentence in re.split(r"[.?!]", text):
    sentencecount += 1
for word in text.split(" "):
    wordcount += 1
    for char in word:
        charcount += 1

# print(sentencecount)
# print(wordcount)
# print(charcount)

# Grading Algorithm
completters = (charcount / wordcount) * 100
compsentences = (sentencecount / wordcount) * 100
compgrades = float((0.0588 * completters - 0.296 * compsentences - 15.8))
compgrades = round(compgrades)
readabilitygrade = compgrades

# print(readabilitygrade)

# Computes grades based on readability grade
if readabilitygrade < 1:
    print("Before Grade 1")

elif readabilitygrade < 16:
    print("Grade", readabilitygrade)

if readabilitygrade > 16:
    print("Grade 16+")





