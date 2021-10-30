import pygame, math
pygame.init()

class Sprite(pygame.sprite.Sprite):
    def __init__(self,scene):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.name = ""
        self.screen = scene.screen
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.Bounds()
        self.rect.center = (self.x, self.y)

    def Bounds(self):
        w = self.screen.get_width()
        h = self.screen.get_height()

        if self.x > w - 50:
            self.x = w - 50
        if self.x < 0 - 50:
            self.x = 0 - 50
        if self.y > h - 50:
            self.y = h - 50
        if self.y < 0 - 50:
            self.y = -50

class Scene(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 500))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.sprites = []
        self.myFont = pygame.font.SysFont("Aerial", 32)
        self.title = self.myFont.render("Graveyard", 1, (0, 0, 0))
        self.x = 500000
        self.y = 0
        self.x1 = 0
        self.y1 = 0
        self.time = 0
        self.timer = self.myFont.render("Time: " + str(self.time), 1, (0, 0, 0))
        self.wait = 0

    def start(self):
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.Go = True
        while self.Go:
            self.loop()

    def loop(self):
        self.time = self.time + 1
        timer = self.myFont.render("Time: " + str(int(self.time / 10)), 1, (0, 0, 0))
        self.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Go = False

        self.screen.blit(self.background, (0, 0))
        for i in self.sprites:
            i.update()
            if i.name == "player":
                if (self.flash() == True):
                    pygame.draw.circle(self.screen, (255,255,153), (i.x + 50, i.y + 45), 50)
                self.keys(i)
                self.x = i.x
                self.y = i.y
            if i.name == "ghost":
                self.x1 = i.x
                self.y1 = i.y
                if(i.x > self.x + 25):
                    i.dx = -self.time / 100
                elif (i.x == self.x + 25):
                    i.dx = 0
                else:
                    i.dx = self.time / 100
                if (i.y > self.y + 20):
                    i.dy = -self.time / 100
                elif (i.y == self.y + 20):
                    i.dy = 0
                else:
                    i.dy = self.time / 100
                if(self.collision() == 1):
                    self.Go = False
                elif(self.collision() == 0):
                    i.x = 490
                    i.y = 100
            self.screen.blit(i.image, (i.x, i.y))

        self.screen.blit(self.title, (320, 30))
        self.screen.blit(timer, (320, 435))

        pygame.display.flip()


    def keys(self,Sprite):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Sprite.dx = -5
        elif keys[pygame.K_RIGHT]:
            Sprite.dx = 5
        elif keys[pygame.K_UP]:
            Sprite.dy = -5
        elif keys[pygame.K_DOWN]:
            Sprite.dy = 5
        else:
            Sprite.dy = 0
            Sprite.dx = 0

    def flash(self):
        if(self.wait > 600):
            return False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.wait = self.wait + 1
            return True
        else:
            return False

    def collision(self):
        deltaX = (self.x + 25) - (self.x1)
        deltaY = (self.y + 20) - (self.y1)


        rad = deltaX * deltaX + deltaY * deltaY
        dist = math.sqrt(rad)

        if(dist < 50 and self.flash() == True):
            return 0
        elif(dist < 20 and self.flash() == False):
            return 1
        else:
            return 2

def main():

    game = Scene()
    game.background.fill((6, 117, 39))

    tree_img = pygame.image.load('New Piskel (1).png')
    ghost_img = pygame.image.load('New Piskel (2).png')
    grave_img = pygame.image.load('New Piskel (6).png')
    player_img = pygame.image.load('New Piskel (7).png')

    ghost = Sprite(game)
    ghost.image = ghost_img
    ghost.name = "ghost"
    ghost.y = 1000

    tree = Sprite(game)
    tree.image = tree_img
    tree.y = 20
    tree.x = 400

    grave = Sprite(game)
    grave.image = grave_img
    grave.x = 490
    grave.y = 100

    player = Sprite(game)
    player.image = player_img
    player.x = 450
    player.y = 125
    player.name ="player"
    game.sprites = [ghost, tree , grave, player]

    game.start()

if __name__ == "__main__":
    main()