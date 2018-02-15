import bpy
import numpy as np
# from .configuration import configuration

# config_dir = configuration()

def configuration():

    config = {
        'background': {
            'style' : 'reccir', # rectangle, circle, reccir, cirtri, square
            'orientation' : 'horizontal', #Vertical/Horizontal
            'border_size' : 0.05,
            'thickness' : 0.01,
            'colour' : {
                'diffuse' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'reflection1' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'reflection2' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'glossy' : [0.06, 0.06, 0.06] # [R, G, B]    # Fixed?
                }
        },
        'lights' : {
            'number_total' : 5,
            'light' : ([[1, 0, 0, 'blank'],
                         [1, 0, 0, 'on'],
                         [1, 0, 0, 'on'],
                         [0, 1, 0, 'off'],
                         [0, 1, 0, 'off'],
                         [1, 0, 0, 'blank']]),
            'light_can_depth' : 0.05,
            'spacing_between_cans' : 0.01,
            'light_can_radius' : 0.1,
            'light_can_wall_thickness' : 0.01,
            'can_hood_length' :0.05
        }
    }
    return config

config_dir = configuration()

# TODO read in config file

sign_values = np.array([[config_dir['background']['colour']['diffuse'][0], config_dir['background']['colour']['diffuse'][1], config_dir['background']['colour']['diffuse'][2], 1],
                        [config_dir['background']['colour']['reflection1'][0], config_dir['background']['colour']['reflection1'][1], config_dir['background']['colour']['reflection1'][2], 1],
                        [config_dir['background']['colour']['reflection2'][0], config_dir['background']['colour']['reflection2'][1], config_dir['background']['colour']['reflection2'][2], 1],
                        [config_dir['background']['colour']['glossy'][0], config_dir['background']['colour']['glossy'][1], config_dir['background']['colour']['glossy'][2], 1]])

style = config_dir['background']['style']
orientation = config_dir['background']['orientation']
border_size = config_dir['background']['border_size']
thickness = config_dir['background']['thickness']

light_values = np.array([[config_dir['lights']['light'][0][0], config_dir['lights']['light'][0][1], config_dir['lights']['light'][0][2], 1],
                         [config_dir['lights']['light'][1][0], config_dir['lights']['light'][1][1], config_dir['lights']['light'][1][2], 1],
                         [config_dir['lights']['light'][2][0], config_dir['lights']['light'][2][1], config_dir['lights']['light'][2][2], 1],
                         [config_dir['lights']['light'][3][0], config_dir['lights']['light'][3][1], config_dir['lights']['light'][3][2], 1],
                         [config_dir['lights']['light'][4][0], config_dir['lights']['light'][4][1], config_dir['lights']['light'][4][2], 1]])

light_can_depth = config_dir['lights']['light_can_depth']
spacing_between_cans =         config_dir['lights']['spacing_between_cans']
light_can_radius =         config_dir['lights']['light_can_radius']
light_can_wall_thickness =         config_dir['lights']['light_can_wall_thickness']
can_hood_length =         config_dir['lights']['can_hood_length']

if style == 'rectangle':
    number_total = config_dir['lights']['number_total']

elif style == 'reccir':
    number_total = config_dir['lights']['number_total']

elif style == 'circle':
    number_total = config_dir['lights']['number_total']
    if number_total > 3:
        number_total = 3

elif style == 'cirtri':
    number_total = config_dir['lights']['number_total']
    if number_total > 3:
        number_total = 3

elif style == 'square':
    number_total = config_dir['lights']['number_total']
    if number_total > 5:
        number_total = 5

else:
    print('Style Unknown')
    number_total = config_dir['lights']['number_total']

object_number = 0    #Ranom Variable (Number of objects)
object_name = [0]



def delete_materials():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

def draw_background_rec(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation):

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size

    if orientation == 'horizontal':
        temp = width
        width = height
        height = temp
        print('Orientation Horizontal')

    else:
        print('Orientation Vertical')
    
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

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
    mat = bpy.data.materials['sign_material']
    obj.data.materials.append(mat)

    return obj

def draw_background_cir(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation):

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size
    
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        vertical_origin = 0

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(height / 2, height / 2, background_thickness)

    obj.rotation_euler.x = -1.57

    obj.location=(0, -background_thickness, vertical_origin)

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    mat = bpy.data.materials['sign_material']
    obj.data.materials.append(mat)

    return obj

