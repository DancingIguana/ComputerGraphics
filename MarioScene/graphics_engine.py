from mesh import Mesh
from material import Material
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr



class GraphicsEngine:

    def __init__(
            self, 
            scene,
            ):
        glClearColor(0.0, 0.0, 0.0, 1)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_FRONT_AND_BACK)     
        glDisable(GL_CULL_FACE)
        glCullFace(GL_FRONT_AND_BACK)


        self.scene = scene

        # Load shaders 
        self.shaders = {}
        for shader in scene.shaders:
            self.shaders[shader["key"]] = {
                "program": self.createShader(
                    shader["vertex"], 
                    shader["fragment"],
                    scene.global_shader_attributes[shader["attributes_key"]]
                ),
                "attributes": shader["attributes_key"],
                
                }

            #self.shaders[shader["key"]]["attributes"]["position"] = glGetAttribLocation(
            #    self.shaders[shader["key"]],
            #    self.shaders[shader["key"]]["attributes"]["name"]
            #)

        #self.shader = self.createShader(
        #    "./shaders/blinn_phong_vertex.txt", 
        #    "./shaders/blinn_phong_fragment.txt"
        #)
        
        #self.position_pointer = glGetAttribLocation(self.shader, "vertexPos")
        #self.texture_pointer = glGetAttribLocation(self.shader, "vertexTexCoord")
        #self.normal_pointer = glGetAttribLocation(self.shader, "vertexNormal")

        # Load Assets
        self.meshes = {}
        for key, mesh_file, shader_attribs_key in scene.meshes:
            self.meshes = Mesh(
                mesh_file, 
                scene.global_shader_attributes[shader_attribs_key]
            )
        
        self.materials = {}
        for key, material_file in scene.textures:
            self.materials[key] = Material(material_file)

        print(self.materials)
        
        # Initialize OpenGL

        glUseProgram(self.shaders["blinn_phong_shader"]["program"])
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
        self.cameraPosLoc = glGetUniformLocation(self.shader, "cameraPostion")
    
    def createShader(self, vertexFilepath, fragmentFilepath, attributes):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        print(attributes)
        for attribute in attributes:
            glBindAttribLocation(shader, attributes[attribute]["index"], attribute)
        glLinkProgram(shader)
        #for attribute in attributes:
        #    print(attribute, glGetAttribLocation(shader, attribute))

        return shader

    def render(self, scene):

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

        for i,light in enumerate(scene.lights):
            glUniform3fv(self.lightLocation["position"][i], 1, light.position)
            glUniform3fv(self.lightLocation["color"][i], 1, light.color)
            glUniform1f(self.lightLocation["strength"][i], light.strength)

        glUniform3fv(self.cameraPosLoc, 1, scene.camera.position)

        # Draw the materials
        for mesh_key, material_key, shader_key, obj in scene.objs:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(obj.eulers), dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(obj.position),dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            self.draw_object(material_key, mesh_key,shader_key)
            glFlush()

    def load_assets(self, assets):
        # Load Assets
        meshes = {}
        materials = {}
        for key, asset_file, asset_type in assets:
            if asset_type == "material": materials[key] = Material(asset_file)
            elif asset_type == "mesh": meshes[key] = Mesh(asset_file)
        
        return meshes, materials
        
        
    def draw_object(self,texture_key,mesh_key,shader_key):
        self.materials[texture_key].use()
        glBindBuffer(GL_ARRAY_BUFFER, self.meshes[mesh_key].vbo)

        for attributes in self.shaders[shader_key]["attributes"]:
            glEnableVertexAttribArray(attributes["position"])
            glVertexAttribPointer(
                attributes["position"],
                attributes["size"],
                attributes["type"],
                attributes["normalize"],
                attributes["stride"],
                attributes["pointer"]
            )
        """
        glEnableVertexAttribArray(self.position_pointer)
        glVertexAttribPointer(self.position_pointer, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(self.texture_pointer)
        glVertexAttribPointer(self.texture_pointer, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        glEnableVertexAttribArray(self.normal_pointer)
        glVertexAttribPointer(self.normal_pointer, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        """
        glDrawArrays(GL_TRIANGLES, 0, self.meshes[mesh_key].vertex_count)


    def set_camera_lights(self, camera, lights, light_location):
        view_transform = pyrr.matrix44.create_look_at(
            eye = camera.position,
            target = camera.position + camera.forwards,
            up = camera.up, dtype = np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        for i,light in enumerate(lights):
            glUniform3fv(light_location["position"][i], 1, light.position)
            glUniform3fv(light_location["color"][i], 1, light.color)
            glUniform1f(light_location["strength"][i], light.strength)

        glUniform3fv(self.cameraPosLoc, 1, camera.position)

    def destroy(self):

        for material_key in self.materials:
            self.materials[material_key].destroy()
        
        for mesh_key in self.meshes:
            self.meshes[mesh_key].destroy()
        glDeleteProgram(self.shader)