import bpy
import numpy as np
import math
# from .configuration import configuration

# config_dir = configuration()
def configuration():

    config = {
        'background': {
            'style' : 'recroundtop', # rectangle, circle, reccir, cirtri, square, recroundtop
            'orientation' : 'vertical', #Vertical/Horizontal
            'border_size' : 0.1,
            'thickness' : 0.01,
            'bevel_radius' : 0.1,
            'colour' : {
                'diffuse' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'reflection1' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'reflection2' : [0.06, 0.06, 0.06], # [R, G, B]   # Fixed?
                'glossy' : [0.06, 0.06, 0.06] # [R, G, B]    # Fixed?
                }
        },
        'lights' : {
            'number_total' : 3,
            'light' : ([[1, 0, 0, 'on'],
                         [1, 0, 0, 'on'],
                         [0, 1, 0, 'off'],
                         [0, 1, 0, 'blank'],
                         [1, 1, 1, 'off'],
                         [1, 0, 0, 'off']]),
            'light_can_depth' : 0.069,
            'spacing_between_cans' : 0.015,
            'light_can_radius' : 0.1,
            'light_can_wall_thickness' : 0.01
        }
    }
    return config

config_dir = configuration()

#bpy.ops.import_mesh.stl(filepath="C://Users//fish_//OneDrive - The University Of Newcastle//Code//Mesh-Generation//Train Lights//Blender//Train_Aspect_Can.stl", filter_glob="*.stl",  files=[{"name":"Train_Aspect_Can.stl"}], directory="C://Users//fish_//OneDrive - The University Of Newcastle//Code//Mesh-Generation//Train Lights//Blender")

PBR_Toggle = True
Light_material_toggle = 'GLASS' #nothing, GLASS, RAMP (toggles both on and off)

# TODO read in config file

sign_values = np.array([[config_dir['background']['colour']['diffuse'][0], config_dir['background']['colour']['diffuse'][1], config_dir['background']['colour']['diffuse'][2], 1],
                        [config_dir['background']['colour']['reflection1'][0], config_dir['background']['colour']['reflection1'][1], config_dir['background']['colour']['reflection1'][2], 1],
                        [config_dir['background']['colour']['reflection2'][0], config_dir['background']['colour']['reflection2'][1], config_dir['background']['colour']['reflection2'][2], 1],
                        [config_dir['background']['colour']['glossy'][0], config_dir['background']['colour']['glossy'][1], config_dir['background']['colour']['glossy'][2], 1]])

style =       config_dir['background']['style']
orientation = config_dir['background']['orientation']
border_size = config_dir['background']['border_size']
thickness =   config_dir['background']['thickness']
bevel_radius =   config_dir['background']['bevel_radius']

light_values = np.array([[config_dir['lights']['light'][0][0], config_dir['lights']['light'][0][1], config_dir['lights']['light'][0][2], 1],
                         [config_dir['lights']['light'][1][0], config_dir['lights']['light'][1][1], config_dir['lights']['light'][1][2], 1],
                         [config_dir['lights']['light'][2][0], config_dir['lights']['light'][2][1], config_dir['lights']['light'][2][2], 1],
                         [config_dir['lights']['light'][3][0], config_dir['lights']['light'][3][1], config_dir['lights']['light'][3][2], 1],
                         [config_dir['lights']['light'][4][0], config_dir['lights']['light'][4][1], config_dir['lights']['light'][4][2], 1]])

light_can_depth =           config_dir['lights']['light_can_depth']
spacing_between_cans =      config_dir['lights']['spacing_between_cans']
light_can_radius =          config_dir['lights']['light_can_radius']
light_can_wall_thickness =  config_dir['lights']['light_can_wall_thickness']

if style == 'rectangle':
    number_total = config_dir['lights']['number_total']

elif style == 'reccir':
    number_total = config_dir['lights']['number_total']

elif style == 'recroundtop':
    number_total = config_dir['lights']['number_total']

elif style == 'circle':
    number_total = config_dir['lights']['number_total']
    if number_total > 3:
        number_total = 3