def draw_background_cirtri(light_radius, 
                           background_thickness,
                           border_size,
                           no_lights,
                           object_number,
                           light_spacing,
                           orientation):

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size
    
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        vertical_origin = 0

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(height / 2, height / 2, background_thickness)

    obj.rotation_euler.x = -1.57

    obj.location=(0, -background_thickness, vertical_origin)

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    mat = bpy.data.materials['sign_material']
    obj.data.materials.append(mat)

    return obj  

def draw_background_reccir(light_radius, 
                           background_thickness,
                           border_size,
                           no_lights,
                           object_number,
                           light_spacing,
                           orientation):

     # Calculate width and height of sign background and height of circular top
    width = 2 * light_radius + 2 * border_size
    height = (border_size + light_radius) + (((no_lights - 1) * light_radius * 2) + ((no_lights - 1) * light_spacing))
    height_circle = (light_radius * 2) + (border_size * 2)

    # Calculate vertical position for background and top
    vertical_origin = (height / 2) - (border_size + light_radius)
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

    # TODO should be deleting this object and combining properly
    # obj2.select = True
    # bpy.ops.object.delete()
    # object_name.remove(object_name[object_number])
    # object_number = object_number - 1  
    obj2.pass_index = 1
    mat = bpy.data.materials['sign_material']
    obj2.data.materials.append(mat)



    # Add material to sign
    obj1.pass_index = 1
    mat = bpy.data.materials['sign_material']
    obj1.data.materials.append(mat)


    return obj1

def draw_background_squ(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation):
    # TODO this..

    print('Not Finished')

    return obj

def draw_can(object_number,
             light_radius,
             light_spacing,
             light_wall_thickness,
             light_depth):

    # Subtract inside cylinder from outside cylinder
    objects = bpy.data.objects

    # Draw outside cylinder
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj_can_orig = objects[object_name[-1]]
    can_obj = objects[object_name[-1]]

    obj_can_orig.scale=(light_radius, light_radius, light_depth)
    obj_can_orig.rotation_euler.x = -1.57

    # Draw inside cylinder
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj2 = objects[object_name[-1]]

    obj2.scale=(light_radius - light_wall_thickness, light_radius - light_wall_thickness, 5)
    obj2.rotation_euler.x = -1.57

    # Subtract cylinders
    mod_bool = obj_can_orig.modifiers.new('my_bool_mod', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = obj2  

    bpy.context.scene.objects.active = obj_can_orig
    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod')
    
    # Delete unused object
    obj2.select = True
    bpy.ops.object.delete()
    object_name.remove(object_name[object_number])
    object_number = object_number - 1

    obj_can_orig.location=(0, light_depth, 0)

    # Cut front of light to curve
    crop_can_front(obj_can_orig,
                             object_number,
                             light_radius,
                             light_wall_thickness,
                             light_depth,
                             light_spacing
                             )


    return obj_can_orig

def crop_can_front(obj,
                   object_number,
                   light_radius,
                   light_wall_thickness,
                   light_depth,
                   light_spacing
                   ):

    objects = bpy.data.objects

    # Stack Lights on top of each other
    center = light_radius #(x_light) * ((2 * light_radius) + light_spacing) + light_radius

    # Draw outside cylinder
    obj1 = obj

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


    
    return obj1


def draw_light(object_number,
               light_radius,
               light_spacing,
               light_wall_thickness,
               light_depth):

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]

    obj1.rotation_euler.x = -1.57
    obj1.scale=(light_radius - light_wall_thickness, light_radius - light_wall_thickness, 0.02)


    # Draw inside cylinder
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location=(0, -light_radius, 0))

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

    return obj1

def draw_blank(object_number,
               light_radius,
               light_spacing,
               light_wall_thickness,
               light_depth):

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]
    
    obj1.scale=(light_radius - light_wall_thickness, light_radius - light_wall_thickness, light_wall_thickness)

    obj1.rotation_euler.x = -1.57
    
    obj1.location=(0, light_wall_thickness, 0)

    return obj1

