- rectangle
    - vertical lights
    - horizontal lights
- circle
    - vertical lights
    - horizontal lights
- rectangle, circle top
    - vertical lights
    - horizontal lights
- square
    - 5 lights (dice face)

- blank light holes

Variables
- Background style
- Background thickness
- Background border top
- Background border bottom
- Background border sides
- Colour/Variables

- Number of lights
- Colour/Existance/ON OFF or each light
- Light can depth
- Spacing between cans
- Light can radius
- Light can wall thickness



import bpy
import numpy as np

# Origin in center back of bottom light

# Default RGBa Values
R = 0.5
G = 0.5
B = 0.5
A = 1

# R1, G1, B1, A1
# R2, G2, B2, A2
lights = np.array([[0, 1, 0, 1],
                   [1, 1, 0, 1],
                   [1, 0, 0, 1]])

# diffuse.inputs[0]
# reflection_mix.inputs[1]
# reflection_mix.inputs[2]
# glossy.inputs['Color']
sign_values = np.array([[0.1, 0.1, 0.1, 1],
                        [0.06, 0.06, 0.06, 1],
                        [0.1, 0.1, 0.1, 1],
                        [0.2, 0.2, 0.2, 1]])


style = "square" # square or oval sign top

light_radius = 0.1    # Radius of outside of can
background_offset_w = 0.05  # Distance of sign on sides from can
background_offset_t = 0.05  # Distance of sign on top from can
background_offset_b = 0.05  # Distance of sign on bottom from can
background_thickness = 0.01 # Thickness of sign

light_spacing = 0.01    # Spacing between light cans
light_wall_thickness = 0.005    # Wall thickness of can
light_depth = 0.05    # Depth of light can

object_number = 0    #Ranom Variable (Number of objects)




# Draw sign background
def Draw_square(light_radius, 
                background_thickness,
                background_offset_w,
                background_offset_t,
                background_offset_b,
                no_lights,
                object_number):


    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * background_offset_w
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + background_offset_t + background_offset_b
    
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (background_offset_b + light_radius)

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(width / 2, background_thickness, height / 2)

    obj.location=(0, -background_thickness, vertical_origin)

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    mat = bpy.data.materials['Sign_Material']
    obj.data.materials.append(mat)




# Draw sign oval background
def Draw_oval(light_radius, 
              background_thickness,
              background_offset_w,
              background_offset_t,
              background_offset_b,
              no_lights,
              object_number):

    # Calculate width and height of sign background and height of circular top
    width = 2 * light_radius + 2 * background_offset_w
    height = (background_offset_b + light_radius) + (((no_lights - 1) * light_radius * 2) + ((no_lights - 1) * light_spacing))
    height_circle = (light_radius * 2) + (background_offset_t * 2)

    # Calculate vertical position for background and top
    vertical_origin = (height / 2) - (background_offset_b + light_radius)
    vertical_origin_circle = ((no_lights - 1) * ((2 * light_radius) + (light_spacing)))

    # Create sign background square
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj1 = bpy.data.objects[object_name[-1]]

    obj1.scale=(width / 2, background_thickness, height / 2)
    obj1.location=(0, -background_thickness, vertical_origin)

    # Create sign background circle
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj2 = bpy.data.objects[object_name[-1]]
    
    obj2.rotation_euler.x = -1.57
    obj2.scale=(width / 2, height_circle / 2, background_thickness)
    obj2.location=(0, -background_thickness, vertical_origin_circle)


    # Combine square and circle
    mod_bool = obj1.modifiers.new('my_bool_mod_2', 'BOOLEAN')
    mod_bool.operation = 'UNION'
    mod_bool.object = obj2
    bpy.context.scene.objects.active = obj1
    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod_2')

    # Add material to sign
    obj1.pass_index = 1
    mat = bpy.data.materials['Sign_Material']
    obj1.data.materials.append(mat)

    obj2.pass_index = 1
    mat = bpy.data.materials['Sign_Material']
    obj2.data.materials.append(mat)

    # obj2.select = True
    # bpy.ops.object.delete()
    # object_name.remove(object_name[object_number])
    # object_number = object_number - 1   



