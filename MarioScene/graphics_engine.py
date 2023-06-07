from mesh import Mesh
from material import Material
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
from mario import Mario


class GraphicsEngine:

    def __init__(
            self, 
            scene
            ):
        glClearColor(0.0, 0.0, 0.0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_FRONT_AND_BACK)     
        glDisable(GL_CULL_FACE)
        glCullFace(GL_FRONT_AND_BACK)
    

        self.scene = scene

        self.shader = self.createShader("./shaders/blinn_phong_vertex.txt", "./shaders/toon_fragment.txt")

        self.shader_indexes = {
            "vertexPos": glGetAttribLocation(self.shader, "vertexPos"),
            "vertexTexCoord": glGetAttribLocation(self.shader, "vertexTexCoord"),
            "vertexNormal": glGetAttribLocation(self.shader, "vertexNormal")
        }

        # Load Assets
        self.meshes = {}
        self.materials = {}
        for key, asset_file, asset_type in scene.assets:
            if asset_type == "material": self.materials[key] = Material(asset_file)
            elif asset_type == "mesh": self.meshes[key] = Mesh(asset_file, self.shader_indexes)

        #self.mario = Mario([5,5,-1.])

        print(self.materials)
        # Initialize OpenGL
        
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 50, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, "view")

        self.lightLocation = {
            "position": [
                glGetUniformLocation(self.shader, f"Lights[{i}].position")
                for i in range(8)
            ],
            "color": [
                glGetUniformLocation(self.shader, f"Lights[{i}].color")
                for i in range(8)
            ],
            "strength": [
                glGetUniformLocation(self.shader, f"Lights[{i}].strength")
                for i in range(8)
            ]
        }

        self.timeLocation = glGetUniformLocation(self.shader, "time")
        self.transitionFramesLocation = glGetUniformLocation(self.shader, "transitionFrames")
        self.initialSizeLocation = glGetUniformLocation(self.shader, "initialSize")
        self.finalSizeLocation = glGetUniformLocation(self.shader, "finalSize")

        self.cameraPosLoc = glGetUniformLocation(self.shader, "cameraPostion")


        
    
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader

    def render(self, scene, mario):

        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        # Setup camera and lights
        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.camera.position,
            target = scene.camera.position + scene.camera.forwards,
            up = scene.camera.up, dtype = np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        active_lights = [light for light in scene.lights if light.on]
        for i,light in enumerate(active_lights):
            glUniform3fv(self.lightLocation["position"][i], 1, light.position)
            glUniform3fv(self.lightLocation["color"][i], 1, light.color)
            glUniform1f(self.lightLocation["strength"][i], light.strength)

        glUniform3fv(self.cameraPosLoc, 1, scene.camera.position)

        # Draw the materials
        for mesh_key, material_key, obj in scene.objs:
            self.draw_object(obj, self.materials[material_key], self.meshes[mesh_key])
            glFlush()
        # Draw mario
        self.draw_object(
            mario.obj, 
            mario.current_texture, 
            mario.mesh, 
            mario.transformation_frame, 
            initialSize=1, 
            finalSize=1.5
        )
        glFlush()
        
        
    def draw_object(
            self,
            obj,
            material,
            mesh,
            time = 0, 
            animationDuration = 10,
            initialSize = 1,
            finalSize = 1):

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        # Apply scale transformation
        scale_matrix = pyrr.matrix44.create_from_scale(obj.scale)
        model_transform = pyrr.matrix44.multiply(model_transform, scale_matrix)

        # Apply rotation transformation
        rotation_matrix = pyrr.matrix44.create_from_eulers(np.radians(obj.eulers), dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(model_transform, rotation_matrix)

        # Apply translation transformation
        translation_matrix = pyrr.matrix44.create_from_translation(np.array(obj.position), dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(model_transform, translation_matrix)

        glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)


        #time = 9
        #animationDuration = 10
        #initialSize = 1
        #finalSize = 2

        glUniform1i(self.timeLocation, time)
        glUniform1i(self.transitionFramesLocation, animationDuration)
        glUniform1f(self.initialSizeLocation, initialSize)
        glUniform1f(self.finalSizeLocation, finalSize)

        material.use()
        glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo)
        glEnableVertexAttribArray(self.shader_indexes["vertexPos"])
        glVertexAttribPointer(self.shader_indexes["vertexPos"], 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        glEnableVertexAttribArray(self.shader_indexes["vertexTexCoord"])
        glVertexAttribPointer(self.shader_indexes["vertexTexCoord"], 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        glEnableVertexAttribArray(self.shader_indexes["vertexNormal"])
        glVertexAttribPointer(self.shader_indexes["vertexNormal"], 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)

    def destroy(self):

        for material_key in self.materials:
            self.materials[material_key].destroy()
        
        for mesh_key in self.meshes:
            self.meshes[mesh_key].destroy()
        glDeleteProgram(self.shader)