def move_can(style,
             light_can_radius,
             spacing_between_cans,
             number_total,
             orientation,
             x_lights,
             light_depth,
             light_can_wall_thickness,
             obj):
    # Orientation flips y and z location values
    # Independent of can type
    # 

    if style == 'reccir':
        center = (x_lights) * ((2 * light_can_radius) + spacing_between_cans)
        obj.location=(0, obj.location[1], center)

    elif style == 'square':

        # TODO some sort of X configuration
        vertical_offset = sqrt(2 * (((2 * light_can_radius) + spacing_between_cans)^2))
        horizontal_offset = vertical_offset

        if x_lights == 1: 

            center_x = 0
            center_y = 0

        elif x_lights == 2:

            center_x = -horizontal_offset
            center_y = -vertical_offset

        elif x_lights == 3:

            center_x = horizontal_offset
            center_y = -vertical_offset

        elif x_lights == 4:

            center_x = -horizontal_offset
            center_y = vertical_offset

        elif x_lights == 5:

            center_x = horizontal_offset
            center_y = vertical_offset

        else:
            print('Too many lights')

        obj.location=(center_x, 0, center_y)

    else:
        center = (x_lights) * ((2 * light_can_radius) + spacing_between_cans)
        if orientation == 'vertical':
            obj.location=(0, obj.location[1], center)

        elif orientation == 'horizontal':
            if number_total % 2 == 0:
                # TODO
                #center = +- spacing_between_cans + light_can_radius

                if x_lights > 1:
                    #center = center + ((2 * light_can_radius) + spacing_between_cans)
                    center = center
                else:
                    print('do nothing')
                    center = center

            else:
                center = (x_lights - ((x_lights - 1) / 2)) * ((2 * light_can_radius) + spacing_between_cans)

            obj.location=(x_light, light_can_wall_thickness, 0)

        else:
            print('Orientation Unknown')

    return obj


