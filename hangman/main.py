#### picking random word ####
import random
words = ["homework", "cleaning", "math", "history", "science", "English", "programming"]
index = random.randrange(0, len(words))
word = words[index]

#### stages of hanging ####
stages = [
'''
#---------
#            
#        
#        
#          
#        
#      #####
#        #
''',
'''
#---------
#        |    
#        
#        
#          
#        
#      #####
#        #
''',
'''
#---------
#        |    
#        O
#        
#          
#        
#      #####
#        # 
''',
'''
#---------
#        |    
#        O
#        |
#          
#        
#      #####
#        #
''',
'''
#---------
#        |    
#        O
#      \/|\/
#          
#        
#      #####
#        #
''',
'''
#---------
#        |    
#        O
#      \/|\/
#        A  
#        
#      #####
#        #
''',
'''
#---------
#        |    
#        O
#      \/|\/
#        A  
#      _/ \_
#      #####
#        #
''',
'''

!!! You have been hung !!!

#---------
#        |    
#        O
#      \/|\/
#        A  
#      _/ \_
#      
#
        _I_
         I
     ~~~~~~~~~
    /  !RIP!  \\
   /           \\
''']


#### Into ####
print('Welcome user to hangman!')
print('I will have a word in my head which all workaholics like and you have to guess it.')
print('...hmmmm I have thought of a word')


letters = []  # already used letters
lifes = len(stages) - 1   # remaining lifes
errors = 0  # errors made so far - to print a hanging stage


print('The word contains ' + str(len(word)) + ' letters')

while True:
    print()
    print(stages[errors])
    print('You have ' + str(lifes) + ' lifes')
    if len(letters) > 0:
        print('You used the following letters: ', ", ".join(letters))
    
    # print the word replacing unguessed letters with *
    print('The known word so far is ', end='')
    for letter in word:
        if letter.lower() in letters:
            print(letter, end="")
        else:
            print("*", end="")
     
    guess = input(". What is your next guess? (give me a letter): ")[0]
    if guess not in word:
        lifes -= 1
        errors +=1
        if lifes == 0:
            print(stages[errors])
            break
        
    letters += guess.lower()
    
    # check if the word is guessed completely
    guessed = True
    for letter in word:
        if letter.lower() not in letters:
            guessed = False
            
    if guessed:
        print('')
        print('LUCKY YOU !!!')
        print('The word is really "' + word + '"')
        print('Next time, for sure, you will be hung!')
        break