elif style == 'cirtri':
    number_total = config_dir['lights']['number_total']
    number_total = 3

elif style == 'square':
    number_total = config_dir['lights']['number_total']
    number_total = 5

else:
    print('Style Unknown')
    number_total = config_dir['lights']['number_total']

object_number = 0    #Ranom Variable (Number of objects)
object_name = [0]


# Romove previous materials
def delete_materials():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

#####################################################################################################################
#####################################################################################################################
#                                                  BACKGROUNDS                                                      #
#####################################################################################################################
#####################################################################################################################

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
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        temp = width
        width = height
        height = temp
        print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        print('Orientation Vertical')
        location_values = (0, -background_thickness, vertical_origin)
    
    # Calculate vertical position for background
    

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(width / 2, background_thickness, height / 2)

    obj.location=location_values

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
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
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size
    
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        print('Orientation Vertical')
        location_values = (0, -background_thickness, vertical_origin)

    if orientation == 'horizontal':
        vertical_origin = 0

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(height / 2, height / 2, background_thickness)

    obj.rotation_euler.x = -1.57

    obj.location= location_values

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
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
    height = ((light_can_radius + spacing_between_cans / 2) / (math.sqrt(3) / 2)) + light_radius + border_size
    

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(height, height, background_thickness)
    obj.rotation_euler.x = -1.57
    obj.location= (0, 0, 0)

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
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
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = bpy.data.objects[object_name[-1]]

    obj1.scale=(width / 2, background_thickness, height / 2)
    obj1.location=(0, -background_thickness, vertical_origin)

    # Create sign background circle
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

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
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
        mat = bpy.data.materials['sign_material']
    obj2.data.materials.append(mat)

    # Add material to sign
    obj1.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
        mat = bpy.data.materials['sign_material']
    obj1.data.materials.append(mat)


    return obj1