# Draw light can
def Draw_light(no_lights,
               object_number,
               light_radius,
               light_spacing,
               light_wall_thickness,
               light_depth):    # Create mesh shape
    # Subtract inside cylinder from outside cylinder
    objects = bpy.data.objects

    # For each light create the cylinder and position it
    for x_lights in range(0, lights.shape[0]):

        # Stack Lights on top of each other
        center = (x_lights) * ((2 * light_radius) + light_spacing)

        # Draw outside cylinder
        object_number = object_number + 1
        bpy.ops.mesh.primitive_cylinder_add(location=(0, light_depth, center))

        object_name.append(bpy.context.active_object.name)
        obj1 = objects[object_name[-1]]

        obj1.scale=(light_radius, light_radius, light_depth)
        obj1.rotation_euler.x = -1.57

        # Draw inside cylinder
        object_number = object_number + 1
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, center))

        object_name.append(bpy.context.active_object.name)
        obj2 = objects[object_name[-1]]

        obj2.scale=(light_radius - light_wall_thickness, light_radius - light_wall_thickness, 5)
        obj2.rotation_euler.x = -1.57

        # Subtract cylinders
        mod_bool = obj1.modifiers.new('my_bool_mod', 'BOOLEAN')
        mod_bool.operation = 'DIFFERENCE'
        mod_bool.object = obj2  

        bpy.context.scene.objects.active = obj1
        res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod')
        
        # Delete unused object
        obj2.select = True
        bpy.ops.object.delete()
        object_name.remove(object_name[object_number])
        object_number = object_number - 1

        # Cut front of light to curve
        Crop_light_front(no_lights,
                         object_number,
                         light_radius,
                         light_spacing,
                         light_wall_thickness,
                         light_depth,
                         x_lights)

        # Add material to light can
        obj1.pass_index = 1
        mat = bpy.data.materials['Sign_Material']
        obj1.data.materials.append(mat)

    return





# Cut front of light off to curved shape
def Crop_light_front(no_lights,
                     object_number,
                     light_radius,
                     light_spacing,
                     light_wall_thickness,
                     light_depth,
                     x_lights):

    objects = bpy.data.objects

    # Stack Lights on top of each other
    center = (x_lights) * ((2 * light_radius) + light_spacing) + light_radius

    # Draw outside cylinder
    obj1 = objects[object_name[-1]]


    # Create face cropper cylinder
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 2 * light_depth - light_radius, center))

    object_name.append(bpy.context.active_object.name)
    obj2 = objects[object_name[-1]]

    obj2.scale=(light_radius, light_radius, light_radius)
    obj2.rotation_euler.y = -1.57


    # Create face cropper cube
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location=(0, light_depth - light_radius, center))

    object_name.append(bpy.context.active_object.name)
    obj3 = objects[object_name[-1]]

    obj3.scale=(light_radius, light_depth, light_radius)
    
    # Combine cube and cylinder for intercecting
    mod_bool = obj3.modifiers.new('my_bool_mod_2', 'BOOLEAN')
    mod_bool.operation = 'UNION'
    mod_bool.object = obj2
    bpy.context.scene.objects.active = obj3
    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod_2')


    # Create difference cube
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location=(0, 2* light_radius + 4 * light_wall_thickness, center - 2 * light_radius))

    object_name.append(bpy.context.active_object.name)
    obj4 = objects[object_name[-1]]

    obj4.scale=(2 * light_radius, 2 * light_radius, 2 * light_radius)
    
    # Subtract intersecting object from difference object
    mod_bool = obj4.modifiers.new('my_bool_mod_3', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = obj3 

    bpy.context.scene.objects.active = obj4
    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod_3')

    # Subtract differencce object from light can
    mod_bool = obj1.modifiers.new('my_bool_mod_4', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = obj4

    bpy.context.scene.objects.active = obj1
    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod_4')
    

    #Delete unused components
    obj4.select = True
    bpy.ops.object.delete()
    object_name.remove(object_name[object_number])
    object_number = object_number - 1     

    obj3.select = True
    bpy.ops.object.delete()
    object_name.remove(object_name[object_number])
    object_number = object_number - 1     

    obj2.select = True
    bpy.ops.object.delete()
    object_name.remove(object_name[object_number])
    object_number = object_number - 1     

    return



# Draw light lens
def Draw_lens(no_lights,
              object_number,
              light_radius,
              light_spacing,
              light_wall_thickness,
              light_depth):

    objects = bpy.data.objects

    for x_lights in range(0, lights.shape[0]):

        color_selection = ('_' + str(lights[x_lights][0])
                         + '_' + str(lights[x_lights][1])
                         + '_' + str(lights[x_lights][2]))

        center = (x_lights) * ((2 * light_radius) + light_spacing)

        object_number = object_number + 1
        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, center))

        object_name.append(bpy.context.active_object.name)
        obj1 = objects[object_name[-1]]

        obj1.rotation_euler.x = -1.57
        obj1.scale=(light_radius - light_wall_thickness, light_radius - light_wall_thickness, 0.02)


        # Draw inside cylinder
        object_number = object_number + 1
        bpy.ops.mesh.primitive_cube_add(location=(0, -light_radius, center))

        object_name.append(bpy.context.active_object.name)
        obj2 = objects[object_name[-1]]

        obj2.scale=(light_radius, light_radius, light_radius)


        mod_bool = obj1.modifiers.new('my_bool_mod', 'BOOLEAN')
        mod_bool.operation = 'DIFFERENCE'
        mod_bool.object = obj2  

        bpy.context.scene.objects.active = obj1
        res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod')
         
        obj2.select = True
        bpy.ops.object.delete()
        object_name.remove(object_name[object_number])
        object_number = object_number - 1
        

        obj1.pass_index = 1
        mat = bpy.data.materials['Lens_Material' + color_selection]
        
        obj1.data.materials.append(mat)

    return