def light_material(R, G, B):

    Alpha = 1

    mat = bpy.data.materials.get('light_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    # diffuse = nodes['Diffuse BSDF']
    # diffuse.name = diffuse.label = 'Diffuse'
    # diffuse.inputs[0].default_value = (R, G, B, Alpha)

    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
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


def light_off_material(R, G, B):

    # TODO set emission value lower

    Alpha = 1

    mat = bpy.data.materials.get('light_off_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_off_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = (R, G, B, Alpha)

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'
    translucent.inputs[0].default_value = (R, G, B, Alpha)

    emission = nodes.new(type='ShaderNodeEmission')
    emission.name = emission.label = 'Emission'
    emission.inputs[0].default_value = (R, G, B, Alpha)
    emission.inputs[1].default_value = 0

    mix_shader_1 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_1.name = mix_shader_1.label = 'Mix Shader 1'

    node_tree.links.new(diffuse.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(mix_shader_1.outputs['Shader'], mix_shader_2.inputs[1])
    node_tree.links.new(emission.outputs['Emission'], mix_shader_2.inputs[2])
    node_tree.links.new(output.inputs['Surface'], mix_shader_2.outputs['Shader'])


def sign_material(sign_values):

    mat = bpy.data.materials.get('sign_material')

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('sign_material')

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

#####################################################################################################################
#####################################################################################################################
#                                                ACTUAL  CODE HERE                                                  #
#####################################################################################################################
#####################################################################################################################


delete_materials()

for i in range(0, light_values.shape[0]):

    if config_dir['lights']['light'][i][3] == 'on':
        light_material(light_values[i][0], 
                       light_values[i][1], 
                       light_values[i][2],
                       )

    elif config_dir['lights']['light'][i][3] == 'off':
        light_off_material(light_values[i][0], 
                           light_values[i][1], 
                           light_values[i][2],
                           )

    else:
        i = i
        #print('blank light')

sign_material(sign_values)

center = (number_total) * ((2 * light_can_radius) + spacing_between_cans)

objects = bpy.data.objects






blank_obj_orig = draw_blank(object_number,
                       light_can_radius,
                       spacing_between_cans,
                       light_can_wall_thickness,
                       light_can_depth
                       )
blank_obj_orig.name = 'blank_obj_orig'

can_obj_orig = draw_can(object_number,
                       light_can_radius,
                       spacing_between_cans,
                       light_can_wall_thickness,
                       light_can_depth
                       )
can_obj_orig.name = 'can_obj_orig'

light_obj_orig = draw_light(object_number,
                       light_can_radius,
                       spacing_between_cans,
                       light_can_wall_thickness,
                       light_can_depth
                       )
light_obj_orig.name = 'light_obj_orig'





for x_light in range (0, (number_total)):
    light_status = config_dir['lights']['light'][x_light][3]

    if light_status == 'blank':
        print(light_status + str(x_light))
        # Number light
        # Duplicate blank_obj
        # Move to position
        bpy.ops.object.select_all(action='DESELECT')

        print(str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2]))        
        
        obj_orig = bpy.data.objects.get("blank_obj_orig")
        obj_orig.select = True

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, 
                                        TRANSFORM_OT_translate={"value":(obj_orig.location[0], obj_orig.location[0], obj_orig.location[0])})


        blank_obj = bpy.data.objects.get("blank_obj_orig.001")
        blank_obj.name = 'blank' + str(x_light)
        blank_obj.pass_index = 1
        mat = bpy.data.materials['sign_material']
        blank_obj.data.materials.append(mat)

        blank_obj = move_can(style,
                            light_can_radius,
                            spacing_between_cans,
                            number_total,
                            orientation,
                            x_light,
                            light_can_depth,
                            light_can_wall_thickness,
                            blank_obj)
        
        

    else:
        # Number light
        # Duplicate light_obj
        # Add lights specific colour
        # Move to position
        bpy.ops.object.select_all(action='DESELECT')

        print(light_status + str(x_light))
        print(str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2]))        
        
        obj_orig = bpy.data.objects.get("can_obj_orig")
        obj_orig.select = True

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, 
                                        TRANSFORM_OT_translate={"value":(obj_orig.location[0], obj_orig.location[0], obj_orig.location[0])})


        can_obj = bpy.data.objects.get("can_obj_orig.001")
        can_obj.name = 'can' + str(x_light)

        can_obj.pass_index = 1
        mat = bpy.data.materials['sign_material']
        can_obj.data.materials.append(mat)


        can_obj = move_can(style,
                            light_can_radius,
                            spacing_between_cans,
                            number_total,
                            orientation,
                            x_light,
                            light_can_depth,
                            light_can_wall_thickness,
                            can_obj)

        bpy.ops.object.select_all(action='DESELECT')
        obj_orig = bpy.data.objects.get("light_obj_orig")
        obj_orig.select = True

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, 
                                        TRANSFORM_OT_translate={"value":(obj_orig.location[0], obj_orig.location[0], obj_orig.location[0])})


        light_obj = bpy.data.objects.get("light_obj_orig.001")
        light_obj.name = 'light' + str(x_light)
     
        light_obj.pass_index = 1

        if light_status == 'on':
            mat = bpy.data.materials['light_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]
        else:
            mat = bpy.data.materials['light_off_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]
        
        light_obj.data.materials.append(mat)

        light_obj = move_can(style,
                            light_can_radius,
                            spacing_between_cans,
                            number_total,
                            orientation,
                            x_light,
                            light_can_depth,
                            light_can_wall_thickness,
                            light_obj)



if style == 'rectangle':
    background_obj = draw_background_rec(light_can_radius, 
                                         thickness,
                                         border_size,
                                         number_total,
                                         object_number,
                                         spacing_between_cans,
                                         orientation
                                         )
                        

elif style == 'reccir':
    background_obj = draw_background_reccir(light_can_radius, 
                                            thickness,
                                            border_size,
                                            number_total,
                                            object_number,
                                            spacing_between_cans,
                                            orientation
                                            )

elif style == 'circle':
    background_obj = draw_background_cir(light_can_radius, 
                                         thickness,
                                         border_size,
                                         number_total,
                                         object_number,
                                         spacing_between_cans,
                                         orientation
                                         )

elif style == 'cirtri':
    background_obj = draw_background_cir(light_can_radius, 
                                         thickness,
                                         border_size,
                                         number_total,
                                         object_number,
                                         spacing_between_cans,
                                         orientation
                                         )

elif style == 'square':
    background_obj = draw_background_squ(light_can_radius, 
                                         thickness,
                                         border_size,
                                         number_total,
                                         object_number,
                                         spacing_between_cans,
                                         orientation
                                         )

else:
    print('Background style Unknown')

objects = bpy.data.objects
objects.remove(objects["light_obj_orig"], True)
objects.remove(objects["blank_obj_orig"], True)
objects.remove(objects["can_obj_orig"], True)


for x in objects:
    bpy.data.objects[x.name].select = True
#bpy.ops.object.join()