def draw_background_recroundtop(light_radius, 
                                background_thickness,
                                border_size,
                                no_lights,
                                object_number,
                                light_spacing,
                                orientation,
                                bevel_radius):

    

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size - 2 * bevel_radius
    vertical_origin = ((height + 2 * bevel_radius) / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        temp = width
        width = height
        height = temp
        print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        print('Orientation Vertical')
        location_values = (0, -background_thickness, vertical_origin)
    
    # Calculate vertical position for background
    





    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj2 = bpy.data.objects[object_name[-1]]

    obj2.scale=((width / 2) - bevel_radius, background_thickness, bevel_radius)

    obj2.location=(0, -background_thickness, vertical_origin + ((height + 2 * bevel_radius) / 2) - bevel_radius)

     # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj3 = bpy.data.objects[object_name[-1]]

    obj3.rotation_euler.x = 1.57
    obj3.scale=(bevel_radius, bevel_radius, background_thickness)

    obj3.location=((width / 2) - bevel_radius, -background_thickness, vertical_origin + ((height + 2 * bevel_radius) / 2) - bevel_radius)

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj4 = bpy.data.objects[object_name[-1]]

    obj4.rotation_euler.x = 1.57
    obj4.scale=(bevel_radius, bevel_radius, background_thickness)

    obj4.location=(-((width / 2) - bevel_radius), -background_thickness, vertical_origin + ((height + 2 * bevel_radius) / 2) - bevel_radius)





    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(width / 2, background_thickness, height / 2)

    obj.location=location_values

    obj.select = True
    obj2.select = True
    obj3.select = True
    obj4.select = True

    bpy.ops.object.join()

    # Add material to sign
    obj.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
        mat = bpy.data.materials['sign_material']
    obj.data.materials.append(mat)

    return obj


def draw_background_squ(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation):
    # Calculate width and height of sign background
    width = (math.sqrt((2 * light_radius + light_spacing) / 2)) + (2 * border_size) + (2 * light_radius)

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(
        location = (0, 0, 0)
        )

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(width / 2, background_thickness, width / 2)
    obj.location=(0, -background_thickness, 0)

    # Bevel edges of sign
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.1
    bpy.context.object.modifiers["Bevel"].segments = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

    # Add material to sign
    obj.pass_index = 1
    if PBR_Toggle:
        mat = bpy.data.materials['PBR_Dielectric']
    else:
        mat = bpy.data.materials['sign_material']
    obj.data.materials.append(mat)

    return obj


#####################################################################################################################
#####################################################################################################################
#                                                    LIGHTS                                                         #
#####################################################################################################################
#####################################################################################################################


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
    center = light_radius

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
             obj,
             light_status):
    # Orientation flips y and z location values
    # Independent of can type

    if style == 'reccir':
        center = (x_lights) * ((2 * light_can_radius) + spacing_between_cans)
        obj.location=(0, obj.location[1], center)

    elif style == 'square':

        # TODO some sort of X configuration
        vertical_offset = (math.sqrt((2 * light_can_radius + spacing_between_cans) * (2 * light_can_radius + spacing_between_cans) / 2))
        horizontal_offset = vertical_offset

        center_x = 0
        center_y = 0

        if x_lights == 1:

            center_x = -horizontal_offset
            center_y = -vertical_offset

        elif x_lights == 2:

            center_x = horizontal_offset
            center_y = -vertical_offset

        elif x_lights == 3:

            center_x = -horizontal_offset
            center_y = vertical_offset

        elif x_lights == 4:

            center_x = horizontal_offset
            center_y = vertical_offset

        else:
            print('Too many lights')

        obj.location=(center_x, obj.location[1], center_y)

    elif style == 'cirtri':

        # TODO some sort of X configuration

        center_x = 0 
        center_y = -(light_can_radius + spacing_between_cans / 2) / (math.sqrt(3) / 2)
        
        if x_lights == 1:

            center_y = (1 / math.sqrt(3)) * (light_can_radius + spacing_between_cans / 2)
            center_x = (light_can_radius + spacing_between_cans / 2)

        elif x_lights == 2:

            center_y = (1 / math.sqrt(3)) * (light_can_radius + spacing_between_cans / 2)
            center_x = -(light_can_radius + spacing_between_cans / 2)

        else:
            print('Too many lights')

        obj.location=(center_x, obj.location[1], center_y)

    else:
        center = (x_lights) * ((2 * light_can_radius) + spacing_between_cans)
        if orientation == 'vertical':
            obj.location=(0, obj.location[1], center)

        elif orientation == 'horizontal':
            obj.location=(center, obj.location[1], 0)

        else:
            print('Orientation Unknown')

    if light_status == 'on':
        add_signal_lamp(x_light, light_values, thickness, light_can_radius, spacing_between_cans, obj.location)

    return obj


def draw_post(object_number):

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]
    
    obj1.scale=(0.05, 0.05, 1.6)
    
    obj1.location=(0, -0.075, -1.6)

    return(obj1)


#####################################################################################################################
#####################################################################################################################
#                                                   MATERIALS                                                       #
#####################################################################################################################
#####################################################################################################################


def light_material(R, G, B):

    Alpha = 1

    mat = bpy.data.materials.get('light_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_material_' + str(R) + '_' + str(G) + '_'+ str(B))
    else:
    	return

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

