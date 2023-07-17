print("Welcome to Qunta Game")
playing =input("Do you want to play? ")
if playing.lower() !="yes":
    quit()
print("OKAY Lets Begin Nyggaaa : )")
score =0
answer =input("What does aws standfor? ")
if answer.lower()=="amazon web service":
    print("correct")
    score += 1
else:
    print("incorrect try again!")
print("you got" + str(score) +  " questions correct !" )


