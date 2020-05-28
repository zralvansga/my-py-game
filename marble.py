# BIGPROJECT4
# marble
# by ejra
# inspired by childhood games
# start date 26 mei 2020
# finish date 26 juni 2020

import pygame,sys,random
from pygame.locals import *

FPS = 60
LEBARWINDOW = 480
TINGGIWINDOW = 480

UKURANMARBLE = 36
JARI2MARBLE = int (UKURANMARBLE* 0.5)
UKURANCELAH = 10

LEBARPAPAN = 7
TINGGIPAPAN = 7

#ukuran margin
XMARGIN = int((LEBARWINDOW - (LEBARPAPAN * (UKURANMARBLE + UKURANCELAH))) / 2)
YMARGIN = int((TINGGIWINDOW - (TINGGIPAPAN * (UKURANMARBLE + UKURANCELAH))) / 2)

# warna yang dibutuhkan
#               R   G   B
PUTIH       = (255,255,255)
JINGGA      = (255,180,  0)
JINGGATUA   = (150, 75,  0)
UNGU        = (200, 10,255)
LIMEHIJAU   = (150,255,  0)
BIRU        = (170,100,255)
BIRUTUA     = (100,  0,150)

BGCOLOR1 = UNGU
BGCOLOR2 = LIMEHIJAU

MARBLECOLOR = JINGGA
MARBLECOLOR2 = JINGGATUA
RINGCOLOR = PUTIH
BOARDCOLOR = BIRU
BOARDCOLOR2 = BIRUTUA
WINTEKSCOLOR = PUTIH

# gambar objek
MARBLE = 'marble'
CURMARBLE = 'curmarble'
RING = 'ring'

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((LEBARWINDOW,TINGGIWINDOW))
    pygame.display.set_caption('Marbles')

    xmouse = 0
    ymouse = 0
    prevselect = (None,None)
    mousehold = False
    win = False
    congratsteks = ['Fantastic!','Magnificent!','Amazing!','Well Played!','Awesome!','Good Game!','Well Done!']
    randomcongrats = ''

    #set level
    #set marble tabel LEBARPAPAN x TINGGIPAPAN
    level = 3
    marbles = setLevel(level)

    while True:
        mouseklik = False
        mouserelease = False
        gambarBG(level)
        refreshMarble(marbles)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEMOTION and mousehold == True:
                print ("mouse hold")
                xmouse, ymouse = event.pos
            
            elif event.type == MOUSEBUTTONUP:
                print ("mouse lepas")
                xmouse, ymouse = event.pos
                mousehold = False
                mouserelease = True

            elif event.type == MOUSEBUTTONDOWN:
                xmouse, ymouse = event.pos
                mouseklik = True
                print("mouse tekan")

            elif event.type == MOUSEMOTION:
                xmouse, ymouse = event.pos

        if tampilReset(xmouse,ymouse,mouseklik) == True:
            #set level
            marbles = setLevel(level)
            win = False

        if win == True:
            wincelebration(randomcongrats)
        else:
            if mousehold == True:
                xmouse, ymouse = pygame.mouse.get_pos()
                gambarObjek(CURMARBLE,xmouse,ymouse)
            else:
                boxx,boxy = sentuhMarble(xmouse,ymouse)
                if mouserelease == True:
                    print(marbles)
                    mouserelease = False
                    # if boxx != None and boxy != None:
                    marbles = cekmarblerelease(boxx,boxy,prevselect,marbles)
                    if marbles != None:
                        if hitungmarbles(marbles) == 1:
                            win = True
                            print('menang')
                            randomcongrats = random.choice(congratsteks)
                        prevselect = (None,None)
                    print(marbles)
                    # kembalikan marble
                    
                if boxx != None and boxy != None:
                    # print("tersentuh")
                    if marbles[boxx][boxy]:
                        gambarObjek(RING,boxx,boxy)
                    if marbles[boxx][boxy] and mouseklik == True:
                        mousehold = True
                        prevselect = (boxx,boxy)
                        marbles[boxx][boxy] = False 

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def lefttopkoordinatbox(boxx,boxy):
    left = boxx * (UKURANMARBLE + UKURANCELAH) + XMARGIN
    top = boxy * (UKURANMARBLE + UKURANCELAH) + YMARGIN
    return (left,top)

