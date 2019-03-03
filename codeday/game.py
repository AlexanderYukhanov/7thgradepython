#from __future__ import print_function

# all scenes
scenes = {}


class Player:
    items = []
    alive = True


# Prints the scene description
def describe_scene(scene):
    print(scene.name)
    print()
    print(scene.description)
    print()

    # describe items in the room
    if len(scene.items) == 0:
        print("There is nothing around here")
    else:
        print("You see:")
        for i in range(0, len(scene.items)):
            print(" - ", scene.items[i])


# Return a list of actions which can be performed
def get_list_of_available_actions(player, scene):
    # compose a list of actions which can be performed
    actions = []

    # all actions defined in the scene
    for a in scene.actions:
        actions.append(a)

    # actions applicable to the items in the scene
    for i in range(0, len(scene.items)):
        # take an item
        def take_item(item):
            def _take_item(player):
                player.items.append(scene.items[item])
                scene.items = scene.items[:item] + scene.items[item + 1:]
                return player
            return _take_item
        actions.append(('take ' + scene.items[i], None, take_item(i)))

    # actions applicable to the item in the player's inventory
    for i in range(0, len(player.items)):
        # drop the item
        def drop_item(item):
            def _drop_item(player):
                scene.items.append(player.items[item])
                player.items = player.items[:item] + player.items[item + 1:]
                return player
            return _drop_item

        actions.append(('drop ' + player.items[i], None, drop_item(i)))

    return actions


# print information about the player
def describe_player(player):
    if player.items:
        print('Your inventory:')
        for item in player.items:
            print(" - ", item)
    else:
        print('Your pockets are empty')


# prints description of the scene and available actions
# asks the player to select an action
# returns name of the new scene or None if the player should stay in the same scene
def process_scene(player, scene):
    describe_scene(scene)
    print()
    describe_player(player)

    print()
    print('You can:')
    available_actions = get_list_of_available_actions(player, scene)
    for i in range(0, len(available_actions)):
        print(i + 1, available_actions[i][0])

    choice = input("What would you do?: ")
    choice = int(choice) - 1
    selected_action = available_actions[choice]
    effect = selected_action[2]
    if effect:
        player = effect(player)
    return player, selected_action[1]


def game(starting_scene):
    player = Player()
    scene = scenes[starting_scene]
    while player.alive:
        player, new_scene = process_scene(player, scene)
        if new_scene:
            scene = scenes[new_scene]


# description of scenes
class Road1:
    name = 'Somewhere on a road'
    description = 'Dirty road under your feet. Wind is blowing'
    items = ['rock', 'stick']
    actions = [
        ('move North', 'restroom', None)
    ]


def exploit_when_toilet_flushed(player):
    print("Oh noooo...")
    print("It was a bomb detonator, you are doomed")
    player.alive = False
    return player


class Restroom:
    name = 'A restroom'
    description = 'Nothing is really interesting here, just do your business and leave'
    items = ['a bottle']
    actions = [
        ('leave', 'road1', None),
        ('flash a toilet', 'restroom', exploit_when_toilet_flushed)
    ]


scenes.update({
    'restroom': Restroom(),
    'road1': Road1()})


game('restroom')
