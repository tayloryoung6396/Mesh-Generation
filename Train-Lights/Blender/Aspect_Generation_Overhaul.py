import bpy
import numpy as np
import math
import os
import random
import yaml
import json

Input_meta_file  = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/VIRB0045-8.json'
Output_meta_file = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Output-meta/'
Input_img_file   = '/home/nubots/Code/Mesh-Generation/Train-Lights/Blender/Input/'

config_dir = {
    'materials' : {
        'aspect' : {
            'red' : (1, 0, 0),
            'yellow' : (1, 1, 0),
            'green' : (0, 1, 0)
        },
        'sign' : {
            'roughness' : 0.05,
            'reflection' : 0.6,
            'diffuse' : (0, 0, 0),
            'glossy' : (0.009, 0.010, 0.012),
            'noise' : (2, 1, 6)
        },
        'post' : {
            'roughness' : 0.3,
            'reflection' : 0.5,
            'diffuse' : (0, 0, 0),
            'glossy' : (0.039, 0.045, 0.056),
            'noise' : (10, 1, 0)
        }
    },
    'sign' : {
        'parameters' : {
            'border_size' : (0.1),
            'thickness' : 0.01,
            'bevel_radius' : (0.1),
            'light_depth' : (0.03),
            'light_spacing' : (0.01),
            'light_radius' : (0.1),
            'light_wall_thickness' : (0.01),
            'post_radius' : 0.05,
            'z_rotation_min' : -10,
            'z_rotation_max' : 10,
            'min_aspect_height' : 1.0,
            'post_height_min' : 1.5,
            'post_height_max' :2.5,
            'far_left' : -2,
            'left' : -0.5,
            'right' : 0.5,
            'far_right' : -2
        },
        'style_options' : ('rectangle', 'reccir'),
        'style_options_parameters' : {
            'rectangle' :{
                'lights_min' : 1,
                'lights_max' : 3,
                '1' : ('red', 'red', 'red'),
                '2' : ('green', 'red', 'red'),
                '3' : ('green', 'yellow', 'red')
            },
            'reccir' : {
                'lights_min' : 1,
                'lights_max' : 3,
                '1' : ('red','red', 'red'),
                '2' : ('green', 'red', 'red'),
                '3' : ('green', 'yellow', 'red')
            }
        },
        # 'post_height' : 
        'posts_min' : 1,
        'posts_max' : 1,
        'aspects_min' : 2,
        'aspects_max' : 2,
        # 'number_posts' :
        # 'post1' : {                             # These lines not needed, only for visual aid
        #     'position' : {                      # These lines not needed, only for visual aid
        #         'rl' :                          # These lines not needed, only for visual aid
        #         'x' :                           # These lines not needed, only for visual aid
        #         'y' :                           # These lines not needed, only for visual aid
        #         'z' :                           # These lines not needed, only for visual aid
        #     }
        #     'number_aspects' :                  # These lines not needed, only for visual aid
        #     'aspect1' : {                       # These lines not needed, only for visual aid
        #         'style' :                       # These lines not needed, only for visual aid
        #         'background' : {
        #             #Stuff
        #         }
        #         'number_lights' :               # These lines not needed, only for visual aid
        #         'light1' : {                    # These lines not needed, only for visual aid
        #             'status' :                  # These lines not needed, only for visual aid
        #         }                               # These lines not needed, only for visual aid
        #         'position' : {                  # These lines not needed, only for visual aid
        #         'x' :                           # These lines not needed, only for visual aid
        #         'y' :                           # These lines not needed, only for visual aid
        #         'z' :                           # These lines not needed, only for visual aid
        #         }                               # These lines not needed, only for visual aid
        #     }
        #     'position' : {                      # These lines not needed, only for visual aid
        #         'x' :                           # These lines not needed, only for visual aid
        #         'y' :                           # These lines not needed, only for visual aid
        #         'z' :                           # These lines not needed, only for visual aid
        #     },
        #     'rotation' : {                      # These lines not needed, only for visual aid
        #         'x' :                           # These lines not needed, only for visual aid
        #         'y' :                           # These lines not needed, only for visual aid
        #         'z' :                           # These lines not needed, only for visual aid
        #     }                                   # These lines not needed, only for visual aid
        # }                                       # These lines not needed, only for visual aid
    },
    'colour' : {
        'red' : (1, 0, 0),
        'yellow' : (1, 1, 0),
        'green' : (0, 1, 0)
    },
    'camera_parameters' : {
            'type' : 'PERSP', # PANO, PERSP
            'FOV' : 2.37365,
            'lens' : 35, # mm
            'sensor_width' : 32 # mm
    }
}

