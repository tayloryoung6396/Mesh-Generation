import bpy
import numpy as np
import math
import os
import random
import yaml
import json

# from .configuration import configuration

Input_meta_file  = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/VIRB0045-8.json'
Output_meta_file = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Output-meta/'
Input_img_file   = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Input/'


# config_dir = configuration()

def configuration():

    # TODO Remove unused variables
    # TODO read in config file

    config = {
        'background': {
            'style' : ('rectangle', 'circle', 'reccir', 'cirtri', 'square', 'recround'),
            'orientation' : ('vertical', 'horizontal'),
            'border_size' : (0.1, 0.1), #0.1, # Range []
            'thickness' : 0.01,
            'bevel_radius' : (0.1, 0.3), #0.1, # Range []
            'post' : {
                'roughness_p' : 0.3,
                'reflection_p' : 0.5,
                'diffuse_p' : (0, 0, 0),
                'glossy_p' : (0.039, 0.045, 0.056),
                'noise_p' : (10, 1, 0)
            },
            'sign' : {
                'roughness_s' : 0.05,
                'reflection_s' : 0.6,
                'diffuse_s' : (0, 0, 0),
                'glossy_s' : (0.009, 0.010, 0.012),
                'noise_s' : (2, 1, 6)
            }
        },
        'lights' : {
            'number_total' : (1, 5), #3, # Range [1, 5]
            'light' : ('red', 'green'),
            'light_status' : ('on', 'off', 'blank'),
            'light_can_depth' : (0.03, 0.069), #0.069, # Range [0.03, 0.069]
            'light_spacing' : (0.01, 0.3), #0.015, # Range []
            'light_radius' : (0.1, 0.2), #0.1, # Range []
            'light_wall_thickness' : (0.005, 0.01) #0.01 # Range []
        },
        'sign_parameters' : {
            'height' : (1.0, 2.0), #1.6, # Range [0.5, 2]
            'radius' : 0.05,
            'position' : {
                'x' : 0, # Range [] left right maybe should be related and follow some relationship / array to account for other lines
                'y' : -0.075, # Range [] front back maybe should be related and follow some relationship / array to account for other lines
                'z' : -1.57269 # Fixed
            },
            'rotation' : {
                'x' : 0, # Range [0]
                'y' : 0, # Range [0]
                'z' : 0 # Range [-10, 10] [170, 190] # TODO add front back variable and insert this rotation in it
                                                     # also alter positive negative depending on left or right
                                                     # probably fix this value to a small range [6, 10]
            }
        },
        'camera_parameters' : {
            'type' : 'PERSP', # PANO, PERSP
            'FOV' : 2.37365,
            'lens' : 35, # mm
            'sensor_width' : 32 # mm
        }
    }
    return config


config_dir = configuration()


# Remove previous materials (for testing)
def delete_materials():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

        # Remove previous materials (for testing)
def delete_compositor():
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
                        orientation,
                        bevel_radius):

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        temp = width
        width = height
        height = temp
        #print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        #print('Orientation Vertical')
        location_values = (0, -background_thickness, vertical_origin)    

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
    mat = bpy.data.materials['PBR_Dielectric']
    obj.data.materials.append(mat)

    output_data['sign_parameters']['sign_height'] = height
    output_data['sign_parameters']['sign_width'] = width

    return obj

def draw_background_cir(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation,
                        bevel_radius):

    # Calculate width and height of sign background
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size 
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

    if orientation == 'horizontal':
        # print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        # print('Orientation Vertical')
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
    mat = bpy.data.materials['PBR_Dielectric']
    obj.data.materials.append(mat)

    output_data['sign_parameters']['sign_height'] = height
    output_data['sign_parameters']['sign_width'] = height

    return obj

def draw_background_cirtri(light_radius, 
                           background_thickness,
                           border_size,
                           no_lights,
                           object_number,
                           light_spacing,
                           orientation,
                           bevel_radius):

    # Calculate width and height of sign background
    height = ((light_radius + light_spacing / 2) / (math.sqrt(3) / 2)) + light_radius + border_size
    
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
    mat = bpy.data.materials['PBR_Dielectric']
    obj.data.materials.append(mat)

    output_data['sign_parameters']['sign_height'] = height
    output_data['sign_parameters']['sign_width'] = height

    return obj

def draw_background_reccir(light_radius, 
                           background_thickness,
                           border_size,
                           no_lights,
                           object_number,
                           light_spacing,
                           orientation,
                           bevel_radius):

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

    mat = bpy.data.materials['PBR_Dielectric']
    obj2.data.materials.append(mat)

    # Add material to sign   
    mat = bpy.data.materials['PBR_Dielectric']
    obj1.data.materials.append(mat)


    output_data['sign_parameters']['sign_height'] = height + height_circle
    output_data['sign_parameters']['sign_width'] = width

    return obj1

