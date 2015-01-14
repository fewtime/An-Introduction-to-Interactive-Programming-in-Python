# 14.11.09

# program template for Spaceship
import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRAME_CENTER = [WIDTH // 2, HEIGHT // 2]
score = 0
lives = 3
time = 0.5
current_rock_number = 0
started = False

FRICTION_RATIO = 0.03
ACCELERATION = 0.3
MISSILE_ANGLE = 45
MISSILE_SPEED_CON = 5
ROTATION_VEL = 0.2

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        global WIDTH, HEIGHT        
        forward = angle_to_vector(self.angle)      
        self.vel[0] = (1 - FRICTION_RATIO) * self.vel[0]
        self.vel[1] = (1 - FRICTION_RATIO) * self.vel[1]
        if self.thrust:
            self.vel[0] += ACCELERATION * forward[0]
            self.vel[1] += ACCELERATION * forward[1]
            ship_thrust_sound.play()
            self.image_center[0] = 135
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            self.image_center[0] = 45
        
        self.angle += self.angle_vel
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        new_missile_pos = [0, 0]
        new_missile_pos[0] = self.pos[0] + MISSILE_ANGLE * forward[0]
        new_missile_pos[1] = self.pos[1] + MISSILE_ANGLE * forward[1]
        new_missile_vel = [0, 0]
        new_missile_vel[0] = self.vel[0] + MISSILE_SPEED_CON * forward[0]
        new_missile_vel[1] = self.vel[1] + MISSILE_SPEED_CON * forward[1]
        missile_sound.rewind()
        missile_sound.play()
        missile_group.add(Sprite(new_missile_pos, new_missile_vel, 0, 0,
                          missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            tmp_center=[self.image_center[0] + self.age* self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, tmp_center, self.image_size, self.pos, self.image_size,self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)    
    
    def update(self):
        global WIDTH, HEIGHT
        
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        
        if self.age <= self.lifespan:
            return True
        else:
            return False        

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.get_position(), other_object.get_position()) <=\
                (self.get_radius() + other_object.get_radius())


# draw helper function
def process_sprite_group(group, canvas):
    for item in set(group):
        if item.update():
            item.draw(canvas)
        else:
            group.remove(item)
        
# group_collide helper function
def group_collide(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            new_explosion = Sprite(item.pos, [0, 0], 0, 0,
                                   explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            group.remove(item)
            return True
    return False

# group_group_collide helper function
def group_group_collide(group_one, group_two):
    for item in set(group_one):
        if group_collide(group_two, item):
            group_one.discard(item)
            return True
    return False

# new_game helper function(Initialize the value)
        
def draw(canvas):
    global started
    global time, current_rock_number
    global lives, score
    
    if started:
        if timer.is_running() == False:
            lives = 3
            score = 0
            current_rock_number = 0
        timer.start()
        soundtrack.play()
    else:
        for rock in set(rock_group):
            rock_group.remove(rock)
        timer.stop()
        soundtrack.rewind()

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("LIFE: " + str(lives), [30, 60], 25, "WHITE")
    canvas.draw_text("SCORE: " + str(score), [600, 60], 25, "WHITE")
    
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), FRAME_CENTER, splash_info.get_size())
    
    # my_ship lives
    if group_collide(rock_group, my_ship):
        current_rock_number -= 1
        lives -= 1
        if lives == 0:
            started = False
            
    # missile and rock        
    if group_group_collide(missile_group, rock_group):
        score += 5
        current_rock_number -= 1
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
            
# timer handler that spawns a rock    
def rock_spawner():
    global current_rock_number, rock_group, score
    
    new_rock_pos = [random.randint(0, WIDTH + 1), random.randint(0, HEIGHT + 1)]
    new_rock_angle_vel = random.random() * 0.4 - 0.2
    new_rock_vel = [0, 0]
    new_rock_vel[0] = random.random() * (score / 397.0) - 1.5
    new_rock_vel[1] = random.random() * (score / 397.0) - 1.5
    
    new_rock = Sprite(new_rock_pos, new_rock_vel, 0, new_rock_angle_vel, asteroid_image, asteroid_info)
    
    if current_rock_number < 12 and not new_rock.collide(my_ship):
        current_rock_number += 1
        rock_group.add(new_rock)

# keydown / keyup / mouseclick handler
def keydown_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = -ROTATION_VEL
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = ROTATION_VEL
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    elif key == simplegui.KEY_MAP['space']:
        pass

def mouse_handler(pos):
    global started
    splash_size = splash_info.get_size()
    
    if pos[0] >= FRAME_CENTER[0] - splash_size[0] // 2 and\
        pos[0] <= FRAME_CENTER[0] + splash_size[0] // 2 and\
        pos[1] >= FRAME_CENTER[1] - splash_size[1] // 2 and\
        pos[1] <= FRAME_CENTER[1] + splash_size[1] // 2:
            if timer.is_running() == False:
                started = True
    else:
        started = False
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
