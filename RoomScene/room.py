import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from box import Cube
from light import Light
from load_utils import load_obj, load_texture
from pywavefront import Wavefront, visualization
from camera import Camera
from collections import defaultdict

room = None
bed = None
sword = None
anvil = None
cameras = None
camera = None
current_camera = None
lights_on = None
light_camera = None
light_bookshelf_left = None
light_bookshelf_right = None
bookshelf_left = None
bookshelf_left_2 = None
bookshelf_right = None
bookshelf_front = None
skull_painting = None
creeper_painting = None
lights_on = None
torch_left = None
torch_right = None
chest_low = None
chest_up = None
def load_all_objects():
    global room, bed, sword, anvil, cameras, camera, current_camera
    global lights_on, light_camera, light_bookshelf_left, light_bookshelf_right
    global bookshelf_left, bookshelf_left_2, bookshelf_right, bookshelf_front, skull_painting
    global creeper_painting, lights_on, torch_left, torch_right, chest_low, chest_up
    lights_on = [1,1,1,1]
    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [1, 1, 1, 1.0]
    
    room_size = [8,3,5]

    # TEXTURES
    stone = load_texture("./textures/stone.png")
    cobblestone = load_texture("./textures/cobblestone.jpeg")
    plank_texture = load_texture("./textures/planks.png")
    bookshelf_texture = load_texture("./textures/bookshelf.png")
    torch_texture = load_texture("./textures/torch_.png")
    chest_side_texture_low = load_texture("./textures/chest_side_low.png")
    chest_front_texture = load_texture("./textures/chest_low_d.png")
    black_texture = load_texture("./textures/black.png")
    chest_up_front_texture = load_texture("./textures/chest_front_u.png")
    chest_up_side_texture = load_texture("./textures/chest_side_up.png")
    chest_up_texture = load_texture("./textures/chest_up.png")
    # OBJECT-TEXTURES
    room_textures = {
        "front": stone,
        "left": stone,
        "right": stone,
        "back": stone,
        "top": cobblestone,
        "bottom": plank_texture,
    }
    room_texture_coords = {
        "bottom": [(0,0), (0,5), (8,5),(8,0)],
        "top": [(0,0), (0,5), (8,5), (8,0)],
        "back": [(0,0), (0,3),(8,3),(8,0)],
        "left": [(0,0),(0,3),(5,3),(5,0)],
        "right": [(0,0),(0,3),(5,3),(5,0)],
    }    
    
    bookshelf_textures = {
        "front": bookshelf_texture,
        "left": bookshelf_texture,
        "right": bookshelf_texture,
        "back": bookshelf_texture,
        "top": plank_texture,
        "bottom": plank_texture,
    }
    bookshelf_left_coords = {
        "top": [(0,0),(0,4),(1,4),(1,0)],
        "right":[(0,0),(0,1),(4,1),(4,0)]
    }
    bookshelf_right_coords = {
        "top":[(0,0),(0,1),(2,1),(4,0)],
        "left":[(0,0),(0,1),(2,1),(2,0)]
    }
    bookshelf_front_coords = {
        "front": [(0,0), (0,1),(2,1),(2,0)],
        "top": [(0,0), (0,1),(2,1),(2,0)],
        "back": [(0,0), (0,1),(2,1),(2,0)],
    }

    chest_low_textures = {
        "front": chest_front_texture,
        "up": black_texture,
        "left": chest_side_texture_low,
        "back": chest_side_texture_low,
        "right": chest_side_texture_low
    }
    chest_up_textures = {
        "front": chest_up_front_texture,
        "up": chest_up_texture,
        "left": chest_up_side_texture,
        "right":chest_up_side_texture,
        "back": chest_up_side_texture,
        "bottom": black_texture
    }
    torch_textures = {
        "left": torch_texture,
        "right": torch_texture,
        "back": torch_texture,
        "front": torch_texture
    }
    
    

    # .OBJ MODELS 
    bed = Wavefront("./objects/bed/Bed.obj")
    sword = Wavefront("./objects/sword/espada minecraft.obj")
    anvil = Wavefront("./objects/anvil/Mineways2Skfb.obj")
    """""""""""""""""""""""""""""""""""""""""""""""""""""
    -----------------------CAMERA------------------------
    """""""""""""""""""""""""""""""""""""""""""""""""""""
    cameras = [
        {
            "position": (0,0,-25),
            "angle": (0,0,0),
        },
        {
            "position": (8,0,-10),
            "angle":(0,30,0)
        },
        {
            "position": (7,-0.5,0),
            "angle": (0,90,0),
        },
        {
            "position": (-7,-0.5,0),
            "angle":(0,-90,0)
        },
        {
            "position": (-8,0,-10),
            "angle":(0,-30,0)
        },
        {
            "position": (-4,-1,-2),
            "angle": (20,0,0)
        },
        {
            "position": (0,0,4),
            "angle":(20,180,0)
        },
        {
            "position": (0,0,0),
            "angle":(0,0,0)
        },
        {
            "position": (-3,-0.5,-3),
            "angle":(30,90,0)
        }
    ]
    current_camera = 0
    camera = Camera(cameras[0]["position"], cameras[0]["angle"])

    """""""""""""""""""""""""""""""""""""""""""""""""""""
    -----------------------LIGHTS------------------------
    """""""""""""""""""""""""""""""""""""""""""""""""""""
    light_camera = Light(GL_LIGHT0, [0,0,20,1],ambient,diffuse,specular,0,0.1,0.01,)
    light_bookshelf_left = Light(GL_LIGHT1, [-7,1, 0 , 1], ambient, diffuse, specular, 0.2, 0.05, 0.01)
    light_bookshelf_right = Light(GL_LIGHT2, [7,1, 0 , 1], ambient, diffuse, specular,0.2,0.05,0.01)

    room = Cube(
        [0,0,0],
        room_size,
        visible_faces=["left","right","back","bottom","top"],
        textures=room_textures,
        texture_coords=room_texture_coords
        )
    creeper_painting = Cube(
        [8,0,-1],
        [0.1,1,2],
        textures= {"left": load_texture("./textures/creeper_painting.png")},
        texture_coords={"left": [(0,0),(0,1),(1,1),(1,0)]}
    )
    skull_painting = Cube(
        [0,0,-5],
        [2,2,0.1],
        textures = {"front": load_texture("./textures/skull_painting.png")}
    )
    bookshelf_left = Cube(
        [-7,-2,-1],
        size=[1,1,4],
        textures = bookshelf_textures,
        texture_coords=bookshelf_left_coords
    )
    bookshelf_left_2 = Cube(
        [-5,-2,-4],
        size = [1,1,1],
        textures=bookshelf_textures
    )
    bookshelf_right = Cube(
        [+7,-2,-1],
        size=[1,1,2],
        textures = bookshelf_textures,
        texture_coords=bookshelf_right_coords
    )
    bookshelf_front = Cube(
        [0,-2,4],
        size = [2,1,1],
        textures= bookshelf_textures,
        texture_coords = bookshelf_front_coords
    )
    chest_low = Cube(
        [4,-2,-3],
        [1,0.75,1],
        textures=chest_low_textures,
    )
    chest_up = Cube(
        [4,-1,-3],
        [1,0.25,1],
        textures = chest_up_textures
    )
    torch_left = Cube(
        [-7,-0.5,2],
        [0.1,0.6,0.1],
        textures=torch_textures
    )
    torch_right = Cube(
        [7,-0.5,0.0],
        [0.1,0.6,0.1],
        textures=torch_textures
    )


