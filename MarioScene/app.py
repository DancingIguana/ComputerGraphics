import pygame
from OpenGL.GL import *
import numpy as np
import pyrr
from scene import Scene
from graphics_engine import GraphicsEngine
from OpenGL.GL.shaders import compileProgram,compileShader


class App:
    def __init__(self, window_size = (800,600)):
        # Initialize pygame
        pygame.init()
        pygame.display.set_mode(window_size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.scene = Scene()
        # Initialize OpenGL
        self.renderer = GraphicsEngine(self.scene)
        # Load the scene's attributes
        

        self.main_loop()
    

    def handle_keys(self):
        return 
    
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # Update scene
            self.handle_keys()
            self.scene.update()

            self.renderer.render(self.scene)

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