import pygame
from OpenGL.GL import *
import numpy as np
import pyrr
from scene import Scene
from graphics_engine import GraphicsEngine
from OpenGL.GL.shaders import compileProgram,compileShader
from mario import Mario
from obj import Obj

class App:
    def __init__(self, window_size = (800,800)):
        # Initialize pygame
        pygame.init()
        pygame.display.set_mode(window_size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.scene = Scene()
        # Initialize OpenGL
        self.renderer = GraphicsEngine(self.scene)
        self.mario = Mario([5,6,-1], self.renderer.shader_indexes)
        # Load the scene's attributes
        self.is_walking = True
        self.is_transforming = False
        self.walk_time = 0
        self.music = pygame.mixer.Sound("./sounds/music.mp3")
        self.music.play(-1)
        self.damage_sound = pygame.mixer.Sound("./sounds/damage.mp3")
        self.grow_sound = pygame.mixer.Sound("./sounds/grow.mp3")
        self.main_loop()
    

    def handle_pressed_keys(self, keys):
        if keys[pygame.K_d]:
            self.mario.right()
            self.walk_time += 1
            print()
        elif keys[pygame.K_a]:
            self.mario.left()
            self.walk_time += 1
        else:
            self.walk_time = 0
        return 
    
    def handle_events(self,running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.scene.lights[0].strength == 0: self.scene.lights[0].strength = 5
                    else: self.scene.lights[0].strength = 0
                elif event.key == pygame.K_2:
                    if self.scene.lights[1].strength == 0: self.scene.lights[1].strength = 100
                    else: self.scene.lights[1].strength = 0
                elif event.key == pygame.K_3:
                    if self.scene.lights[2].strength == 0: self.scene.lights[2].strength = 100
                    else: self.scene.lights[2].strength = 0
                elif event.key == pygame.K_SPACE:
                    if self.scene.camera_mode == "follow": self.scene.camera_mode = "fixed"
                    else: self.scene.camera_mode = "follow"
                elif event.key == pygame.K_t:
                    self.is_transforming = True
                    if self.mario.is_small: self.mario.is_small = False
                    else: self.mario.is_small = True
        return running

        

    def main_loop(self):
        running = True
        cooldown = 0
        i = 0
        while running:
            # Update scene
            running = self.handle_events(running)
            keys = pygame.key.get_pressed()
            self.handle_pressed_keys(keys)
            self.scene.update(self.mario)
            #print(self.walk_time)
            if self.walk_time > 0:
                if (self.walk_time - 1) % 5 == 0:
                    self.mario.current_texture = self.mario.sprites[
                        self.mario.animations["walking"][
                            i%len(self.mario.animations["walking"])
                        ]
                    ]["material"]
                    i += 1
            else:
                self.mario.current_texture = self.mario.sprites["idle"]["material"]
                i = 0
            

            # If mario touches the goomba
            if abs(self.scene.objs[-1][2].position[1] - self.mario.obj.position[1]) < 0.1 and cooldown == 0 and not self.mario.is_small: 
                self.is_transforming = True
                self.mario.is_small = True
                cooldown = 60
                self.damage_sound.play()
                
            
            # If mario touces the mushroom
            if abs(self.scene.objs[-2][2].position[1] - self.mario.obj.position[1]) < 0.1 and cooldown == 0 and self.mario.is_small: 
                self.is_transforming = True
                self.mario.is_small = False
                cooldown = 60
                self.grow_sound.play()

            if self.is_transforming and self.mario.transformation_frame < 100:
                self.mario.transformation_frame += 1
            else:
                if self.mario.is_small: self.mario.transformation_frame = 0
                else: self.mario.transformation_frame = 10
                self.is_transforming = False


            if cooldown > 0: cooldown -= 1
            self.renderer.render(self.scene,self.mario)

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()
    

    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,"r") as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,"r") as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader

    def quit(self):
        self.renderer.destroy()
        pygame.quit()


if __name__ == "__main__":
    App()