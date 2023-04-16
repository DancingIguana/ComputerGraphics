from OpenGL.GL import *
from OpenGL.GLU import *
class Light:
    def __init__(self, gl_light, light_pos, ambient, diffuse, specular, constant_atten, linear_atten, quad_atten):
        self.gl_light = gl_light
        self.light_pos = light_pos
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.constant_atten = constant_atten
        self.linear_atten = linear_atten
        self.quad_atten = quad_atten
    
    def turn_off(self):
        glDisable(self.gl_light)
    
    def turn_on(self):
        glPushMatrix()
        glEnable(self.gl_light)
        glLightfv(self.gl_light, GL_POSITION, self.light_pos)
        glLightfv(self.gl_light, GL_AMBIENT, self.ambient)
        glLightfv(self.gl_light, GL_DIFFUSE, self.diffuse)
        glLightfv(self.gl_light, GL_SPECULAR, self.specular)
        glLightf(self.gl_light, GL_CONSTANT_ATTENUATION, self.constant_atten)
        glLightf(self.gl_light, GL_LINEAR_ATTENUATION, self.linear_atten)
        glLightf(self.gl_light, GL_QUADRATIC_ATTENUATION, self.quad_atten)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glPopMatrix()