"""""""""""""""""""""""""""""""""""""""""""""""""""""
-------------------EVENT HANDLERS--------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""
chest_open = False
def handle_events():
    global current_camera, chest_open
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            print(event.type)
            if event.key == pygame.K_SPACE:
                current_camera = (current_camera + 1) % len(cameras)
                camera.update_position(cameras[current_camera]["position"])
                camera.update_angle(cameras[current_camera]["angle"])

            elif event.key == pygame.K_1:
                lights_on[0] = 0 if lights_on[0] else 1
                if lights_on[0] == 0: light_camera.turn_off()
            elif event.key == pygame.K_2:
                lights_on[1] = 0 if lights_on[1] else 1
                if lights_on[1] == 0: light_bookshelf_left.turn_off()
            elif event.key == pygame.K_3:
                lights_on[2] = 0 if lights_on[2] else 1
                if lights_on[2] == 0: light_bookshelf_right.turn_off()
            elif event.key == pygame.K_o:
                chest_open = False if chest_open else True

def pressed_key_event_handlers(keys):
    if keys[pygame.K_w]:
        camera.update_position([camera.position[0],camera.position[1],camera.position[2] + 0.5])
        print('key left')
    elif keys[pygame.K_a]:
        camera.update_position([camera.position[0]+0.5,camera.position[1],camera.position[2]])
        print('key right')
    elif keys[pygame.K_s]:
        camera.update_position([camera.position[0],camera.position[1],camera.position[2] - 0.5])
        print('key up')
    elif keys[pygame.K_d]:
        camera.update_position([camera.position[0]-0.5,camera.position[1],camera.position[2]])
        print('key down')
    elif keys[pygame.K_RIGHT]:
        camera.update_angle([camera.angle[0],camera.angle[1]+1,camera.angle[2]])
    elif keys[pygame.K_LEFT]:
        camera.update_angle([camera.angle[0],camera.angle[1]-1,camera.angle[2]])
    elif keys[pygame.K_UP]:
        camera.update_angle([camera.angle[0]-1,camera.angle[1],camera.angle[2]])
    elif keys[pygame.K_DOWN]:
        camera.update_angle([camera.angle[0]+1,camera.angle[1],camera.angle[2]])

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL, RESIZABLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    load_all_objects()

    sword_angle = 0
    chest_angle = 0
    
    while True:
        handle_events()
        keys = pygame.key.get_pressed()
        pressed_key_event_handlers(keys)

        sword_angle+=1
        chest_angle += 1
        if sword_angle == 360: sword_angle = 0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.set()

        if lights_on[0]: light_camera.turn_on()
        if lights_on[1]: light_bookshelf_left.turn_on()
        if lights_on[2]: light_bookshelf_right.turn_on()

        room.draw()
        bookshelf_left.draw()
        bookshelf_left_2.draw()
        bookshelf_right.draw()
        bookshelf_front.draw()
        creeper_painting.draw()
        skull_painting.draw()
        torch_left.draw()
        torch_right.draw()
        chest_low.draw()
        if chest_open:
            if chest_up.orbit_angle > -90:
                chest_up.orbit(-1,1,0,0,0,0,-1)
        else:
            if chest_up.orbit_angle < 0:
                chest_up.orbit(1,0,0,0,0,0,-1)

        chest_up.draw()

        glPushMatrix()
        glTranslatef(0,-3,0)
        #glScalef(0.5,0.5,0.5)
        visualization.draw(bed)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(7,-0.5,3)
        glRotatef(sword_angle,0,1,0)
        glScalef(5,5,5)
        visualization.draw(sword)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(6,-3,4)
        glRotatef(90,0,1,0)
        glScalef(4,4,4)
        visualization.draw(anvil)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()