def draw_background_recround(light_radius, 
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
        # print('Orientation Horizontal')
        location_values = (vertical_origin, -background_thickness, 0)

    else:
        # print('Orientation Vertical')
        location_values = (0, -background_thickness, vertical_origin)

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
    obj3.location=((width / 2) - bevel_radius, 
                    -background_thickness, 
                    vertical_origin + ((height + 2 * bevel_radius) / 2) - bevel_radius
                    )

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj4 = bpy.data.objects[object_name[-1]]

    obj4.rotation_euler.x = 1.57
    obj4.scale=(bevel_radius, bevel_radius, background_thickness)
    obj4.location=(-((width / 2) - bevel_radius), 
                      -background_thickness, 
                      vertical_origin + ((height + 2 * bevel_radius) / 2) - bevel_radius)

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    obj.scale=(width / 2, background_thickness, height / 2)
    obj.location=location_values

    # TODO this is kinda terrible but works..
    obj.select = True
    obj2.select = True
    obj3.select = True
    obj4.select = True

    bpy.ops.object.join()

    # Add material to sign    
    mat = bpy.data.materials['PBR_Dielectric']
    obj.data.materials.append(mat)

    output_data['sign_parameters']['sign_height'] = height + bevel_radius
    output_data['sign_parameters']['sign_width'] = width

    return obj

def draw_background_squ(light_radius, 
                        background_thickness,
                        border_size,
                        no_lights,
                        object_number,
                        light_spacing,
                        orientation,
                        bevel_radius):

    # Calculate width and height of sign background
    width = (math.sqrt((2 * light_radius + light_spacing) / 2)) + (2 * border_size) + (2 * light_radius)

    # Create sign background
    object_number = object_number + 1
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))

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
    mat = bpy.data.materials['PBR_Dielectric']
    obj.data.materials.append(mat)

    output_data['sign_parameters']['sign_height'] = width
    output_data['sign_parameters']['sign_width'] = width

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
             light_radius,
             light_spacing,
             number_total,
             orientation,
             x_lights,
             light_depth,
             light_wall_thickness,
             obj,
             light_status):

    # Orientation flips y and z location values
    # Independent of can type

    if style == 'reccir':
        center = (x_lights) * ((2 * light_radius) + light_spacing)
        obj.location=(0, obj.location[1], center)

    elif style == 'square':

        vertical_offset = (math.sqrt((2 * light_radius + light_spacing) * (2 * light_radius + light_spacing) / 2))
        horizontal_offset = vertical_offset

        center_x = 0
        center_y = 0
        if x_lights == 0:
            center_x = center_x
        elif x_lights == 1:

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
            print('Too many lights 1, ' + str(x_lights))

        obj.location=(center_x, obj.location[1], center_y)

    elif style == 'cirtri':

        center_x = 0 
        center_y = -(light_radius + light_spacing / 2) / (math.sqrt(3) / 2)
        
        if x_lights == 0:
            center_x = center_x
        elif x_lights == 1:

            center_y = (1 / math.sqrt(3)) * (light_radius + light_spacing / 2)
            center_x = (light_radius + light_spacing / 2)

        elif x_lights == 2:

            center_y = (1 / math.sqrt(3)) * (light_radius + light_spacing / 2)
            center_x = -(light_radius + light_spacing / 2)

        else:
            print('Too many lights 2, '  + str(x_lights))

        obj.location=(center_x, obj.location[1], center_y)

    else:
        center = (x_lights) * ((2 * light_radius) + light_spacing)
        if orientation == 'vertical':
            obj.location=(0, obj.location[1], center)

        elif orientation == 'horizontal':
            obj.location=(center, obj.location[1], 0)

        else:
            print('Orientation Unknown')

    if light_status == 'on':
        add_signal_lamp(x_light, light_values, thickness, light_radius, light_spacing, obj.location)

    return obj

def draw_post(object_number,
              number_total,
              light_radius,
              border_size,
              light_spacing):

    background_height = (number_total * light_radius * 2) + ((number_total - 1) * light_spacing) + border_size * 2

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]

    obj1.scale=(post_radius, 
                post_radius,
                sign_height)

    obj1.location=(0, 
                   -0.075,
                   -((sign_height) - (background_height - border_size - light_radius))
                   )

    return(obj1)

