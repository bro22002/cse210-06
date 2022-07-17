from random import choice, randrange
import pygame
from actor import Actor, Arena
from pacman_map import in_wall
from pacman_biscotti import cookis, big_cookis
import g2d
pacman_powerup =  False 

class Ghost(Actor):
    #color: 
    # 0 = red
    # 1 = pink
    # 2 = blue
    # 3 = orang
    def __init__(self, arena, pos, color):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._arena = arena
        self._color = color 
        arena.add(self)
        self._fps = 0 
        self._flag = False 
        self._dx, self._dy =2, 0
        self._pacman_powerup = False 

    def move(self):
        arena_w, arena_h = self._arena.size()

        dirs = ([(2, 0), (0, 2), (0, -2), (-2, 0)]) 

        if self._x % 8 == 0 and self._y % 8 == 0:
            dirs.remove((-self._dx, -self._dy)) 
            self._dx, self._dy = choice(dirs)

            if in_wall((self._x+self._dx), (self._y+self._dy)):
                dirs.remove((self._dx, self._dy))
                self._dx, self._dy = choice(dirs)

        if in_wall((self._x+self._dx), (self._y+self._dy)):
            dirs.remove((self._dx, self._dy))
            self._dx, self._dy = choice(dirs)
    
        self._x = self._x + self._dx
        self._y = self._y + self._dy
        
        if self._y < 0:
            self._y = 0

        elif self._y > arena_h - self._h:
            self._y = arena_h - self._h
            
        if self._x < 0:
            self._x = 0

        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

        #effetto pac-man / tunel per i fantasmi
        if (self._x == 0 and self._y == 112) and self._dx < 0: 
            self._x = 216 
            self._y = 112 

        if (self._x == 216 and self._y == 112) and self._dx > 0:
            self._x = 0 
            self._y = 112 

    def collide(self, other):
        # if pacman powerup is active then I enable fansama to 'die' if it collides with pac-man "
        if (pacman_powerup): 
            list_respawn=[(8,8), (208,8), (208,64), (8,64), (8,232), (8, 160)]
            if isinstance(other, PacMan):
                pygame.mixer.init() 
                pygame.mixer.music.load("Music/pacman_eatghost.wav")
                pygame.mixer.music.play()
                Arena.remove(self._arena, self)
                respawn = choice(list_respawn)
                Ghost(self._arena, respawn, self._color)


    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
    # ghost skin when pac-man is in power up
        if (pacman_powerup): 

            if (self._fps==6):
                self._fps = 0
                self._flag = not self._flag
            else:   
                self._fps +=1
                
            if self._dx > 0:
                if (self._flag):
                    return 16, 142
                else:
                    return 0, 142 
        
            elif self._dx < 0:
                if (self._flag):
                    return 32, 142
                else:
                    return 48, 142 
                
        
            elif self._dy > 0:
                if (self._flag):
                    return 112, 142
                else:
                    return 96, 142 
        
        
            elif self._dy < 0:
                if (self._flag):
                    return 64, 142
                else:
                    return 80, 142 
                
        
            else:
                return 16, 142
        else:
        #skin for ghost when pacman is in normal mode
            if (self._fps==6):
                self._fps = 0
                self._flag = not self._flag
            else:   
                self._fps +=1
                
            if self._dx > 0:
                if (self._flag):
                    return 0, 64+16*self._color
                else:
                    return 16, 64+16*self._color 
        
            elif self._dx < 0:
                if (self._flag):
                    return 32, 64+16*self._color
                else:
                    return 48, 64+16*self._color 
                
        
            elif self._dy > 0:
                if (self._flag):
                    return 112, 64+16*self._color
                else:
                    return 96, 64+16*self._color
        
        
            elif self._dy < 0:
                if (self._flag):
                    return 64, 64+16*self._color
                else:
                    return 80, 64+16*self._color 
                
        
            else:
                return 16, 64