object_number = 0    #Ranom Variable (Number of objects)
object_name = [0]
fno = 1

# Remove previous materials
def delete_materials():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

# Delete old objects
def delete_objects():
    for object in bpy.data.objects:
        bpy.data.objects.remove(object)

# Remove previous compositor
def delete_compositor():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

#####################################################################################################################
#####################################################################################################################
#                                                  BACKGROUNDS                                                      #
#####################################################################################################################
#####################################################################################################################

def draw_background_rec(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size
    vertical_origin = (height / 2) - (border_size + light_radius)

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

    aspect['background'] = {}
    aspect['background']['sign_height'] = height
    aspect['background']['sign_width'] = width

    return obj

def draw_background_cir(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

    # Calculate width and height of sign background
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size 
    # Calculate vertical position for background
    vertical_origin = (height / 2) - (border_size + light_radius)

    location_values = (0, -background_thickness, vertical_origin)

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

    aspect['background'] = {}
    aspect['background']['sign_height'] = height
    aspect['background']['sign_width'] = height

    return obj

def draw_background_cirtri(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

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

    aspect['background'] = {}
    aspect['background']['sign_height'] = height
    aspect['background']['sign_width'] = height

    return obj

def draw_background_reccir(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

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
    # mod_bool = obj1.modifiers.new('my_bool_mod_2', 'BOOLEAN')
    # mod_bool.operation = 'UNION'
    # mod_bool.object = obj2
    # bpy.context.scene.objects.active = obj1
    # res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod_2')

    bpy.ops.object.select_all(action='DESELECT')
    obj1.select = True
    obj2.select = True
    bpy.ops.object.join()
    bpy.context.object.name = ('background_obj')
    obj1 = bpy.data.objects.get('background_obj')

    # TODO should be deleting this object and combining properly
    # obj2.select = True
    # bpy.ops.object.delete()
    # object_name.remove(object_name[object_number])
    # object_number = object_number - 1  

    # mat = bpy.data.materials['PBR_Dielectric']
    # obj2.data.materials.append(mat)

    # Add material to sign   
    mat = bpy.data.materials['PBR_Dielectric']
    obj1.data.materials.append(mat)

    aspect['background'] = {}
    aspect['background']['sign_height'] = height + height_circle
    aspect['background']['sign_width']= width

    return obj1

def draw_background_recround(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

    # Calculate width and height of sign background
    width = 2 * light_radius + 2 * border_size
    height = (no_lights * light_radius * 2) + ((no_lights - 1) * light_spacing) + border_size + border_size - 2 * bevel_radius

    vertical_origin = ((height + 2 * bevel_radius) / 2) - (border_size + light_radius)

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

    aspect['background'] = {}
    aspect['background']['sign_height'] = height + bevel_radius
    aspect['background']['sign_width'] = width

    return obj

def draw_background_squ(aspect, sign, object_number):
    no_lights = aspect['number_lights']
    border_size = sign['parameters']['border_size']
    background_thickness = sign['parameters']['thickness']
    bevel_radius = sign['parameters']['bevel_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_radius = sign['parameters']['light_radius']

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

    aspect['background'] = {}
    aspect['background']['sign_height'] = width
    aspect['background']['sign_width'] = width

    return obj

#####################################################################################################################
#####################################################################################################################
#                                                    LIGHTS                                                         #
#####################################################################################################################
#####################################################################################################################

def draw_can(object_number):

    light_radius = sign['parameters']['light_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_wall_thickness = sign['parameters']['light_wall_thickness']
    light_depth = sign['parameters']['light_depth']

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
                   light_spacing):

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


def draw_light(object_number):

    light_radius = sign['parameters']['light_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_wall_thickness = sign['parameters']['light_wall_thickness']
    light_depth = sign['parameters']['light_depth']

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

def draw_blank(object_number):

    light_radius = sign['parameters']['light_radius']
    light_spacing = sign['parameters']['light_spacing']
    light_wall_thickness = sign['parameters']['light_wall_thickness']
    light_depth = sign['parameters']['light_depth']

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]
    
    obj1.scale=(light_radius - light_wall_thickness, 
                light_radius - light_wall_thickness,
                light_wall_thickness)

    obj1.rotation_euler.x = -1.57
    
    obj1.location=(0, light_wall_thickness, 0)

    return obj1

def move_can(sign, post, aspect, light, obj, x_lights):

    style  = aspect['style']
    light_radius  = sign['parameters']['light_radius']
    light_spacing  = sign['parameters']['light_spacing']
    number_total  = aspect['number_lights']
    light_depth  = sign['parameters']['light_depth']
    light_wall_thickness  = sign['parameters']['light_wall_thickness']
    light_status  = light['status']

    # Orientation flips y and z location values
    # Independent of can type

    if style == 'reccir':
        center = (x_lights) * ((2 * light_radius) + light_spacing)
        obj.location=(0, obj.location[1], center)

    elif style == 'square':

        vertical_offset = (math.sqrt((2 * light_radius + light_spacing) * (2 * light_radius + light_spacing) / 2))

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
        obj.location=(0, obj.location[1], center)

    return obj

def draw_post(object_number, sign):

    light_radius = sign['parameters']['light_radius']
    border_size = sign['parameters']['border_size']
    light_spacing = sign['parameters']['light_spacing']
    post_height = sign['parameters']['post_height']
    post_radius = sign['parameters']['post_radius']

    objects = bpy.data.objects

    object_number = object_number + 1
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))

    object_name.append(bpy.context.active_object.name)
    obj1 = objects[object_name[-1]]

    obj1.scale=(post_radius, 
                post_radius,
                post_height/2)

    obj1.location=(0, 
                   -0.075,
                   (post_height/2)# TODO check this equation # origin bottom face of post, center
                   )

    return(obj1)

#####################################################################################################################
#####################################################################################################################
#                                                   MATERIALS                                                       #
#####################################################################################################################
#####################################################################################################################

def light_glass_material(colour,
                         wave_scale, 
                         wave_distortion, 
                         wave_detail, 
                         wave_detail_scale):

    glass_value = (colour[0], 
                   colour[1], 
                   colour[2],
                   1)

    diffuse_value = (colour[0] * 0.6 / 30, 
                     colour[1] * 0.6 / 30, 
                     colour[2] * 0.6 / 30,
                     1)

    mat = bpy.data.materials.get('light_glass_material_' 
                                + str(int(colour[0])) + '_' 
                                + str(int(colour[1])) + '_'
                                + str(int(colour[2])))

    # TODO solve double creation of nodes

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_material_'
                                    + str(int(colour[0])) + '_' 
                                    + str(int(colour[1])) + '_'
                                    + str(int(colour[2])))
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


def light_glass_off_material(colour):

    glass_value = (colour[0] * 0.1, 
                   colour[1] * 0.1, 
                   colour[2] * 0.1,
                   1)

    diffuse_value = (colour[0] * 0.05 * 0.01, 
                     colour[1] * 0.05 * 0.01, 
                     colour[2] * 0.05 * 0.01,
                     1)

    translucent_value = (colour[0] * 0.05, 
                         colour[1] * 0.05, 
                         colour[2] * 0.05,
                         1)

    mat = bpy.data.materials.get('light_glass_off_material_' 
                                 + str(int(colour[0])) + '_' 
                                 + str(int(colour[1])) + '_'
                                 + str(int(colour[2])))

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new('light_glass_off_material_' 
                                     + str(int(colour[0])) + '_' 
                                     + str(int(colour[1])) + '_'
                                     + str(int(colour[2])))
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

def PBR_Dielectric(material, mat_name):

    mat = bpy.data.materials.get(mat_name)

    #if it doesnt exist, create it.
    if mat is None:
        # create material and assign
        mat = bpy.data.materials.new(mat_name)
    else:
        return

    roughness         = material['roughness']
    reflection        = material['reflection']
    diffuse_values    = material['diffuse']
    glossy_values     = material['glossy']
    noise_values      = material['noise']

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

#####################################################################################################################
#####################################################################################################################
#                                                   COMPOSITE                                                       #
#####################################################################################################################
#####################################################################################################################

def compositor_add():
    
    # Link up our output layers to file output nodes
    nodes = scene.node_tree.nodes

    render_layers = nodes.new(type="CompositorNodeRLayers")
    render_layers.name = render_layers.label = 'render_layers'
    background_layers = nodes.new(type="CompositorNodeImage")
    background_layers.name = background_layers.label = 'background_layers'
    mix = nodes.new(type="CompositorNodeMixRGB")
    mix.name = mix.label = 'mix'


    mask1 = nodes.new(type="CompositorNodeIDMask")
    mask1.name = mask1.label = 'mask1'
    mask1.index = 1

    mask2 = nodes.new(type="CompositorNodeIDMask")
    mask2.name = mask2.label = 'mask2'
    mask2.index = 2

    mask3 = nodes.new(type="CompositorNodeIDMask")
    mask3.name = mask3.label = 'mask3'
    mask3.index = 3

    mask4 = nodes.new(type="CompositorNodeIDMask")
    mask4.name = mask4.label = 'mask4'
    mask4.index = 4

    mask5 = nodes.new(type="CompositorNodeIDMask")
    mask5.name = mask5.label = 'mask5'
    mask5.index = 5

    mask6 = nodes.new(type="CompositorNodeIDMask")
    mask6.name = mask6.label = 'mask6'
    mask6.index = 6

    mask7 = nodes.new(type="CompositorNodeIDMask")
    mask7.name = mask7.label = 'mask7'
    mask7.index = 7

    mask8 = nodes.new(type="CompositorNodeIDMask")
    mask8.name = mask8.label = 'mask8'
    mask8.index = 8

    mix11 = nodes.new(type="CompositorNodeMixRGB")
    mix11.name = mix11.label = 'mix11'

    mix12 = nodes.new(type="CompositorNodeMixRGB")
    mix12.name = mix12.label = 'mix12'

    mix13 = nodes.new(type="CompositorNodeMixRGB")
    mix13.name = mix13.label = 'mix13'

    mix14 = nodes.new(type="CompositorNodeMixRGB")
    mix14.name = mix14.label = 'mix14'

    mix21 = nodes.new(type="CompositorNodeMixRGB")
    mix21.name = mix21.label = 'mix21'

    mix22 = nodes.new(type="CompositorNodeMixRGB")
    mix22.name = mix22.label = 'mix22'

    mix31 = nodes.new(type="CompositorNodeMixRGB")
    mix31.name = mix31.label = 'mix31'

    indexob_file = nodes.new('CompositorNodeOutputFile')
    indexob_file.name = indexob_file.label = 'indexob_file'
    image_file = nodes.new('CompositorNodeOutputFile')
    image_file.name = image_file.label = 'image_file'

    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask1.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask2.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask3.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask4.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask5.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask6.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask7.inputs[0])
    scene.node_tree.links.new(render_layers.outputs['IndexOB'], mask8.inputs[0])

    scene.node_tree.links.new(mask1.outputs[0], mix11.inputs[1])
    scene.node_tree.links.new(mask2.outputs[0], mix11.inputs[2])
    scene.node_tree.links.new(mask3.outputs[0], mix12.inputs[1])
    scene.node_tree.links.new(mask4.outputs[0], mix12.inputs[2])
    scene.node_tree.links.new(mask5.outputs[0], mix13.inputs[1])
    scene.node_tree.links.new(mask6.outputs[0], mix13.inputs[2])
    scene.node_tree.links.new(mask7.outputs[0], mix14.inputs[1])
    scene.node_tree.links.new(mask8.outputs[0], mix14.inputs[2])

    scene.node_tree.links.new(mix11.outputs[0], mix21.inputs[1])
    scene.node_tree.links.new(mix12.outputs[0], mix21.inputs[2])
    scene.node_tree.links.new(mix13.outputs[0], mix22.inputs[1])
    scene.node_tree.links.new(mix14.outputs[0], mix22.inputs[2])

    scene.node_tree.links.new(mix21.outputs[0], mix31.inputs[1])
    scene.node_tree.links.new(mix22.outputs[0], mix31.inputs[2])

    scene.node_tree.links.new(mix31.outputs[0], indexob_file.inputs['Image'])

    scene.node_tree.links.new(render_layers.outputs['Image'], mix.inputs[2])
    scene.node_tree.links.new(background_layers.outputs['Image'], mix.inputs[1])
    scene.node_tree.links.new(render_layers.outputs['Alpha'], mix.inputs[0])
    scene.node_tree.links.new(mix.outputs[0], image_file.inputs['Image'])

    composite = nodes.new(type='CompositorNodeComposite')
    scene.node_tree.links.new(mix.outputs[0], composite.inputs[0])


def compositor_set(frame_number, background_img):
    
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
             sun_rotation):

    objects = bpy.data.objects

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
    light_values = (0.426 * light_values[0], 
                    0.426 * light_values[1], 
                    0.426 * light_values[2], 1)

    objects = bpy.data.objects

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

    return(obj)

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
#                                             POST/ASPECT LOCATION                                                  #
#####################################################################################################################
#####################################################################################################################

def calculate_post_location(sign, post_number):
    # TODO
    post = sign['post' + str(post_number)]
    rl_position = post['position']['rl']
    # Forwards, Backwards (Lower weighting)
    direction_choice = ['forwards'] * 80 + ['backwards'] * 20
    post['direction'] = random.choice(direction_choice) 

    if post['direction'] == 'forwards':
        direction = 0
        
    else:
        direction = 180
    # Along some line
    # TODO figure out some eqn and how to flip it and move left and right
    # TODO figure out what changes when i menuvour a post
    # Include some half cut-off the screen (train going past it)
    min_x = sign['parameters'][rl_position]
    max_x = min_x * 1.5

    post['position'] = {}
    post['position']['x'] = (max_x - min_x * np.random.random() + min_x) # This is the post and aspectss combined, not only the post TODO
    post['position']['y'] = -(10 - 1 * np.random.random() + 1) # This is the post and aspectss combined, not only the post TODO
    post['position']['z'] = 0 # This is the post and aspectss combined, not only the post TODO
    # TODO somewhere i need to acount for moving the sign up so the bottom of the post is at ground height (maybe?)

    # Vary angle along z axis by +- 5 degrees of zero position both for forwards and backwards
    post['rotation'] = {}
    post['rotation']['x'] = 0
    post['rotation']['y'] = 0
    post['rotation']['z'] = random.randint(sign['parameters']['z_rotation_min'],
                                        sign['parameters']['z_rotation_max']) + direction

    position = (post['position']['x'], post['position']['y'], post['position']['z'])
    rotation = (post['rotation']['x'], post['rotation']['y'], post['rotation']['z'])

    return(position, rotation)


def calculate_aspect_location(sign, post, aspect_number):

    post_height = sign['parameters']['post_height']

    if aspect_number == 0:
        aspect0 = post['aspect0']
        sign_height = aspect0['background']['sign_height']
        light_radius = sign['parameters']['light_radius']
        border_size = sign['parameters']['border_size']

        vertical_difference = post_height - light_radius - border_size

        aspect0['position'] = {}
        aspect0['position']['x'] = 0
        aspect0['position']['y'] = 0
        aspect0['position']['z'] = vertical_difference

        aspect0['rotation'] = {}
        aspect0['rotation']['x'] = 0
        aspect0['rotation']['y'] = 0
        aspect0['rotation']['z'] = 0

        position = (aspect0['position']['x'], aspect0['position']['y'], aspect0['position']['z'])
        rotation = (aspect0['rotation']['x'], aspect0['rotation']['y'], aspect0['rotation']['z'])

        return(position, rotation)

    #  account for different location of post
    elif aspect_number == 1:
        aspect1 = post['aspect1']
        sign_height = aspect1['background']['sign_height']
        light_radius = sign['parameters']['light_radius']
        border_size = sign['parameters']['border_size']

        # move it down by the range(height above the bottom light of this aspect 
        # + the amount below the bottom light of the top aspect
        # + some minimum offset, minimum sign position)

        amount_overlap = sign_height + light_radius + border_size # some small gap minimum
        min_aspect_height = sign['parameters']['min_aspect_height'] + amount_overlap

        aspect0 = post['aspect0']
        sign_height0 = aspect0['background']['sign_height']
        top_limit = post_height - sign_height0 - light_radius - border_size - 0.1         

        # do some random position between amount_overlap and minimum_height
        rand_aspect_height = (top_limit - min_aspect_height * np.random.random() + min_aspect_height)

        # update location values of aspect
        aspect1['position'] = {}
        aspect1['position']['x'] = 0
        aspect1['position']['y'] = 0
        aspect1['position']['z'] = rand_aspect_height

        aspect1['rotation'] = {}
        aspect1['rotation']['x'] = 0
        aspect1['rotation']['y'] = 0
        aspect1['rotation']['z'] = 0

        position = (aspect1['position']['x'], aspect1['position']['y'], aspect1['position']['z'])
        rotation = (aspect1['rotation']['x'], aspect1['rotation']['y'], aspect1['rotation']['z'])

        return(position, rotation)

    else:
        print('Too many aspects')

#####################################################################################################################
#####################################################################################################################
#                                                   CODE HERE                                                       #
#####################################################################################################################
#####################################################################################################################

delete_materials()

#delete_compositor()

#delete_objects()

# Make materials
aspect_material = config_dir['materials']['aspect']
for material in aspect_material:

    light_glass_material(aspect_material[material], 2, 1, 5, 1)
    light_glass_off_material(aspect_material[material])

# Create the sign material
sign_material = config_dir['materials']['sign']
PBR_Dielectric(sign_material, 
               'PBR_Dielectric'
               )

# Create the post material
post_material = config_dir['materials']['post']
PBR_Dielectric(post_material,
               'PBR_Dielectric_post'
               )

draw_background = {
    'rectangle' : draw_background_rec,
    'reccir' : draw_background_reccir,
    'recround' : draw_background_recround,
    'circle' : draw_background_cir,
    'cirtri' : draw_background_cirtri,
    'square' : draw_background_squ
}

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

# Calculate how many files we have
files = 0
for filename in os.listdir(Input_img_file):
    if filename.endswith(".jpg"):
        files += 1
print('Files to render: {}' .format(files))

#####################################################################################################################
#####################################################################################################################
#                                                     FRAMES                                                        #
#####################################################################################################################
#####################################################################################################################

files = 0
for filename in os.listdir(Input_img_file):
    if filename.endswith(".jpg"):
        files += 1
        print('Rendering file: {}' .format(files))
        config_dir['img_name'] = filename
    else:
        continue

    #delete_materials()

    delete_objects()

    # Find current frame number
    frame_number = filename.lstrip('frame')
    frame_number = frame_number.rstrip('.jpg')
    frame_number = int(frame_number)

    # Read in meta data of frame number
    with open(os.path.join(Input_meta_file)) as json_data:
        data = json.load(json_data)
        for x in data:
            if x['frame_number'] == frame_number:
                frame_data = x
                break

    sign = config_dir['sign']

    # Choose random number of posts for frame
    sign['number_posts'] = random.randint(sign['posts_min'], sign['posts_max'])

    # Vary between 4 positions:
    a = 1 # Far Left (Lower weighting)
    b = 1 # Left
    c = 1 # Right
    d = 1 # Far Right (Lower weighting)

    post_height_min = sign['parameters']['post_height_min']
    post_height_max = sign['parameters']['post_height_max']
    sign['parameters']['post_height'] = (post_height_max - post_height_min * np.random.random() + post_height_min) # Calculate outside of loop, so all are the same in  a frame

    pass_count = 0 # used for pass index allowing each aspect to be an individual colour

    for post_number in range(0, sign['number_posts']):
        
        bpy.ops.object.select_all(action='DESELECT')

        post_obj = draw_post(object_number, sign)
        post_obj.name = 'post' + str(post_number)

        # Create post group for each post
        ###################################################################################################################################
        bpy.data.groups.new('Post_group' + str(post_number))
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        bpy.context.object.name = "Post" + str(post_number)
        post_group = bpy.data.groups.get('Post_group' + str(post_number))
        ###################################################################################################################################


        sign['post' + str(post_number)] = {}
        post = sign['post' + str(post_number)]

        post['number_aspects'] = random.randint(sign['aspects_min'], sign['aspects_max'])
        
        # Make it less likely for a post to be positioned in the same rl twice in a frame
        rl_choice = ['far_left', 'left', 'right', 'far_right']
        rl_weight = [(10 / a), (40 / b), (40 / c), (10 / d)]
        rl_total = rl_weight[0] + rl_weight[1] + rl_weight[2] + rl_weight[3]
        rl_weight = [(10 / a) / rl_total, (40 / b) / rl_total, (40 / c) / rl_total, (10 / d) / rl_total]
        #rl_position = random.choice(rl_choice)
        #rl_position = random.choice(rl_choice, rl_weight)
        rl_position = np.random.choice(rl_choice, 1, p=rl_weight)
        if rl_position == 'far_left':
            rl_position = 'far_left'
            a += 1
        if rl_position == 'left':
            rl_position = 'left'
            b += 1
        if rl_position == 'right':
            rl_position = 'right'
            c += 1
        if rl_position == 'far_right':
            rl_position = 'far_right'
            d += 1
        sign['post' + str(post_number)]['position'] = {}
        sign['post' + str(post_number)]['position']['rl'] = rl_position

        for aspect_number in range(0, post['number_aspects']):

            post['aspect' + str(aspect_number)] = {}
            aspect = post['aspect' + str(aspect_number)]

            # Random style
            aspect['style'] = random.choice(sign['style_options'])
            aspect['number_lights'] = random.randint(sign['style_options_parameters'][aspect['style']]['lights_min'], 
                                                     sign['style_options_parameters'][aspect['style']]['lights_max'])

            bpy.ops.object.select_all(action='DESELECT')

            background_obj = draw_background[aspect['style']](aspect, sign, object_number)

            # Create aspect group for each aspect on post
            ###################################################################################################################################
            # bpy.data.groups.new('Aspect_group' + str(aspect_number))
            # bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

            # bpy.context.object.name = ('Aspect' + str(aspect_number))
            # aspect_group = bpy.data.groups.get('Aspect_group' + str(aspect_number))
            ################################################################################################################################### 


            light_on = random.randint(sign['style_options_parameters'][aspect['style']]['lights_min'], 
                                      aspect['number_lights'])

            pass_count = pass_count + 1

            for light_number in range(0, aspect['number_lights']):

                aspect['light' + str(light_number)] = {}

                if light_number == light_on:
                    aspect['light' + str(light_number)]['status'] = 'on'
                else:
                    aspect['light' + str(light_number)]['status'] = 'off'

                light = aspect['light' + str(light_number)]

                if light['status'] == 'blank':

                    # If the light is blank, draw the object, add material, move to position, add to aspect group
                    blank_obj = draw_blank(object_number)
                    blank_obj.name = 'blank' + str(post_number) + str(aspect_number) + str(light_number)
                    
                    mat = bpy.data.materials['PBR_Dielectric']
                    blank_obj.data.materials.append(mat)

                    blank_obj = move_can(sign, post, aspect, light, blank_obj, light_number)
                    light['blank' + str(light_number)] = str(blank_obj.name)

                    bpy.ops.object.select_all(action='DESELECT')
                    if light_number == 0:
                        background_obj.select = True
                    else:
                        aspect_group = bpy.data.objects.get('Aspect_group' + str(aspect_number))
                        aspect_group.select = True
                    blank_obj.select = True
                    bpy.ops.object.join()
                    bpy.context.object.name = ('Aspect_group' + str(aspect_number))
                    aspect_group = bpy.data.objects.get('Aspect_group' + str(aspect_number))

                else:
                    # If the light is on or off, draw the object, add material, move to position, add to aspect group
                    can_obj = draw_can(object_number)
                    can_obj.name = 'can' + str(post_number) + str(aspect_number) + str(light_number)
                    
                    mat = bpy.data.materials['PBR_Dielectric']
                    can_obj.data.materials.append(mat)

                    can_obj = move_can(sign, post, aspect, light, can_obj, light_number)


                    bpy.ops.object.select_all(action='DESELECT')
                    if light_number == 0:
                        background_obj.select = True
                    else:
                        aspect_group = bpy.data.objects.get('Aspect_group' + str(aspect_number))
                        aspect_group.select = True
                    can_obj.select = True
                    bpy.ops.object.join()
                    bpy.context.object.name = ('Aspect_group' + str(aspect_number))
                    aspect_group = bpy.data.objects.get('Aspect_group' + str(aspect_number))



                    light_obj = draw_light(object_number)
                    light_obj.name = 'light' + str(post_number) + str(aspect_number) + str(light_number)
                    light_obj = move_can(sign, post, aspect, light, light_obj, light_number)

                    colour = sign['style_options_parameters'][aspect['style']][str(aspect['number_lights'])]
                    colour = colour[light_number]
                    rgb = config_dir['colour'][colour]
                    light_values = (rgb[0], rgb[1], rgb[2])

                    if light['status'] == 'on':
                        mat_name = 'light_glass_material_' + str(light_values[0]) + '_' + str(light_values[1]) + '_' + str(light_values[2])
                        mat = bpy.data.materials[mat_name]                

                    else:
                        mat_name = 'light_glass_material_' + str(light_values[0]) + '_' + str(light_values[1]) + '_' + str(light_values[2])
                        mat = bpy.data.materials[mat_name]

                    light_obj.data.materials.append(mat)

                    light_radius  = sign['parameters']['light_radius']
                    light_spacing  = sign['parameters']['light_spacing']
                    light_wall_thickness  = sign['parameters']['light_wall_thickness']
                    light_status  = light['status']

                    if light_status == 'o':
                        lamp_obj = add_signal_lamp(light_number, light_values, light_wall_thickness, light_radius, light_spacing, light_obj.location)



                    #print('here 1a' + str(post_number) + str(aspect_number))
                    bpy.ops.object.select_all(action='DESELECT')
                    aspect_group.select = True
                    light_obj.select = True
                    bpy.ops.object.join()
                    bpy.context.object.name = ('Aspect_group' + str(aspect_number))
                    aspect_group = bpy.data.objects.get('Aspect_group' + str(aspect_number))
                    #print('here 1b' + str(post_number) + str(aspect_number))


            #Index aspect group, move position
            #aspect_group.pass_index = pass_count

            position, rotation = calculate_aspect_location(sign, post, aspect_number)

            # bpy.ops.object.select_all(action='DESELECT')

            aspect_group.location = position #+ aspect_group.location
            #aspect_group.rotation_euler.x = rotation[0] + aspect_group.rotation_euler[0]
            #aspect_group.rotation_euler.y = rotation[1] + aspect_group.rotation_euler[1]
            #aspect_group.rotation_euler.z = rotation[2] + aspect_group.rotation_euler[2]

            
            #print('here 2a' + str(post_number) + str(aspect_number))
            bpy.ops.object.select_all(action='DESELECT')
            if aspect_number == 0:
                post_obj.select = True
            else:
                post_group = bpy.data.objects.get('Post_group' + str(post_number))
                post_group.select = True
            aspect_group.select = True
            bpy.ops.object.join()
            bpy.context.object.name = ('Post_group' + str(post_number))
            post_group = bpy.data.objects.get('Post_group' + str(post_number))
            #print('here 2b' + str(post_number) + str(aspect_number))

        # Combine aspect to post here
        position, rotation = calculate_post_location(sign, post_number)

        post_group.location = position
        #post_group.rotation_euler.x = rotation[0] + post_group.rotation_euler[0]
        #post_group.rotation_euler.y = rotation[1] + post_group.rotation_euler[1]
        #post_group.rotation_euler.z = rotation[2] + post_group.rotation_euler[2]

    #####################################################################################################################
    #####################################################################################################################
    #                                    SHADOW CATCHER    CAMERA    LAMPS    COMPOSITOR                                #
    #####################################################################################################################
    #####################################################################################################################

    # Shadow catcher plane
    # bpy.ops.mesh.primitive_plane_add(location=(position))
    # bpy.context.object.scale=(5, 5, 1)
    # bpy.context.object.cycles.is_shadow_catcher = True

    location_values = (0.0, 0.0, 0.0)
    angle_values = (1.57, 0, 3.14)

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

    lamp_add(object_number, sun_rotation)

    background_img = load_img(frame_number)

    compositor_set(frame_number,
                   background_img)

    #####################################################################################################################
    #####################################################################################################################
    #                                              INFORMATION SAVING    RENDER                                         #
    #####################################################################################################################
    #####################################################################################################################

    # Render the image
    bpy.context.scene.frame_set(fno)
    #bpy.ops.render.render(write_still=True)

    config_dir['frame_data'] = frame_data

    with open(os.path.join(Output_meta_file,
                           'meta{:04d}.yaml'.format(frame_number)),
                           'w'
                           ) as md:
        md.write(yaml.dump(config_dir, indent=4, default_flow_style=False))
    fno += 1

print('Finished Rendering :)')
