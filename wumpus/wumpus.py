#!/usr/bin/env python3

import random

Instructions = '''
WELCOME TO 'HUNT THE WUMPUS'

  THE WUMPUS LIVES IN A CAVE OF 25 ROOMS. EACH ROOM
HAS 4 TUNNELS LEADING TO OTHER ROOMS.

     HAZARDS:
 BOTTOMLESS PITS - SOME ROOMS HAVE BOTTOMLESS PITS IN THEM
     IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
 SUPER EVIL CHIPMUNKS - SOME OTHER ROOMS HAVE SUPER EVIL 
     CHIPMUNKS. IF YOU GO THERE, A CHIPMUNK GRABS YOU AND
     TAKES YOU TO SOME OTHER ROOM AT RANDOM. (WHICH MAY BE
     TROUBLESOME)
     
     WUMPUS:
 THE WUMPUS IS NOT BOTHERED BY HAZARDS (HE HAS SUCKER
 FEET AND IS TOO BIG FOR A CHIPMUNK TO LIFT). USUALLY
 HE IS ASLEEP. THE ONLY THING WAKE HIM UP - YOU ENTERED
 HIS ROOM. HE EATS YOU UP AND YOU LOSE!

     YOU:
 EACH TURN YOU MAY MOVE OR SHOOT AN ARROW
   MOVING:  YOU CAN MOVE ONE ROOM (THRU ONE TUNNEL)
   ARROWS:  YOU HAVE 5 ARROWS. YOU LOSE WHEN YOU RUN OUT
     YOU AIM BY TELLING THE COMPUTER THE ROOM NUMBER YOU 
     WANT THE ARROW TO GO TO.
     IF THE ARROW CAN'T GO THAT WAY (IF NO TUNNEL) IT BOUNCED
     OF THE WALL AND HIT YOUR HEAD.
       IF THE ARROW HITS THE WUMPUS, YOU WIN.
       IF THE ARROW HITS YOU, YOU LOSE.

     WARNINGS:
 WHEN YOU ARE TWO ROOM AWAY FROM A WUMPUS OR ONE ROOM AWAY
 FROM A HAZARD, THE COMPUTER SAYS:
   WUMPUS   :  'I SMELL A WUMPUS'
   CHIPMUNK :  'CHIPMUNKS SCURRYING AROUND'
   PIT      :  'I FEEL A DRAFT'
'''

print_instructions = input('INSTRUCTIONS (Y-N)?')
if print_instructions == 'y' or print_instructions == 'Y':
    print(Instructions)

# cave. cave is a N x N rooms
N = 5
Pits = 2  # number of pits to allocate in the cave
Chipmunks = 3  # number of chipmunks to allocate in the cave

# Constants to describe what is in the room
Empty = 0
Chipmunk = 1
Pit = 2

# create an empty cave
cave = []
for y in range(N):
    cave.append([Empty] * N)

# place pits
for _ in range(Pits):
    x = random.randint(0, N - 1)
    y = random.randint(0, N - 1)
    cave[y][x] = Pit

# place chipmunks
for _ in range(Chipmunks):
    x = random.randint(0, N - 1)
    y = random.randint(0, N - 1)
    cave[y][x] = Chipmunk

# initial hunter's position
hunter_x = 0
hunter_y = 0

# initial number of arrows
left_arrows = 5

# select place for wumpus
wumpus_x = random.randint(0, N - 1)
wumpus_y = random.randint(0, N - 1)

# Make the entry point free of pits and chipmunks
cave[0][0] = Empty

