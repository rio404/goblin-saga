from gameresources import *
from player import *
from enemy import *

clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 30, True)
score = 0
shootLoop = 0
roundNo = 0
newRound = True
man = None
goblinArray = []

def main():

    pygame.mixer.music.play(-1)
    global man

    while True:
        clock.tick(27)
        goblinArray.clear()
        man = Player(300, 410, 64, 64)
        goblin = Enemy(100, 415, 64, 64, 450)
        goblinArray.append(goblin)
        goblin = Enemy(200, 415, 64, 64, 450)
        goblinArray.append(goblin)
        bullets = []
        global shootLoop
        shootLoop = 0
        global roundNo
        roundNo += 1
        global newRound
        newRound = True
        run = True
        while run and goblinsAlive():
            clock.tick(27)
            keys = pygame.key.get_pressed()
            run = isExit()
            checkPause(keys)
            bullets = executeRound(man, goblinArray, bullets, keys, roundNo)
            displayNewRoundMessage(roundNo)
        if run == False:
            break
    pygame.quit()

def goblinsAlive():
    global goblinArray
    deadCount = 0
    for goblin in goblinArray:
        if not goblin.visible:
            deadCount += 1
    if deadCount == len(goblinArray):
        return False
    return True

def displayNewRoundMessage(roundNo):
    global newRound
    if newRound:
        font1 = pygame.font.SysFont('comicsans', 50)
        text = font1.render('Round '+ str(roundNo), 1, (0, 0, 0))
        win.blit(text, ((screensize_x / 2) - (text.get_width() / 2), (screensize_y / 2) - (text.get_height() / 2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        newRound = False

def isExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def checkPause(keys):
    if keys[pygame.K_ESCAPE]:
        print("GAME PAUSED")
        paused = True
        while paused:
            fontpaused = pygame.font.SysFont('comicsans', 50)
            text = fontpaused.render('Game Paused', 1, (0, 0, 0))
            win.blit(text, (screensize_x/2 - text.get_width()/2, screensize_y/2 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    k = event.key
                    if k == pygame.K_RETURN:
                        paused = False
                if event.type == pygame.QUIT:
                    pygame.quit()

def checkManJump(man, keys):
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= int((man.jumpCount ** 2) * 0.5 * neg)
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False

def checkManMovement(man, keys):
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screensize_x - man.vel - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True

def bulletShoot(bullets, man, shootLoop, keys):
    # if type(keys) is tuple:
        if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (200, 50, 0), facing))
                return (True, bullets)
        return (False, bullets)

def redrawGameWindow(man, goblinArray, bullets):
    win.blit(bg, (0, 0))  # This will draw our background image at (0,0)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (340, 10))
    man.draw(win)
    for goblin in goblinArray:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
        print("Redraw "+str(bullets.index(bullet))+"  "+str(bullet.x))
    pygame.display.update()

def manGoblinHit(man, goblin):
    global score
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

def goblinBulletHit(goblinArray, bullets):
    global score
    if(len(bullets)>0):
        for bullet in bullets:
            #print("Compare - "+str(goblinArray.index(goblin))+" and "+str(bullets.index(bullet)))
            for goblin in goblinArray:
                if goblin.visible:
                    if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                            goblin.hitbox[1]:
                        if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                                goblin.hitbox[2]:
                            score += 1
                            goblin.hit()
                            bullets.pop(bullets.index(bullet))
                            continue
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
                # print("Hit " +str(bullets.index(bullet))+" "+str(bullet.x))

            else:
                bullets.pop(bullets.index(bullet))
    return bullets

def executeRound(man, goblinArray, bullets, keys, roundNo):
    global shootLoop

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0
    for goblin in goblinArray:
        manGoblinHit(man, goblin)
    bullets = goblinBulletHit(goblinArray, list(bullets))
    isBulletShot, bullets = bulletShoot(bullets, man, shootLoop, keys)
    if isBulletShot:
        shootLoop = 1
    checkManMovement(man, keys)
    checkManJump(man, keys)
    redrawGameWindow(man, goblinArray, bullets)
    return bullets
if __name__ == '__main__':
    main()

pygame.quit()