#####################################################################################################################
#####################################################################################################################
#                                                   MATERIALS                                                       #
#####################################################################################################################
#####################################################################################################################

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

    diffuse_value = (light_values[i][0] * 0.6 / 30, 
                     light_values[i][1] * 0.6 / 30, 
                     light_values[i][2] * 0.6 / 30,
                     1)

    mat = bpy.data.materials.get('light_glass_material_' 
                                + str(int(light_values[i][0])) + '_' 
                                + str(int(light_values[i][1])) + '_'
                                + str(int(light_values[i][2])))

    # TODO solve double creation of nodes

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_material_'
                                    + str(int(light_values[i][0])) + '_' 
                                    + str(int(light_values[i][1])) + '_'
                                    + str(int(light_values[i][2])))
    else:
        return

    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    output = nodes['Material Output']

    translucent = nodes.new(type='ShaderNodeBsdfTranslucent')
    translucent.name = translucent.label = 'Translucent'

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

    wave_tex = nodes.new(type='ShaderNodeTexWave')
    wave_tex.name = wave_tex.label = 'Wave Texture'
    wave_tex.inputs[1].default_value = wave_scale
    wave_tex.inputs[2].default_value = wave_distortion
    wave_tex.inputs[3].default_value = wave_detail
    wave_tex.inputs[4].default_value = wave_detail_scale

    # Link nodes
    node_tree.links.new(wave_tex.outputs[0], translucent.inputs[0])
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(glass.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[1])
    node_tree.links.new(diffuse.outputs[0], mix_shader_2.inputs[2])
    node_tree.links.new(fresnel.outputs[0], mix_shader_2.inputs[0])
    node_tree.links.new(mix_shader_2.outputs[0], output.inputs['Surface'])


def light_glass_off_material(light_values, i):

    glass_value = (light_values[i][0] * 0.1, 
                   light_values[i][1] * 0.1, 
                   light_values[i][2] * 0.1,
                   1)

    diffuse_value = (light_values[i][0] * 0.05 * 0.01, 
                     light_values[i][1] * 0.05 * 0.01, 
                     light_values[i][2] * 0.05 * 0.01,
                     1)

    translucent_value = (light_values[i][0] * 0.05, 
                         light_values[i][1] * 0.05, 
                         light_values[i][2] * 0.05,
                         1)

    mat = bpy.data.materials.get('light_glass_off_material_' 
                                 + str(int(light_values[i][0])) + '_' 
                                 + str(int(light_values[i][1])) + '_'
                                 + str(int(light_values[i][2])))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_off_material_' 
                                     + str(int(light_values[i][0])) + '_' 
                                     + str(int(light_values[i][1])) + '_'
                                     + str(int(light_values[i][2])))
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

    # Link Nodes
    node_tree.links.new(translucent.outputs['BSDF'], mix_shader_1.inputs[2])
    node_tree.links.new(glass.outputs['BSDF'], mix_shader_1.inputs[1])
    node_tree.links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[1])
    node_tree.links.new(diffuse.outputs[0], mix_shader_2.inputs[2])
    node_tree.links.new(fresnel.outputs[0], mix_shader_2.inputs[0])
    node_tree.links.new(mix_shader_2.outputs[0], output.inputs['Surface'])

def PBR_Dielectric(roughness, 
                   reflection, 
                   diffuse_values, 
                   glossy_values, 
                   noise_values, 
                   mat_name):

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
    noise.inputs['Scale'].default_value = noise_values[0]
    noise.inputs['Detail'].default_value = noise_values[1]
    noise.inputs['Distortion'].default_value = noise_values[2]

    value_1 = nodes.new(type='ShaderNodeValue')
    value_1.name = value_1.label = 'Roughness'
    value_1.outputs[0].default_value = roughness

    value_2 = nodes.new(type='ShaderNodeValue')
    value_2.name = value_2.label = 'Reflection'
    value_2.outputs[0].default_value = reflection

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
    mix_rgb_2.inputs[2].default_value = (1, 1, 1, 1)

    glossy_1 = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy_1.name = glossy_1.label = 'Glossy 1'
    glossy_1.inputs[0].default_value = (glossy_values[0], glossy_values[1], glossy_values[2], 1)

    mix_1 = nodes.new(type='ShaderNodeMixShader')
    mix_1.name = mix_1.label = 'Mix 1'

    diffuse = nodes['Diffuse BSDF']
    diffuse.name = diffuse.label = 'Diffuse'
    diffuse.inputs[0].default_value = (diffuse_values[0], diffuse_values[1], diffuse_values[2], 1)

    power_1 = nodes.new(type='ShaderNodeMath')
    power_1.name = power_1.label = 'Power 1'
    power_1.operation = 'POWER'

    power_2 = nodes.new(type='ShaderNodeMath')
    power_2.name = power_2.label = 'Power 2'
    power_2.operation = 'POWER'
    
    node_tree.links.new(noise.outputs[0], glossy_1.inputs[2])
    node_tree.links.new(noise.outputs[0], diffuse.inputs[2])
    node_tree.links.new(diffuse.inputs[1], value_1.outputs[0])
    node_tree.links.new(power_1.inputs['Value'], value_2.outputs[0])
    node_tree.links.new(power_2.inputs['Value'], value_2.outputs[0])

    node_tree.links.new(geometry.outputs['Incoming'], mix_rgb_1.inputs[2])
    node_tree.links.new(diffuse.outputs['BSDF'], mix_1.inputs[1])
    node_tree.links.new(power_1.outputs['Value'], mix_rgb_1.inputs['Fac'])
    node_tree.links.new(power_1.outputs['Value'], glossy_1.inputs['Roughness'])
    node_tree.links.new(power_2.outputs['Value'], mix_rgb_2.inputs[1])

    node_tree.links.new(bump_1.outputs['Normal'], mix_rgb_1.inputs[1])
    node_tree.links.new(mix_rgb_1.outputs[0], fresnel.inputs['Normal'])
    node_tree.links.new(fresnel.outputs['Fac'], mix_rgb_2.inputs['Fac'])
    node_tree.links.new(mix_rgb_2.outputs[0], mix_1.inputs['Fac'])
    node_tree.links.new(glossy_1.outputs['BSDF'], mix_1.inputs[2])

    node_tree.links.new(output.inputs[0], mix_1.outputs[0])