def light_material_ramp(R, G, B):

    Alpha = 1

    mat = bpy.data.materials.get('light_material_ramp_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_material_ramp_' + str(R) + '_' + str(G) + '_'+ str(B))
    else:
    	return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    value_1 = nodes.new(type='ShaderNodeValue')
    value_1.name = value_1.label = 'Value 1'
    value_1.outputs[0].default_value = 1

    value_2 = nodes.new(type='ShaderNodeValue')
    value_2.name = value_2.label = 'Value 2'
    value_2.outputs[0].default_value = 1

    value_3 = nodes.new(type='ShaderNodeValue')
    value_3.name = value_3.label = 'Value 3'
    value_3.outputs[0].default_value = 1

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'
    translucent.inputs[0].default_value = (1, 1, 1, 1)

    emission_1 = nodes.new(type='ShaderNodeEmission')
    emission_1.name = emission_1.label = 'Emission 1'
    emission_1.inputs[0].default_value = (R, G, B, Alpha)
    emission_1.inputs[1].default_value = 5

    emission_2 = nodes.new(type='ShaderNodeEmission')
    emission_2.name = emission_2.label = 'Emission 2'
    emission_2.inputs[0].default_value = (R, G, B, Alpha)
    emission_2.inputs[1].default_value = 50

    mix_shader_1 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_1.name = mix_shader_1.label = 'Mix Shader 1'

    subtract_1 = nodes.new(type='ShaderNodeMath')
    subtract_1.name = subtract_1.label = 'Subtract 1'
    subtract_1.operation = 'SUBTRACT'

    subtract_2 = nodes.new(type='ShaderNodeMath')
    subtract_2.name = subtract_2.label = 'Subtract 2'
    subtract_2.operation = 'SUBTRACT'
    subtract_2.use_clamp = True

    divide_1 = nodes.new(type='ShaderNodeMath')
    divide_1.name = divide_1.label = 'Divide 1'
    divide_1.operation = 'DIVIDE'
    divide_1.inputs[0].default_value = 1

    divide_2 = nodes.new(type='ShaderNodeMath')
    divide_2.name = divide_2.label = 'Divide 1'
    divide_2.operation = 'DIVIDE'

    multiply_1 = nodes.new(type='ShaderNodeMath')
    multiply_1.name = multiply_1.label = 'Multiply 1'
    multiply_1.operation = 'MULTIPLY'

    multiply_2 = nodes.new(type='ShaderNodeMath')
    multiply_2.name = multiply_2.label = 'Multiply 2'
    multiply_2.operation = 'MULTIPLY'


    node_tree.links.new(value_1.outputs[0], multiply_1.inputs[1])
    node_tree.links.new(value_2.outputs[0], subtract_1.inputs[0])
    node_tree.links.new(value_2.outputs[0], divide_2.inputs[0])
    node_tree.links.new(value_3.outputs[0], subtract_1.inputs[0])

    node_tree.links.new(subtract_1.outputs[0], divide_1.inputs[1])
    node_tree.links.new(subtract_1.outputs[0], divide_2.inputs[1])
    node_tree.links.new(divide_1.outputs[0], multiply_1.inputs[0])
    node_tree.links.new(divide_2.outputs[0], subtract_2.inputs[1])
    node_tree.links.new(multiply_1.outputs[0], subtract_2.inputs[0])

    node_tree.links.new(subtract_2.outputs[0], mix_shader_1.inputs[0])
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(mix_shader_1.outputs['Shader'], multiply_2.inputs[0])
    node_tree.links.new(emission_1.outputs['Emission'], mix_shader_1.inputs[2])
    node_tree.links.new(emission_2.outputs['Emission'], output.inputs['Volume'])
    node_tree.links.new(multiply_2.outputs[0], output.inputs['Surface'])