def gambarWadah2(boxx,boxy):
    left,top = lefttopkoordinatbox(boxx,boxy)
    pygame.draw.circle(DISPLAYSURF,BOARDCOLOR2,(left+JARI2MARBLE+3,top+JARI2MARBLE+3),JARI2MARBLE+15)

def gambarWadah(boxx,boxy):
    left,top = lefttopkoordinatbox(boxx,boxy)
    pygame.draw.circle(DISPLAYSURF,BOARDCOLOR,(left+JARI2MARBLE,top+JARI2MARBLE),JARI2MARBLE+10)

def gambarObjek(bentuk,boxx,boxy):
    left,top = lefttopkoordinatbox(boxx,boxy)
    if bentuk == MARBLE:
        pygame.draw.circle(DISPLAYSURF,MARBLECOLOR2,(left+JARI2MARBLE+2,top+JARI2MARBLE+2),JARI2MARBLE)
        pygame.draw.circle(DISPLAYSURF,MARBLECOLOR,(left+JARI2MARBLE,top+JARI2MARBLE),JARI2MARBLE)
    elif bentuk == RING:
        pygame.draw.circle(DISPLAYSURF,RINGCOLOR,(left+JARI2MARBLE,top+JARI2MARBLE),JARI2MARBLE+3,3)
    elif bentuk == CURMARBLE:
        pygame.draw.circle(DISPLAYSURF,MARBLECOLOR2,(boxx+2,boxy+2),JARI2MARBLE)
        pygame.draw.circle(DISPLAYSURF,MARBLECOLOR,(boxx,boxy),JARI2MARBLE)

def sentuhMarble(x,y):
    for boxx in range(LEBARPAPAN):
        for boxy in range(TINGGIPAPAN):
            left, top = lefttopkoordinatbox(boxx,boxy)
            boxrect = pygame.Rect(left,top,UKURANMARBLE,UKURANMARBLE)
            if boxrect.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)

def refreshMarble(marbles):
    for i in range(LEBARPAPAN):
        for j in range(TINGGIPAPAN):
            if marbles[i][j] == True:
                gambarObjek(MARBLE,i,j)

def cekmarblerelease(boxx,boxy,prevselect,marbles):
    if prevselect == (None,None):
        return marbles
    oldboxx,oldboxy = prevselect                               
    if boxx == None and boxy == None :
        boxx,boxy = prevselect
        marbles[boxx][boxy] = True 
    if marbles[boxx][boxy] == True :
        boxx,boxy = prevselect
        marbles[boxx][boxy] = True 
    else:
        #               kanan            
        if (boxx == oldboxx + 2 and boxy == oldboxy and marbles[oldboxx + 1][oldboxy] == True) :
            marbles[boxx][boxy] = True
            marbles[oldboxx + 1][oldboxy] = False
        #               kiri
        elif (boxx == oldboxx - 2 and boxy == oldboxy and marbles[oldboxx - 1][oldboxy] == True):
            marbles[boxx][boxy] = True
            marbles[oldboxx - 1][oldboxy] = False
        #               atas
        elif (boxx == oldboxx  and boxy == oldboxy + 2 and marbles[oldboxx][oldboxy  + 1] == True):
            marbles[boxx][boxy] = True
            marbles[oldboxx][oldboxy + 1] = False
        #               bawah
        elif (boxx == oldboxx  and boxy == oldboxy - 2 and marbles[oldboxx][oldboxy  - 1] == True):
            marbles[boxx][boxy] = True
            marbles[oldboxx][oldboxy - 1] = False
        else:
            boxx,boxy = prevselect
            marbles[boxx][boxy] = True 
    return marbles

def hitungmarbles(marbles):
    jum = 0
    for i in sum(marbles,[]):
        if i == True:
            jum += 1
    print(jum)
    return jum