class PacMan(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._lives = 4
        self._last_collision = 0 
        self._arena = arena
        self._old_direction = (0, 0)
        self._eaten_cookies = 0
        self._fps_powerup = 0
        self._fps = 0
        self._seconds = 5
        self._pacman_powerup = False
        self._flag = False
        arena.add(self)
        
    def move(self):
        arena_w, arena_h = self._arena.size()
        
        #collision with the wall
        if not (in_wall((self._x + self._dx), (self._y + self._dy))): 
            self._y += self._dy 
            self._x += self._dx
        
        if self._y < 0:
            self._y = 0
        elif self._y > arena_h - self._h:
            self._y = arena_h - self._h

        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w
        
        
        if (self._x == 0 and self._y == 112) and self._dx < 0: 
            self._x = 216 
            self._y = 112 

        if (self._x == 216 and self._y == 112) and self._dx > 0:
            self._x = 0 
            self._y = 112 

    def control(self, keys):
        if self._x % 8 == 0 and self._y % 8 == 0:
            #u, d, l, r = "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"
            u, d, l, r = "w", "s", "a", "d"
            self._old_direction = self._dx, self._dy

            if u in keys:
                self._dx, self._dy = 0, -self._speed

            elif d in keys:
                self._dx, self._dy = 0,  self._speed
                
            if l in keys:
                self._dx, self._dy = -self._speed, 0
            elif r in keys:
                self._dx, self._dy = self._speed, 0
    
            if in_wall((self._x + self._dx), (self._y + self._dy)):# wall collision control,
                #if the chosen direction goes against the wall, keep that direction before the fight
                if(self._dx, self._dy)  != (self._old_direction):
                   self._dx, self._dy = self._old_direction                   

    def lives(self) -> int:
        return self._lives

    def symbol_life(self):
        #visualization of pac-man's lives
        for i in range (self._lives): 
            lung = 130+(i * 12)
            g2d.draw_image_clip("pac-man.png", (130, 17), (12, 12), (lung, 260))
      
    def collide(self, other):
        #collision with the ghost
        if isinstance(other, Ghost) and not(pacman_powerup):
           # if pac-man had a collision within one second
            if self._arena.count() - self._last_collision < 30:
                return
            self._last_collision = self._arena.count()
            #pac-man respawn after collision
            self._dx, self._dy = 0, 0
            self._x = 112
            self._y = 88
            
            self._lives-=1
            if (self._lives == 0):
                Arena.remove(self._arena, self)
        # count cookies that  pacman eats
        if isinstance(other, big_cookies):
            self._eaten_cookies +=1
            self._seconds = 0
        
        if isinstance(other, cookies):
            self._eaten_cookies +=1   

    def seconds_powerup(self):
        # pca-man powerup timer function
        global pacman_powerup
        self._fps_powerup +=1
        if self._fps_powerup == 30:
            self._fps_powerup = 0
            self._seconds +=1
        #activation of the power up only if it is less than 5
        if self._seconds < 5: 
            pacman_powerup = True
        else:
            pacman_powerup = False

    def pacman_powerup(self):
        return pacman_powerup

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def eaten_cookies(self):
        return self._eaten_cookies

    def symbol(self):
        #alternation of pac-man symbols
        if (self._fps==6):
            self._fps = 0
            self._flag = not self._flag
        else:   
            self._fps +=1
                
        if self._dx > 0:
            if (self._flag):
                return 0, 0
            else:
                return 16, 0 
        
        elif self._dx < 0:
            if (self._flag):
                return 0, 16
            else:
                return 16, 16
        
        elif self._dy > 0:
            if (self._flag):
                return 0, 48
            else:
                return 16, 48
        
        elif self._dy < 0:
            if (self._flag):
                return 0, 32
            else:
                return 16, 32
        
        else:
            return 0, 0

class cookies:
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 2, 2
        self._arena = arena
        arena.add(self)
        self._cookis = cookis() 
        
    def make_cookis(arena):
            lista_cookis = cookis()
            for coordinata_cookis in lista_cookis:
                y, x = coordinata_cookis
                y = (y*8)-2
                x = x*8
                cookies(arena,(x,y))

    def collide(self, other):
        #if pac-man collides with a cookie, he removes the cookie from the arena
        if isinstance(other, PacMan):
            Arena.remove(self._arena, self )
            if not(pygame.mixer.music.get_busy() == True):
                pygame.mixer.init() 
                pygame.mixer.music.load("Music/pacman_chomp.wav")
                pygame.mixer.music.play()
                
    def move(self):
        pass
    
    def position(self):
        
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
            return 167, 55
            
class big_cookies:
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 8, 8
        self._arena = arena
        arena.add(self)
        
    def make_big_cookis(arena):
            lista_big_cookis = big_cookis()
            for big_cooki in lista_big_cookis:
                y, x = big_cooki
                y = (y*8)-5
                x = (x*8)-3
                big_cookies(arena,(x,y))
    
    def move(self):
        pass

    def collide(self, other):

        if isinstance(other, PacMan):
            Arena.remove(self._arena, self)

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
            return 180, 52