def light_glass_material(light_values, 
                         i, 
                         wave_scale, 
                         wave_distortion, 
                         wave_detail, 
                         wave_detail_scale):

    glass_value = (light_values[i][0], 
                   light_values[i][1], 
                   light_values[i][2],
                   1)

    diffuse_value = (light_values[i][0] * 0.6, 
                     light_values[i][1] * 0.6, 
                     light_values[i][2] * 0.6,
                     1)

    mat = bpy.data.materials.get('light_glass_material_' + str(light_values[i][0]) + '_' + str(light_values[i][1]) + '_'+ str(light_values[i][2]))

    # TODO solve double creation of nodes
    # nodes_get = nodes.get

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_material_' + str(light_values[i][0]) + '_' + str(light_values[i][1]) + '_'+ str(light_values[i][2]))
        # nodes_get = nodes.new
    else:
    	return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'

    #translucent = check_node(mat, 'ShaderNodeBsdfTranslucent', 'Translucent', translucent)

    mix_shader_1 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_1.name = mix_shader_1.label = 'Mix Shader 1'

    #mix_shader_1 = check_node(mat, 'ShaderNodeMixShader', 'Mix Shader 1', mix_shader_1)

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    #mix_shader_2 = check_node(mat, 'ShaderNodeMixShader', 'Mix Shader 2', mix_shader_2)

    fresnel = nodes.new(type='ShaderNodeFresnel')
    fresnel.name = fresnel.label = 'Fresnel'

    #fresnel = check_node(mat, 'ShaderNodeFresnel', 'Fresnel', fresnel)

    glass = nodes.new(type='ShaderNodeBsdfGlass')
    glass.name = glass.label = 'Glass'
    #glass = check_node(mat, 'ShaderNodeBsdfGlass', 'Glass', glass)
    glass.inputs[0].default_value = glass_value
    glass.distribution = 'BECKMANN'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    #diffuse = check_node(mat, 'ShaderNodeBsdfDiffuse', 'Diffuse', diffuse)
    diffuse.inputs[0].default_value = diffuse_value

    wave_tex = nodes.new(type='ShaderNodeTexWave')
    wave_tex.name = wave_tex.label = 'Wave Texture'
    #wave_tex = check_node(mat, 'ShaderNodeTexWave', 'Wave Texture', wave_tex)
    wave_tex.inputs[1].default_value = wave_scale
    wave_tex.inputs[2].default_value = wave_distortion
    wave_tex.inputs[3].default_value = wave_detail
    wave_tex.inputs[4].default_value = wave_detail_scale

    node_tree.links.new(wave_tex.outputs[0], translucent.inputs[0])
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(glass.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[1])
    node_tree.links.new(diffuse.outputs[0], mix_shader_2.inputs[2])
    node_tree.links.new(fresnel.outputs[0], mix_shader_2.inputs[0])
    node_tree.links.new(mix_shader_2.outputs[0], output.inputs['Surface'])

def check_node(mat, check_node, node_label, node_name):

    if mat.use_nodes:
        node_tree = mat.node_tree
        nodes = node_tree.nodes
        node = nodes.get(check_node, None)

        if node is None:
            print("Not Found:", node)
            node_name = nodes.new(type=check_node)
            node_name.name = node_name.label = node_label

        else:
            if node.name == node_name:
                node_name = node
            else:
                node_name = nodes.new(type=check_node)
                node_name.name = node_name.label = node_label
    return(node_name)


def light_off_material(R, G, B):

    # TODO set emission value lower

    Alpha = 1

    mat = bpy.data.materials.get('light_off_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_off_material_' + str(R) + '_' + str(G) + '_'+ str(B))

    else:
    	return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = (R * 0.2, G * 0.2, B * 0.2, Alpha)

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

def light_glass_off_material(light_values, i):

    glass_value = (light_values[i][0] * 0.1, 
                   light_values[i][1] * 0.1, 
                   light_values[i][2] * 0.1,
                   1)

    diffuse_value = (light_values[i][0] * 0.05, 
                     light_values[i][1] * 0.05, 
                     light_values[i][2] * 0.05,
                     1)

    translucent_value = (light_values[i][0] * 0.05, 
                         light_values[i][1] * 0.05, 
                         light_values[i][2] * 0.05,
                         1)

    mat = bpy.data.materials.get('light_glass_off_material_' + str(light_values[i][0]) + '_' + str(light_values[i][1]) + '_'+ str(light_values[i][2]))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_off_material_' + str(light_values[i][0]) + '_' + str(light_values[i][1]) + '_'+ str(light_values[i][2]))


    else:
    	return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'
    translucent.inputs[0].default_value = translucent_value

    mix_shader_1 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_1.name = mix_shader_1.label = 'Mix Shader 1'

    mix_shader_2 = nodes.new(type='ShaderNodeMixShader')
    mix_shader_2.name = mix_shader_2.label = 'Mix Shader 2'

    fresnel = nodes.new(type='ShaderNodeFresnel')
    fresnel.name = fresnel.label = 'Fresnel'

    glass = nodes.new(type='ShaderNodeBsdfGlass')
    glass.name = glass.label = 'Glass'
    glass.inputs[0].default_value = glass_value
    glass.distribution = 'BECKMANN'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = diffuse_value


    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(glass.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[1])
    node_tree.links.new(diffuse.outputs[0], mix_shader_2.inputs[2])
    node_tree.links.new(fresnel.outputs[0], mix_shader_2.inputs[0])
    node_tree.links.new(mix_shader_2.outputs[0], output.inputs['Surface'])