def wincelebration(randomcongrats):
    settingFont = pygame.font.Font('freesansbold.ttf',36)
    permukaanteks = settingFont.render(randomcongrats,True,WINTEKSCOLOR)
    teksRectObj = permukaanteks.get_rect()
    teksRectObj.center = (int(LEBARWINDOW/2),int(TINGGIWINDOW/4))

    DISPLAYSURF.blit(permukaanteks,teksRectObj)

def gambarBG(level):
    if level == 1:
        DISPLAYSURF.fill(BGCOLOR1)
        for i in range(7):
            gambarWadah2(i,3)
        for i in range(7):
            gambarWadah(i,3)

    elif level == 2:
        DISPLAYSURF.fill(BGCOLOR1)
        for i in range(1,6):
            for j in range(1,6):
                gambarWadah2(i,j)
        for i in range(1,6):
            for j in range(1,6):
                gambarWadah(i,j)
    elif level == 3:
        DISPLAYSURF.fill(BGCOLOR1)
        for i in range(7):
            for j in range(7):
                gambarWadah2(i,j)
        for i in range(7):
            for j in range(7):
                gambarWadah(i,j)
    else:
        #default level 1
        DISPLAYSURF.fill(BGCOLOR1)
        for i in range(7):
            for j in range(1):
                gambarWadah2(i,j)
        for i in range(7):
            for j in range(1):
                gambarWadah(i,j)

def setLevel(level):
    # kosongkan marbles table
    marbles = []

    # isi dengan False
    for i in range(LEBARPAPAN):
        marbles.append([False] * TINGGIPAPAN)

    # inisialisasi level
    if level == 1:
        marbles[int(LEBARPAPAN/2)-2][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)-1][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)+1][int(TINGGIPAPAN/2)] = True
    elif level == 2:
        marbles[int(LEBARPAPAN/2)-1][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)][int(TINGGIPAPAN/2)-1] = True
        marbles[int(LEBARPAPAN/2)+1][int(TINGGIPAPAN/2)+1] = True
    elif level == 3:
        marbles[int(LEBARPAPAN/2)-2][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)-1][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)+1][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)+2][int(TINGGIPAPAN/2)] = True

        marbles[int(LEBARPAPAN/2)-1][int(TINGGIPAPAN/2)-1] = True
        marbles[int(LEBARPAPAN/2)][int(TINGGIPAPAN/2)-1] = True
        marbles[int(LEBARPAPAN/2)+1][int(TINGGIPAPAN/2)-1] = True

        marbles[int(LEBARPAPAN/2)][int(TINGGIPAPAN/2)-2] = True
        #===========================================
        # ========= tambah level disini ===========
        #===========================================
    else:
        #default level 1
        marbles[int(LEBARPAPAN/2)-2][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)-1][int(TINGGIPAPAN/2)] = True
        marbles[int(LEBARPAPAN/2)+1][int(TINGGIPAPAN/2)] = True
    
    # kembalikan nilai marbles table
    return marbles

def tampilReset(x,y,mouseklik):
    fontsize = 18
    settingFont = pygame.font.Font('freesansbold.ttf',fontsize)
    permukaanteks = settingFont.render('Reset',True,WINTEKSCOLOR)
    teksRectObj = permukaanteks.get_rect()
    teksRectObj.center = (int(LEBARWINDOW/10),int(TINGGIWINDOW/20))
    
    if teksRectObj.collidepoint(x,y):
        fontsize = 20
        settingFont = pygame.font.Font('freesansbold.ttf',fontsize)
        permukaanteks = settingFont.render('Reset',True,WINTEKSCOLOR)
        teksRectObj = permukaanteks.get_rect()
        teksRectObj.center = (int(LEBARWINDOW/10),int(TINGGIWINDOW/20))
        DISPLAYSURF.blit(permukaanteks,teksRectObj)
        if mouseklik == True:
            return True
        else:
            return False
    DISPLAYSURF.blit(permukaanteks,teksRectObj)
    

if __name__ == '__main__':
    main()