def compositor_add():
    
    # Link up our output layers to file output nodes
    nodes = scene.node_tree.nodes

    render_layers = nodes.new(type="CompositorNodeRLayers")
    render_layers.name = render_layers.label = 'render_layers'
    background_layers = nodes.new(type="CompositorNodeImage")
    background_layers.name = background_layers.label = 'background_layers'
    mix = nodes.new(type="CompositorNodeMixRGB")
    mix.name = mix.label = 'mix'
    mask = nodes.new(type="CompositorNodeIDMask")
    mask.name = mask.label = 'mask'
    mask.index = 1

    indexob_file = nodes.new('CompositorNodeOutputFile')
    indexob_file.name = indexob_file.label = 'indexob_file'
    image_file = nodes.new('CompositorNodeOutputFile')
    image_file.name = image_file.label = 'image_file'

    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask.inputs[0])
    scene.node_tree.links.new(mask.outputs[0], indexob_file.inputs['Image'])
    scene.node_tree.links.new(render_layers.outputs['Image'], mix.inputs[2])
    scene.node_tree.links.new(background_layers.outputs['Image'], mix.inputs[1])
    scene.node_tree.links.new(render_layers.outputs['Alpha'], mix.inputs[0])
    scene.node_tree.links.new(mix.outputs[0], image_file.inputs['Image'])

    composite = nodes.new(type='CompositorNodeComposite')
    scene.node_tree.links.new(mix.outputs[0], composite.inputs[0])


def compositor_set(frame_number,
                   background_img):
    
    # Link up our output layers to file output nodes
    nodes = scene.node_tree.nodes

    render_layers = nodes['render_layers']
    background_layers = nodes['background_layers']
    indexob_file = nodes['indexob_file']
    image_file = nodes['image_file']

    indexob_file.base_path = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Output-stn/'
    indexob_file.file_slots[0].path = 'stencil' + str(frame_number)
    image_file.base_path = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Output-img/'
    image_file.file_slots[0].path = 'image' + str(frame_number)

    background_layers.image = background_img

#####################################################################################################################
#####################################################################################################################
#                                                    CAMERA                                                         #
#####################################################################################################################
#####################################################################################################################

def camera_add(location_values, angle_values, camera):

    bpy.ops.object.camera_add(location=(location_values), 
                              rotation=(angle_values))

    object_name.append(bpy.context.active_object.name)
    obj = bpy.data.objects[object_name[-1]]

    if type == 'PANO':
        obj.data.type = camera['type']
        obj.data.cycles.panorama_type = 'FISHEYE_EQUIDISTANT'
        obj.data.cycles.fisheye_fov = camera['FOV']
        obj.data.sensor_width = camera['sensor_width'] 

    else:   
        obj.data.type = camera['type']
        obj.data.lens = camera['lens']
        obj.data.sensor_width = camera['sensor_width'] 

def lamp_add(object_number, 
             object_name, 
             sun_rotation):
    object_number = object_number + 1
    bpy.ops.object.lamp_add(type='SUN',
                            location=(0, 0, 0)
                            )
    object_name.append(bpy.context.active_object.name)
    obj = objects[object_name[-1]]
    obj.name = 'Main Sun'
    mesh_name = bpy.data.objects['Main Sun'].data.name
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[1].default_value = 50
    bpy.data.lamps[mesh_name].node_tree.nodes['Emission'].inputs[0].default_value = (1, 1, 1, 1)
    obj.rotation_euler.x = sun_rotation[0]
    obj.rotation_euler.y = sun_rotation[1]
    obj.rotation_euler.z = sun_rotation[2]