def sign_material(sign_values):

    mat = bpy.data.materials.get('sign_material')

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('sign_material')


    else:
    	return

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

def PBR_Dielectric(roughness, reflection, diffuse_values, glossy_values, noise_values, mat_name):
    import bpy
    mat = bpy.data.materials.get(mat_name)

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new(mat_name)

    else:
    	return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    RGB_COLOUR_WHITE = (1, 1, 1)
    RGB_COLOUR = (0.58, 0.57, 0.56)

    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.name = noise.label = 'Noise Texture'

    value_1 = nodes.new(type='ShaderNodeValue')
    value_1.name = value_1.label = 'Roughness'

    value_2 = nodes.new(type='ShaderNodeValue')
    value_2.name = value_2.label = 'Reflection'

    geometry = nodes.new(type='ShaderNodeNewGeometry')
    geometry.name = geometry.label = 'Geometry'

    bump_1 = nodes.new(type='ShaderNodeBump')
    bump_1.name = bump_1.label = 'Bump 1'

    mix_rgb_1 = nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_1.name = mix_rgb_1.label = 'Mix RGB 1'

    fresnel = nodes.new(type='ShaderNodeFresnel')
    fresnel.name = fresnel.label = 'Fresnel 1'

    mix_rgb_2 = nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_2.name = mix_rgb_2.label = 'Mix RGB 2'

    glossy_1 = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy_1.name = glossy_1.label = 'Glossy 1'

    mix_1 = nodes.new(type='ShaderNodeMixShader')
    mix_1.name = mix_1.label = 'Mix 1'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'

    power_1 = nodes.new(type='ShaderNodeMath')
    power_1.name = power_1.label = 'Power 1'
    power_1.operation = 'POWER'

    power_2 = nodes.new(type='ShaderNodeMath')
    power_2.name = power_2.label = 'Power 2'
    power_2.operation = 'POWER'


    value_1.outputs[0].default_value = roughness
    value_2.outputs[0].default_value = reflection
    noise.inputs['Scale'].default_value = noise_values[0]
    noise.inputs['Detail'].default_value = noise_values[1]
    noise.inputs['Distortion'].default_value = noise_values[2]
    node_tree.links.new(noise.outputs[0], glossy_1.inputs[2])
    node_tree.links.new(noise.outputs[0], diffuse.inputs[2])



    diffuse.inputs[0].default_value = (diffuse_values[0], diffuse_values[1], diffuse_values[2], 1)
    node_tree.links.new(diffuse.inputs[1], value_1.outputs[0])
    node_tree.links.new(power_1.inputs['Value'], value_2.outputs[0])
    node_tree.links.new(power_2.inputs['Value'], value_2.outputs[0])
    #bump_1.inputs['Normal'].default_value
    #glossy_1.inputs['Normal'].default_value

    node_tree.links.new(geometry.outputs['Incoming'], mix_rgb_1.inputs[2])

    node_tree.links.new(diffuse.outputs['BSDF'], mix_1.inputs[1])
    node_tree.links.new(power_1.outputs['Value'], mix_rgb_1.inputs['Fac'])
    node_tree.links.new(power_1.outputs['Value'], glossy_1.inputs['Roughness'])
    node_tree.links.new(power_2.outputs['Value'], mix_rgb_2.inputs[1])

    node_tree.links.new(bump_1.outputs['Normal'], mix_rgb_1.inputs[1])
    node_tree.links.new(mix_rgb_1.outputs[0], fresnel.inputs['Normal'])
    node_tree.links.new(fresnel.outputs['Fac'], mix_rgb_2.inputs['Fac'])

    mix_rgb_2.inputs[2].default_value = (1, 1, 1, 1)
    glossy_1.inputs[0].default_value = (glossy_values[0], glossy_values[1], glossy_values[2], 1)

    node_tree.links.new(mix_rgb_2.outputs[0], mix_1.inputs['Fac'])
    node_tree.links.new(glossy_1.outputs['BSDF'], mix_1.inputs[2])

    node_tree.links.new(output.inputs[0], mix_1.outputs[0])