gameover = False
while not gameover:
    if cave[hunter_y][hunter_x] == Chipmunk:
        cave[hunter_y][hunter_x] = Empty  # chipmunks left the original room
        hunter_y = random.randint(0, N - 1)
        hunter_x = random.randint(0, N - 1)
        print('CHIPMUNKS CARRIED AND DROPPED YOU SOMEWHERE')

    if hunter_x == wumpus_x and hunter_y == wumpus_y:
        print('YOU HAVE PERISHED.')
        print('WHAHAHAHA - YOU LOSE!')
        gameover = True
        continue

    if cave[hunter_y][hunter_x] == Pit:
        print('YYYYIIIIEEEE . . . FELL IN PIT')
        print('HA HA HA - YOU LOSE!')
        gameover = True
        continue

    if left_arrows == 0:
        print('YOU RAN OUT OF ARROWS.')
        print('SIT AND DIE HERE! (THE KING WILL KILL YOU ANYWAY)')
        gameover = True
        continue

    # print info about the current position
    room_number = hunter_y * N + hunter_x
    print('YOU ARE IN ROOM ' + str(room_number))

    # describe nearby rooms
    # figure out if the wumpus in 2 rooms away
    wumpus_around = False
    can_smell_wumpus_from = [
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)]
    for rel in can_smell_wumpus_from:
        new_y = (N + hunter_y + rel[0]) % N
        new_x = (N + hunter_x + rel[1]) % N
        if wumpus_x == new_x and wumpus_y == new_y:
            wumpus_around = True

    # figure out if other dangers in one room away
    # describes relative positions of rooms where we can go
    can_move_into = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    chipmunks_around = False
    pits_around = False
    for rel in can_move_into:
        new_y = (N + hunter_y + rel[0]) % N
        new_x = (N + hunter_x + rel[1]) % N
        if cave[new_y][new_x] == Pit:
            pits_around = True
        if cave[new_y][new_x] == Chipmunk:
            chipmunks_around = True

    # print warnings
    if chipmunks_around:
        print('CHIPMUNKS SCURRYING AROUND')
    if pits_around:
        print('I FEEL A DRAFT')
    if wumpus_around:
        print('I SMELL A WUMPUS!')

    print('TUNNELS LEAD TO ', end='')
    # select all possible moves, each pair contains delta y and delta x
    allowed_rooms = []  # a list of allowed rooms to check if the player has entered allowed move
    for move in can_move_into:
        new_y = (N + hunter_y + move[0]) % N
        new_x = (N + hunter_x + move[1]) % N
        new_room_number = new_y * N + new_x
        allowed_rooms.append(new_room_number)
        print(new_room_number, end=' ')
    print()

    action = input('SHOOT OR MOVE (S-M) ')
    if action == 'm' or action == 'M':
        # handle move
        target_room = -1
        try:
            target_room = int(input('WHICH ROOM? '))
        except:
            pass
        if target_room in allowed_rooms:
            hunter_x = target_room % N
            hunter_y = target_room // N
        else:
            print('YOU HIT THE WALL AND REMAIN IN THE SAME ROOM')
    elif action == 's' or action == 'S':
        # handle shoot
        target_room = -1  # not allowed room number
        try:
            target_room = int(input('WHICH ROOM? '))
        except:
            # the program comes here is it failed to convert the
            # player's input into an integer. In this case we do
            # nothing (just pass) making target_room to remain -1
            # which is not allowed room number.
            pass
        left_arrows -= 1
        if target_room in allowed_rooms:
            room_x = target_room % N
            room_y = target_room // N
            if room_x == wumpus_x and room_y == wumpus_y:
                print("YOU KILLED THE WUMPUS. YOU WAS JUST LUCKY")
                gameover = True
            else:
                print("YOU WASTED AN ARROW! IT'S SO LIKE YOU!")
        else:
            print('THE ARROW BOUNCED OFF A WALL AND HIT YOUR FACE.')
            gameover = True
    elif action == 'cheat':
        for y in range(N):
            for x in range(N):
                if x == hunter_x and y == hunter_y:
                    print('L', end='')
                elif x == wumpus_x and y == wumpus_y:
                    print('W', end='')
                elif cave[y][x] == Pit:
                    print('V', end='')
                elif cave[y][x] == Chipmunk:
                    print('~', end='')
                elif cave[y][x] == Empty:
                    print(' ', end='')
                else:
                    print(' ', end='?')
            print()


