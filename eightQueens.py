import pyglet
from pyglet.window import Window, mouse, gl
bgimage = pyglet.image.load("load/chessb1.jpg")#image of chess board
queen = pyglet.image.load("load/qv5.1.png") #image of queen
errortile = pyglet.image.load('load/error.png') #image for error tiles
myicon = pyglet.image.load("load/iii.jpg") ##game icon

width = bgimage.width #widht is calculated of chesssboard, accurate value can be calculated
height = bgimage.height #height is calculated of chesssboard, accurate value can be calculated
mygame = Window(width, height,
                resizable=False,
                caption="eight queens",
                config=pyglet.gl.Config(double_buffer = True),
                vsync=False)
platform = pyglet.window.get_platform()  # access current platform
display = platform.get_default_display()  # access current display
screen = display.get_default_screen()  # access current screen
mygame.set_location(screen.width // 2 - 325, screen.height // 2 - 325)  ##center
 
loseimage = pyglet.image.load("load/lose.png")
lose_sprite=pyglet.sprite.Sprite(loseimage,width//6,height//3)
lose_sprite.visible = False
 
winimage = pyglet.image.load("load/win.png")
win_sprite=pyglet.sprite.Sprite(winimage,width//4,height//3)
win_sprite.visible = False
validmove = False#initially validmove is false
 
queens = 0  #initially number of queen is zero
wincheck = False    #initially wincheck variable is false
 
errorTilesList = [[0] * 8 for i in range(8)]   #array for error tiles i.e red color background
queensList = [[0] * 8 for i in range(8)]   #array for queens
 
tQueens = []    #empty list to store visible queens
 
batch_queens = pyglet.graphics.Batch()  #used to improve the performance of the code
batch_errortile = pyglet.graphics.Batch()   #used to improve the performance of the code
 
queenlabel = pyglet.text.Label("",
                               font_name='Times New Roman',
                               font_size=24,
                               x=190, y=175,
                               anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
 
# queens and error tiles are placed through nested loops
for y in range(0, 8):
    for x in range(0, 8):#queens and error tiles are placed on each and every box
        queensList[x][y] = (pyglet.sprite.Sprite(queen, (65 * x + 65), (65 * y + 65), batch=batch_queens))
        errorTilesList[x][y] = (
        pyglet.sprite.Sprite(errortile, 55 + (errortile.width * x) * 1.03, 55 + (errortile.height * y) * 1.03,
                             batch=batch_errortile))    #error tiles are placed on each and every box
 
        queensList[x][y].visible = False
        errorTilesList[x][y].visible = False
 
 
     
def checkMove(x, y):
    global queens, validmove, wincheck  # global variables are used
    if queensList[x][y].visible is False:  # for undo functionality
        if queens >= 8:  # max 8 queens can be placed
            queenlabel.text = "no more queen can be placed"
            queensList[x][y].visible = False
 
        else:
            queensList[x][y].visible = True #for visibility
            queens = queens + 1
            if [x, y] not in tQueens:
                tQueens.append([x, y])
            if validmove == True and queens == 8:
                win_sprite.visible = True   #win image will appear
            if validmove == False and queens ==8:
                lose_sprite.visible = True
 
    else:
        tQueens.remove([x, y])
        queensList[x][y].visible = False
        queens = queens - 1
 
    for i in range(0, 8):   #total boxes are 8
        for j in range(0, 8):   #total boxes are 8
            errorTilesList[j][i].visible = False  # visibility is defined false
    for j in range(0, len(tQueens)):
        for k in range(0, len(tQueens)):
            X = tQueens[j][0]  # coordinate 1   ##X cordinate of queen 1
            Y = tQueens[j][1]  # coordinate 1##Y cordinate of queen 1
            X1 = tQueens[k][0]  # coordinate 2##X1 cordinate of queen 2
            Y1 = tQueens[k][1]  # coordinate 2##Y2 cordinate of queen 2
            # cheking for illegal moves in horizontal,verticle and diagonal
            if X == X1 and k != j:
                errorTilesList[X][Y].visible = True  # error tile is visible for 1st queen
                errorTilesList[X1][Y1].visible = True  # error tile is visible for 2nd queen
                validmove = False  # illegal move
            elif Y == Y1 and k != j:
                errorTilesList[X][Y].visible = True  # error tile is visible for 1st queen
                errorTilesList[X1][Y1].visible = True  # error tile is visible for 2nd queen
                validmove = False  # illegal move
             #to check in diagonal   
            elif abs(X - X1) == abs(Y - Y1) and k != j: #abs to convert negative to positive
                errorTilesList[X][Y].visible = True  # error tile is visible for 1st queen
                errorTilesList[X1][Y1].visible = True  # error tile is visible for 2nd queen
                validmove = False  # illegal move
                # conditions for legal moves
            elif X != X1 and k != j and Y != Y1 and k != j and abs(X - X1) != abs(Y - Y1) and k != j:   #abs to convert negative to positive ##to cover diagonal in positive and neggative direction
                validmove = True  # valid move variable is set to true
                 
@mygame.event
def on_mouse_press(x, y, button, modifiers):
    global queens, validmove, wincheck  # these are the global variables
    if button == mouse.LEFT:  # if lefty click is pressed
        for i in range(8):
            for j in range(8):
                if ((j * 69) +55<= x < ((j + 1) * 69)+55 and (
                        x > 50 or x <= 602)):  # each tile is covered through nested loops
                    if ((i * 67)+63 <= y < ((i + 1) * 67) +63 and (
                            y < 591 or y > 55)):  # previously each tile was defined individually
                        checkMove(j, i)  # x any y coordinates are send as an argument to checckMove function
 
                        # functionality of right key is removed

@mygame.event
def on_draw():
    mygame.clear()
    bgimage.blit((width - bgimage.width) / 2, (height - bgimage.height) / 2)
    batch_errortile.draw()
    batch_queens.draw()
    win_sprite.draw()
    lose_sprite.draw()
 
# auto update
def update(dt):
    on_draw()  # draw function is updated
pyglet.clock.schedule_interval(update, 1 / 60)  # clock for function auto update
# Launching the app window
 
pyglet.app.run()