#####################################################################################################################
#####################################################################################################################
#                                                    CAMERA                                                         #
#####################################################################################################################
#####################################################################################################################


def camera_add(location_values, angle_values, type):

    bpy.ops.object.camera_add(location=(location_values), 
                              rotation=(angle_values))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    if type == 'PANO':
        obj.data.type = 'PANO'
        obj.data.cycles.panorama_type = 'FISHEYE_EQUIDISTANT'
        obj.data.cycles.fisheye_fov = 2.37365 # 136 degrees
        obj.data.sensor_width = 32 # mm 

    else:   
        obj.data.type = 'PERSP'
        obj.data.lens = 35
        obj.data.sensor_width = 32 # mm 


def lamp_add(object_number,
             object_name):
    object_number = object_number + 1
    bpy.ops.object.lamp_add(type='HEMI',
                            location=(100, 20, 400)
                            )
    bpy.ops.transform.rotate(value = 0, axis=(0.207868, -0.752946, -0.62439))
    #emission.inputs[0].default_value = (1, 1, 1)
    #emission.inputs[1].default_value = 1
    object_name.append(bpy.context.active_object.name)
    obj = objects[object_name[-1]]
    obj.name = 'Main Sun'
    mesh_name = bpy.data.objects['Main Sun'].data.name
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[1].default_value = 80
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[0].default_value = (1, 1, 1, 1)
    obj.rotation_euler.x = 0.785398 #0.698132
    obj.rotation_euler.z = 2.251475 #2.268928

def add_signal_lamp(x_light, light_values, background_thickness, light_can_radius, spacing_between_cans, location):

    location_values = (location[0], background_thickness * 1.01 + location[1], location[2])
    light_values = (0.426 * light_values[x_light][0], 0.426 * light_values[x_light][1], 0.426 * light_values[x_light][2], 1)

    bpy.ops.object.lamp_add(type='AREA',
                            location=location_values
                            )
    bpy.context.object.data.size = 0.001
    object_name.append(bpy.context.active_object.name)
    obj = objects[object_name[-1]]
    obj.name = 'Signal' + str(x_light)
    mesh_name = bpy.data.objects['Signal' + str(x_light)].data.name
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[1].default_value = 0.5
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[0].default_value = light_values
    obj.rotation_euler.x = 1.57
    obj.rotation_euler.z = 0.139626

    print('I made a lamp :)')

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
scene.render.resolution_x = 4500
scene.render.resolution_y = 2300
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
        if Light_material_toggle == 'RAMP':
            light_material_ramp(light_values[i][0], 
                                light_values[i][1], 
                                light_values[i][2],
                                )
        elif Light_material_toggle == 'GLASS':
            light_glass_material(light_values,
                                 i,
                                 2, 
                                 1, 
                                 5, 
                                 1)
        else:
            light_material(light_values[i][0], 
                           light_values[i][1], 
                           light_values[i][2],
                           )

    elif config_dir['lights']['light'][i][3] == 'off':
        
        if Light_material_toggle == 'GLASS':
            light_glass_off_material(light_values, i)
        else:
            light_off_material(light_values[i][0], 
                           light_values[i][1], 
                           light_values[i][2],
                           )

    else:
        i = i
        #print('blank light')

sign_material(sign_values)

roughness = 0.05
reflection = 0.6
diffuse = (0, 0, 0)
glossy = (0.009, 0.010, 0.012)
noise = (2, 1, 6)

PBR_Dielectric(roughness, reflection, diffuse, glossy, noise, 'PBR_Dielectric')

roughness = 0.3
reflection = 0.5
diffuse = (0, 0, 0)
glossy = (0.039, 0.045, 0.056)
noise = (10, 1, 0)

PBR_Dielectric(roughness, reflection, diffuse, glossy, noise, 'PBR_Dielectric_post')

center = (number_total) * ((2 * light_can_radius) + spacing_between_cans)

objects = bpy.data.objects