def create_lens_material(R, G, B, Alpha):

    mat = bpy.data.materials.get('Lens_Material_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('Lens_Material_' + str(R) + '_' + str(G) + '_'+ str(B))

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = (R, G, B, Alpha)

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'
    translucent.inputs[0].default_value = (R, G, B, Alpha)

    emission = nodes.new(type='ShaderNodeEmission')
    emission.name = emission.label = 'Emission'
    emission.inputs[0].default_value = (R, G, B, Alpha)

    mix_shader_1 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_1.name = mix_shader_1.label = 'Mix Shader 1'

    node_tree.links.new(diffuse.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(mix_shader_1.outputs['Shader'], mix_shader_2.inputs[1])
    node_tree.links.new(emission.outputs['Emission'], mix_shader_2.inputs[2])
    node_tree.links.new(output.inputs['Surface'], mix_shader_2.outputs['Shader'])


def create_sign_material(sign_values):

    mat = bpy.data.materials.get('Sign_Material')

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('Sign_Material')

    roughness = 0.1

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = (sign_values[0][0], sign_values[0][1], sign_values[0][2], sign_values[0][3])

    roughness_value = nodes.new(type='ShaderNodeValue')
    roughness_value.name = roughness_value.label = 'Roughness'
    roughness_value.outputs[0].default_value = roughness

    reflection_mix = nodes.new(type='ShaderNodeMixRGB')
    reflection_mix.inputs[1].default_value = (sign_values[1][0], sign_values[1][1], sign_values[1][2], sign_values[1][3])
    reflection_mix.inputs[2].default_value = (sign_values[2][0], sign_values[2][1], sign_values[2][2], sign_values[2][3])
    reflection_mix.name = reflection_mix.label = 'Reflectivity'

    glossy = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy.inputs['Color'].default_value = (sign_values[3][0], sign_values[3][1], sign_values[3][2], sign_values[3][3])
    glossy.name = glossy.label = 'Gloss'

    mix = nodes.new(type='ShaderNodeMixShader')
    mix.name = mix.label = 'GlossDiffuseMix'

    # Link our roughness
    node_tree.links.new(roughness_value.outputs[0], glossy.inputs['Roughness'])
    node_tree.links.new(roughness_value.outputs[0], diffuse.inputs['Roughness'])

    node_tree.links.new(reflection_mix.outputs['Color'], mix.inputs['Fac'])
    node_tree.links.new(diffuse.outputs['BSDF'], mix.inputs[1])
    node_tree.links.new(glossy.outputs['BSDF'], mix.inputs[2])
    node_tree.links.new(mix.outputs['Shader'], output.inputs['Surface'])

def Delete_material():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)




#####################################################################################################################
#####################################################################################################################
#                                                   CODE HERE                                                       #
#####################################################################################################################
#####################################################################################################################

# Delete old objects 
for object in bpy.data.objects:
    bpy.data.objects.remove(object)


# # Change to the cycles renderer and setup some options
bpy.context.scene.render.engine = 'CYCLES'
scene = bpy.data.scenes['Scene']
scene.cycles.device = 'CPU'
scene.cycles.samples = 256

# Enable the object pass index so we can make our masks
scene.render.layers['RenderLayer'].use_pass_object_index = True
scene.use_nodes = True

# Set resolution, and render at that resolution
scene.render.resolution_x = 1280
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100

scene = bpy.context.scene

scene.update()

Delete_material()

# Something
object_number = 0
object_name = [0]
objects = bpy.data.objects

# Add plane for background
object_number = object_number + 1

bpy.ops.mesh.primitive_plane_add( location=(0, 0, -1))
bpy.context.object.scale=(5, 5, 1)


object_name.append(bpy.context.active_object.name)
plane_object = objects[object_name[0]]
        

# Create light materials
for i in range(0, lights.shape[0]):
    create_lens_material(lights[i - 1][0], lights[i - 1][1], lights[i - 1][2], lights[i - 1][3])

create_sign_material(sign_values)


Draw_light(lights.shape[0],
           object_number,
           light_radius,
           light_spacing,
           light_wall_thickness,
           light_depth)
           
if style == "square":
    Draw_square(light_radius, 
            background_thickness,
            background_offset_w,
            background_offset_t,
            background_offset_b,
            lights.shape[0],
            object_number)
else:
    Draw_oval(light_radius, 
            background_thickness,
            background_offset_w,
            background_offset_t,
            background_offset_b,
            lights.shape[0],
            object_number)

#Join_body()

Draw_lens(lights.shape[0],
          object_number,
          light_radius,
          light_spacing,
          light_wall_thickness,
          light_depth)

plane_object.select = True
bpy.ops.object.delete()
object_name.remove(object_name[object_number])
object_number = object_number - 1

for x in objects:
    bpy.data.objects[x.name].select = True
bpy.ops.object.join()
