# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, counter
    state = 0
    counter = 0
    exposed = dict()
    deck = range(1, 9)
    deck1 = range(1, 9)
    deck.extend(deck1)
    random.shuffle(deck)
    for n in range(17):
        exposed[n] = False

# define event handlers
def mouseclick(position):
    # add game state logic here
    global state, card1, card2, counter
    card_num = position[0] / 50
    if state == 0:
        if exposed[card_num] == False:
            card1 = card_num
            exposed[card1] = True
            state = 1
    elif state == 1:
        if exposed[card_num] == False:
            card2 = card_num
            exposed[card2] = True
            state = 2
            counter += 1
    else:
        if exposed[card_num] == False:
            if deck[card1] != deck[card2]:
                exposed[card1] = False
                exposed[card2] = False
            card1 = card_num
            exposed[card1] = True
            state = 1
            counter += 1
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    pos = [7, 75]
    for number in range(len(deck)):
        # use numbers
        #canvas.draw_text(str(deck[number]), (pos), 72, 'Black')
        # use images
        if deck[number] == 1:
            canvas.draw_image(image1, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 2:
            canvas.draw_image(image2, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 3:
            canvas.draw_image(image3, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 4:
            canvas.draw_image(image4, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 5:
            canvas.draw_image(image5, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 6:
            canvas.draw_image(image6, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 7:
            canvas.draw_image(image7, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        if deck[number] == 8:
            canvas.draw_image(image8, (376, 530), (753, 1061), (number * 50 + 25, 50), (50, 100))
        pos[0] += 50
    for key in exposed.keys():
        canvas.draw_polygon([(key * 50, 0), (key * 50 + 50, 0), (key * 50 + 50, 100), (key * 50, 100)], 1, 'Grey')
        if exposed[key] == False:
            # use image as back
            canvas.draw_image(image, (377, 528), (755, 1057), (key * 50 + 25, 50), (50, 100))
            # use green back
            #canvas.draw_polygon([(key * 50, 0), (key * 50 + 50, 0), (key * 50 + 50, 100), (key * 50, 100)], 1, 'Grey', 'Green')
    label.set_text("Turns = " + str(counter))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background('SteelBlue')
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
image = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/back_card.png')
image1 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/1.png')
image2 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/2.png')
image3 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/3.png')
image4 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/4.png')
image5 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/5.png')
image6 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/6.png')
image7 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/7.png')
image8 = simplegui.load_image('https://dl.dropboxusercontent.com/u/19384330/8.png')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