def add_signal_lamp(x_light, light_values, background_thickness, light_radius, light_spacing, location):

    location_values = (location[0], background_thickness * 1.01 + location[1], location[2])
    light_values = (0.426 * light_values[x_light][0], 
                    0.426 * light_values[x_light][1], 
                    0.426 * light_values[x_light][2], 1)

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

def load_img(frame_number):

    #filepath = "/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/4tel_train_images/frame" + str(frame_number) + ".jpg"
    filepath = Input_img_file + 'frame' + str(frame_number) + '.jpg'
    #filepath = "C:/Users/Taylor/OneDrive - The University Of Newcastle/Code/Mesh-Generation/Train-Lights/Blender/Input/frame" + str(frame_number) + ".jpg"
    img = bpy.data.images.load(filepath, check_existing=False)

    return(img)

#####################################################################################################################
#####################################################################################################################
#                                                   SUN STUFF                                                       #
#####################################################################################################################
#####################################################################################################################

def sunpos(timestamp, latitude, longitude):

    earth_mean_radius = 6371.01
    astronomical_unit = 149597890

    # Calculate the epoch of 1 January 2000 at 12:00pm
    almanac_epoch = 946688400
    days_since_epoch = (timestamp - almanac_epoch) / (60 * 60 * 24)

    # Calculate ecliptic coordinates (ecliptic longitude and obliquity of the
    # ecliptic in radians but without limiting the angle to be less than 2*Pi) 
    # (i.e., the result may be greater than 2*Pi)
    omega = 2.1429 - 0.0010394594 * days_since_epoch
    mean_latitude = 4.8950630 + 0.017202791698 * days_since_epoch # Radians
    mean_anomaly = 6.2400600 + 0.0172019699 * days_since_epoch
    ecliptic_longitude = mean_latitude + 0.03341607 * math.sin(mean_anomaly) + 0.00034894 * math.sin(2 * mean_anomaly) - 0.0001134 - 0.0000203 * math.sin(omega)
    ecliptic_obliquity = 0.4090928 - 6.2140e-9 * days_since_epoch + 0.0000396 * math.cos(omega)

    # Calculate celestial coordinates ( right ascension and declination ) in radians 
    # but without limiting the angle to be less than 2*Pi (i.e., the result may be 
    # greater than 2*Pi)
    dY = math.cos(ecliptic_obliquity) * math.sin(ecliptic_longitude)
    dX = math.cos(ecliptic_longitude)
    right_ascension = math.atan2(dY, dX)
    if right_ascension < 0.0:
        right_ascension += math.pi * 2.0
    declination = math.asin(math.sin(ecliptic_obliquity) * math.sin(ecliptic_longitude))
    

    # Calculate local coordinates ( azimuth and zenith angle ) in degrees
    gmst = 18.697374558 + 24.06570982441908 * days_since_epoch
    lmst = (gmst * 15 * (math.pi / 180) + longitude)
    hour_angle = lmst - right_ascension


    zenith = math.acos(math.cos(latitude) * math.cos(hour_angle) * math.cos(declination) + math.sin(declination) * math.sin(latitude))
    dY = -math.sin(hour_angle)
    dX = math.tan(declination) * math.cos(latitude) - math.sin(latitude) * math.cos(hour_angle)
    
    azimuth = math.atan2(dY, dX)
    if azimuth < 0.0:
        azimuth += math.pi * 2.0

    # Parallax Correction
    parallax = (earth_mean_radius / astronomical_unit) * math.sin(zenith)
    zenith += parallax

    # print('zenith sunpos rads: {}'.format(zenith))
    # print('azimuth sunpos rads: {}'.format(azimuth))
    
    return (zenith, azimuth)


def sun_location(zenith, azimuth, heading):

    # Account for Heading to Azimuth
    theta = heading - azimuth
    sun_rotation = (-zenith,
                    0,
                    theta)

    return(sun_rotation)


#####################################################################################################################
#####################################################################################################################
#                                                   CODE HERE                                                       #
#####################################################################################################################
#####################################################################################################################


draw_background = {
    'rectangle' : draw_background_rec,
    'reccir' : draw_background_reccir,
    'recround' : draw_background_recround,
    'circle' : draw_background_cir,
    'cirtri' : draw_background_cirtri,
    'square' : draw_background_squ
}


# Change directories so we are where this file is
script_dir = os.path.dirname(os.path.realpath(__file__))