for x_light in range (0, (number_total)):
    light_status = config_dir['lights']['light'][x_light][3]

    if light_status == 'blank':
        print(light_status + str(x_light))
        # Number light
        # Duplicate blank_obj
        # Move to position
        blank_obj = draw_blank(object_number,
                               light_can_radius,
                               spacing_between_cans,
                               light_can_wall_thickness,
                               light_can_depth
                               )

        blank_obj.name = 'blank' + str(x_light)
        blank_obj.pass_index = 1
        if PBR_Toggle:
            mat = bpy.data.materials['PBR_Dielectric']
        else:
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
                             blank_obj,
                             light_status)
        
        

    else:
        # Number light
        # Duplicate light_obj
        # Add lights specific colour
        # Move to position
        bpy.ops.object.select_all(action='DESELECT')

        print(light_status + str(x_light))
        print(str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2]))        
        
        can_obj = draw_can(object_number,
                           light_can_radius,
                           spacing_between_cans,
                           light_can_wall_thickness,
                           light_can_depth
                           )

        can_obj.name = 'can' + str(x_light)

        can_obj.pass_index = 1
        if PBR_Toggle:
            mat = bpy.data.materials['PBR_Dielectric']
        else:
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
                           can_obj,
                           light_status)

        light_obj = draw_light(object_number,
                               light_can_radius,
                               spacing_between_cans,
                               light_can_wall_thickness,
                               light_can_depth
                               )

        light_obj.name = 'light' + str(x_light)
     
        light_obj.pass_index = 1

        if light_status == 'on':
            if Light_material_toggle == 'RAMP':
                mat = bpy.data.materials['light_material_ramp_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]
            
            elif Light_material_toggle == 'GLASS':
                mat = bpy.data.materials['light_glass_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]

            else:
                mat = bpy.data.materials['light_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]
                    
        else:
            if Light_material_toggle == 'GLASS':
                mat = bpy.data.materials['light_glass_off_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]

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
                             light_obj,
                             light_status)



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

elif style == 'recroundtop':
    background_obj = draw_background_recroundtop(light_can_radius, 
                                            thickness,
                                            border_size,
                                            number_total,
                                            object_number,
                                            spacing_between_cans,
                                            orientation,
                                            bevel_radius
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
    background_obj = draw_background_cirtri(light_can_radius, 
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


#####################################################################################################################
#####################################################################################################################
#                                                      POST                                                         #
#####################################################################################################################
#####################################################################################################################



post_obj = draw_post(object_number)

if PBR_Toggle:
    mat = bpy.data.materials['PBR_Dielectric_post']
else:
    mat = bpy.data.materials['sign_material']

post_obj.data.materials.append(mat)

for x in objects:
    bpy.data.objects[x.name].select = True
bpy.ops.object.join()

# s = 'Signal'
# for x in objects.name:
# 	if s.find('Signal') != -1:
# 		x.select =True

# TODO rotate signal lights

bpy.context.object.location = (0, -0.075, -1.57269)
bpy.context.object.rotation_euler.z = 0.139626 # 8 deg

# for x in
#     bpy.context.object.location = (0, -0.075, -1.57269)
#     bpy.context.object.rotation_euler.z = 0.139626 # 8 deg



#####################################################################################################################
#####################################################################################################################
#                                          SHADOW CATCHER    CAMERA    LAMPS                                        #
#####################################################################################################################
#####################################################################################################################



bpy.ops.mesh.primitive_plane_add(location=(0, 0, -3))
bpy.context.object.scale=(5, 5, 1)
#mat = bpy.data.materials['light_off_material_' + str(light_values[x_light][0]) + '_' + str(light_values[x_light][1]) + '_' + str(light_values[x_light][2])]
#bpy.context.object.data.materials.append(mat)
bpy.context.object.cycles.is_shadow_catcher = True


location_values = (0.94495, 14.53555, 0.79661)
angle_values = (1.424895, -0.002425, 3.103351)

camera_add(location_values, angle_values, 'PERSP')

lamp_add(object_number, object_name)






y = abs(mod(2x, 1) - 0.5)