# # Change to the cycles renderer and setup some options
bpy.context.scene.render.engine = 'CYCLES'
scene = bpy.data.scenes['Scene']
scene.cycles.device = 'GPU'
scene.cycles.samples = 256

# Enable the object pass index so we can make our masks
scene.render.layers['RenderLayer'].use_pass_object_index = True
scene.use_nodes = True

# Set resolution, and render at that resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene = bpy.context.scene

scene.update()

#delete_compositor()

compositor_add()



#####################################################################################################################
#####################################################################################################################
#                                                ACTUAL  CODE HERE                                                  #
#####################################################################################################################
#####################################################################################################################

# Used for generating multiple images

directory = "/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Input/"

files = 0

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        files += 1

print('Files to render: {}' .format(files))

files = 0

for filename in os.listdir(directory):
    if filename.endswith(".jpg"): 
        # print(os.path.join(directory, filename))
        files += 1
        print('Rendering file: {}' .format(files))
    else:
        continue




    # TODO somehow split this into the respective functions/ a function itself

    style =          random.choice(config_dir['background']['style'])
    orientation =    random.choice(config_dir['background']['orientation'])
    border_size =    (config_dir['background']['border_size'][1] - config_dir['background']['border_size'][0]) * np.random.random() + config_dir['background']['border_size'][0]
                                    
    thickness =      config_dir['background']['thickness']
    bevel_radius =   (config_dir['background']['bevel_radius'][1] - config_dir['background']['bevel_radius'][0]) * np.random.random() + config_dir['background']['bevel_radius'][0]
                                    
    number_total =   random.randint(config_dir['lights']['number_total'][0], config_dir['lights']['number_total'][1])

    light_choice = np.zeros((5,3))

    for i in range(0, 5):
        if random.choice(config_dir['lights']['light']) == 'red':
            light_choice[i] = (1, 0, 0)

        else:
            light_choice[i] = (0, 1, 0)

    # R, G, B, A
    light_values = np.array([[light_choice[0][0], 
                              light_choice[0][1], 
                              light_choice[0][2], 
                              1],
                             [light_choice[1][0], 
                              light_choice[1][1], 
                              light_choice[1][2], 
                              1],
                             [light_choice[2][0], 
                              light_choice[2][1], 
                              light_choice[2][2], 
                              1],
                             [light_choice[3][0], 
                              light_choice[3][1], 
                              light_choice[3][2], 
                              1],
                             [light_choice[4][0], 
                              light_choice[4][1], 
                              light_choice[4][2], 
                              1]
                            ])


    light_status = np.array([random.choice(config_dir['lights']['light_status']),
                             random.choice(config_dir['lights']['light_status']),
                             random.choice(config_dir['lights']['light_status']),
                             random.choice(config_dir['lights']['light_status']),
                             random.choice(config_dir['lights']['light_status'])
                            ])


    # print(light_status[0] + '  ' + str(int(light_values[0][0])) + '_' + str(int(light_values[0][1])) + '_' + str(int(light_values[0][2])))
    # print(light_status[1] + '  ' + str(int(light_values[1][0])) + '_' + str(int(light_values[1][1])) + '_' + str(int(light_values[1][2])))
    # print(light_status[2] + '  ' + str(int(light_values[2][0])) + '_' + str(int(light_values[2][1])) + '_' + str(int(light_values[2][2])))
    # print(light_status[3] + '  ' + str(int(light_values[3][0])) + '_' + str(int(light_values[3][1])) + '_' + str(int(light_values[3][2])))  
    # print(light_status[4] + '  ' + str(int(light_values[4][0])) + '_' + str(int(light_values[4][1])) + '_' + str(int(light_values[4][2])))  


    light_can_depth =       (config_dir['lights']['light_can_depth'][1] - config_dir['lights']['light_can_depth'][0]) * np.random.random() + config_dir['lights']['light_can_depth'][0]


    light_spacing =         (config_dir['lights']['light_spacing'][1] - config_dir['lights']['light_spacing'][0]) * np.random.random() + config_dir['lights']['light_spacing'][0]


    light_radius =          (config_dir['lights']['light_radius'][1] - config_dir['lights']['light_radius'][0]) * np.random.random() + config_dir['lights']['light_radius'][0]


    light_wall_thickness =  (config_dir['lights']['light_wall_thickness'][1] - config_dir['lights']['light_wall_thickness'][0]) * np.random.random() + config_dir['lights']['light_wall_thickness'][0]


    sign_height =   np.random.random()
    (config_dir['sign_parameters']['height'][0],
                                    config_dir['sign_parameters']['height'][1])


    post_radius =   config_dir['sign_parameters']['radius']

    sign_position = np.array([config_dir['sign_parameters']['position']['x'],
                             config_dir['sign_parameters']['position']['y'],
                             config_dir['sign_parameters']['position']['z']])

    sign_rotation = np.array([config_dir['sign_parameters']['rotation']['x'],
                             config_dir['sign_parameters']['rotation']['y'],
                             config_dir['sign_parameters']['rotation']['z']])

    # Set maximum number of lights for some designs
    if style == 'circle':
        if number_total > 3:
            number_total = 3

    elif style == 'cirtri':
        number_total = 3

    elif style == 'square':
        number_total = 5

    else:
        number_total = number_total

    print('Number Total: {}' .format(number_total))


    object_number = 0    #Ranom Variable (Number of objects)
    object_name = [0]
    fno = 1

    output_data = {
            'img_name' : '',
            'background': {
                'style' : style,
                'orientation' : orientation,
                'border_size' : border_size,
                'thickness' : thickness,
                'bevel_radius' : bevel_radius,
            },
            'lights' : {
                'number_total' : number_total,
                'light' : light_values.tolist(),
                'light_depth' : light_can_depth,
                'light_spacing' : light_spacing,
                'light_radius' : light_radius,
                'light_wall_thickness' : light_wall_thickness
            },
            'sign_parameters' : {
                'height_total' : sign_height,
                'radius' : post_radius,
                'sign_height' : '',
                'sign_width' : '',
                'position' : sign_position.tolist(),
                'rotation' : sign_rotation.tolist(),
            },
            'frame_data' : {
            }
        }










    # Delete old objects 
    for object in bpy.data.objects:
        bpy.data.objects.remove(object)
    
    delete_materials()

    # TODO delete objects at the start


    frame_number = filename.lstrip('frame')
    frame_number = frame_number.rstrip('.jpg')
    frame_number = int(frame_number)

    #frame_number = 3150 # TODO temporary

    background_img = load_img(frame_number)

    output_data['img_name'] = 'frame' + str(frame_number) + '.jpg'

    img_number = frame_number #get image number from end of string

    # Read in meta data
    with open(os.path.join(Input_meta_file)) as json_data:
        data = json.load(json_data)
        for x in data:
            if x['frame_number'] == img_number:
                frame_data = x
                break
        # print(frame_data['frame_number'])




    # For each light, create the material required
    for i in range(0, number_total):

        if light_status[i] == 'on':
            light_glass_material(light_values,
                                 i,
                                 2, 
                                 1, 
                                 5, 
                                 1)

        elif light_status[i] == 'off':
            light_glass_off_material(light_values, i)

    # Create the sign material
    PBR_Dielectric(config_dir['background']['sign']['roughness_s'], 
                   config_dir['background']['sign']['reflection_s'],
                   config_dir['background']['sign']['diffuse_s'], 
                   config_dir['background']['sign']['glossy_s'], 
                   config_dir['background']['sign']['noise_s'], 
                   'PBR_Dielectric'
                   )

    # Create the post material
    PBR_Dielectric(config_dir['background']['post']['roughness_p'], 
                   config_dir['background']['post']['reflection_p'], 
                   config_dir['background']['post']['diffuse_p'], 
                   config_dir['background']['post']['glossy_p'], 
                   config_dir['background']['post']['noise_p'],
                   'PBR_Dielectric_post'
                   )


    objects = bpy.data.objects

    # For each light create it and move to required position
    for x_light in range (0, (number_total - 1)):
        light_status_var = light_status[x_light]

        if light_status_var == 'blank':
            #print(light_status + str(x_light))

            blank_obj = draw_blank(object_number,
                                   light_radius,
                                   light_spacing,
                                   light_wall_thickness,
                                   light_can_depth
                                   )

            blank_obj.name = 'blank' + str(x_light)
            
            mat = bpy.data.materials['PBR_Dielectric']
            blank_obj.data.materials.append(mat)

            blank_obj = move_can(style,
                                 light_radius,
                                 light_spacing,
                                 number_total,
                                 orientation,
                                 x_light,
                                 light_can_depth,
                                 light_wall_thickness,
                                 blank_obj,
                                 light_status_var)

        else:

            bpy.ops.object.select_all(action='DESELECT')

            # print(light_status + str(x_light))
            # print(str(light_values[x_light][0]) + '_' 
                # + str(light_values[x_light][1]) + '_' 
                # + str(light_values[x_light][2]))        
            
            can_obj = draw_can(object_number,
                               light_radius,
                               light_spacing,
                               light_wall_thickness,
                               light_can_depth
                               )

            can_obj.name = 'can' + str(x_light)
            
            mat = bpy.data.materials['PBR_Dielectric']
            can_obj.data.materials.append(mat)


            can_obj = move_can(style,
                               light_radius,
                               light_spacing,
                               number_total,
                               orientation,
                               x_light,
                               light_can_depth,
                               light_wall_thickness,
                               can_obj,
                               0)

            light_obj = draw_light(object_number,
                                   light_radius,
                                   light_spacing,
                                   light_wall_thickness,
                                   light_can_depth
                                   )

            light_obj.name = 'light' + str(x_light)

            if light_status_var == 'on':
                mat = bpy.data.materials['light_glass_material_' 
                                         + str(int(light_values[x_light][0])) + '_' 
                                         + str(int(light_values[x_light][1])) + '_' 
                                         + str(int(light_values[x_light][2]))]                    
            else:
                mat = bpy.data.materials['light_glass_off_material_' 
                                         + str(int(light_values[x_light][0])) + '_' 
                                         + str(int(light_values[x_light][1])) + '_' 
                                         + str(int(light_values[x_light][2]))]

            light_obj.data.materials.append(mat)

            light_obj = move_can(style,
                                 light_radius,
                                 light_spacing,
                                 number_total,
                                 orientation,
                                 x_light,
                                 light_can_depth,
                                 light_wall_thickness,
                                 light_obj,
                                 light_status_var)


    # Make background sign
    background_obj = draw_background[style](light_radius, 
                                            thickness,
                                            border_size,
                                            number_total,
                                            object_number,
                                            light_spacing,
                                            orientation,
                                            bevel_radius
                                            )


    # Make post
    post_obj = draw_post(object_number,
                         number_total,
                         light_radius,
                         border_size,
                         light_spacing)

    mat = bpy.data.materials['PBR_Dielectric_post']
    post_obj.data.materials.append(mat)

    # Combine all objects
    for x in objects:
        bpy.data.objects[x.name].select = True
    bpy.ops.object.join()

    # Group lights with sign
    s = 'Signal'
    for x in bpy.data.objects:
        if s.find('Signal') != -1:
           x.select =True

    for x in objects:
        bpy.data.objects[x.name].select = True

    bpy.data.groups.new('Aspect')
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    bpy.context.object.name = "Aspect"
    obj = bpy.data.objects.get('Aspect')


    # Move sign to required position
    obj.location = sign_position
    obj.rotation_euler.x = sign_rotation[0]
    obj.rotation_euler.y = sign_rotation[1]
    obj.rotation_euler.z = sign_rotation[2] # 8 deg

    # TODO fix stencil
    obj.pass_index = 1


    #####################################################################################################################
    #####################################################################################################################
    #                                    SHADOW CATCHER    CAMERA    LAMPS    COMPOSITOR                                #
    #####################################################################################################################
    #####################################################################################################################


    # Shadow catcher plane
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, -3))
    bpy.context.object.scale=(5, 5, 1)
    bpy.context.object.cycles.is_shadow_catcher = True


    location_values = (0.94495, 14.53555, 0.79661)
    angle_values = (1.424895, -0.002425, 3.103351)

    camera_add(location_values, angle_values, config_dir['camera_parameters'])

    bpy.context.scene.camera = bpy.data.objects["Camera"]

    zenith, azimuth = sunpos(frame_data['utc_timestamp'], 
                            (frame_data['frame_position_lat'] * (math.pi / 180)), 
                            (frame_data['frame_position_long'] * (math.pi / 180))
                            )

    sun_rotation = sun_location(zenith, 
                                azimuth,
                                (frame_data['frame_heading'] * (math.pi / 180))
                                )

    lamp_add(object_number, 
             object_name, 
             sun_rotation)

    compositor_set(frame_number,
                   background_img)

    #####################################################################################################################
    #####################################################################################################################
    #                                              INFORMATION SAVING    RENDER                                         #
    #####################################################################################################################
    #####################################################################################################################

    # Render the image
    bpy.context.scene.frame_set(fno)
    bpy.ops.render.render(write_still=True)

    output_data['frame_data'] = frame_data

    with open(os.path.join(Output_meta_file,
                           'meta{:04d}.yaml'.format(frame_number)),
                           'w'
                           ) as md:
        md.write(yaml.dump(output_data, indent=4, default_flow_style=False))
    fno += 1

print('Finished Rendering :)')





# delete materials
# delete compositor
# delete objects
# create compositor
# create my 8 materials
# for each frame
    # read json file
    # decide on number of posts
    # for each post
        # decide on number of aspects
        # for each aspect
            # decide on number of lights
            # make background
            # decide which light is on
            # for each light
                # create it
                # apply material
                # add lamp
                # move it relative to background
            # join aspect parts
            # give each aspect a unique pass index
            # add meta data to meta file
        # group post and aspects
        # move to position
        # ungroup
    # calculate sun location
    # add sun
    # add camera
    # render
    # save meta file