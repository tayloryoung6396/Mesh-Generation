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

def configuration():

    # TODO Remove unused variables
    # TODO read in config file

    config = {
        'materials' : {
            'aspect' : {
                'red' : (1, 0, 0)
                'yellow' : (1, 1, 0)
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
            'number_posts' :
            'posts_min' :
            'posts_max' :
            'post' : {
                'number_aspects' :
                'aspects_min' :
                'aspects_max' :
                'aspect' : {
                    'number_lights' :
                    'lights_min' :
                    'lights_max' :
                    'light' : {
                        'status' : (['off'], ['off'], ['off'])
                    },
                },
            }
        }
    }
    return config


config_dir = configuration()

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

# Remove previous materials
def delete_materials():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)

# Remove previous compositor
def delete_compositor():
    for items in bpy.data.materials:
        bpy.data.materials.remove(items)






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
#                                                   CODE HERE                                                       #
#####################################################################################################################
#####################################################################################################################

delete_materials()

delete_compositor()

delete_objects()

compositor_add()

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
        output_data['img_name'] = filename
    else:
        continue

    # Find current frame number
    frame_number = filename.lstrip('frame')
    frame_number = frame_number.rstrip('.jpg')
    frame_number = int(frame_number)


    # Read in meta data of frame number
    with open(os.path.join(Input_meta_file)) as json_data:
        data = json.load(json_data)
        for x in data:
            if x['frame_number'] == img_number:
                frame_data = x
                break

    sign = config_dir['sign']

    # Choose random number of posts for frame
    sign['number_posts'] = random.randint(sign['posts_min'], sign['posts_max'])

    for post_number in range(0, sign['number_posts']):
        post = sign['post']

        post['number_aspects'] = random.randint(post['aspects_min'], post['aspects_max'])
        post_obj = draw_post()

        for aspect_number in range(0, post['number_aspects']):
            aspect = post['aspect']

            # Random style
            style = random.choice(aspect['style'])
            background_obj = draw_background[style]()

            aspect['number_lights'] = random.randint(aspect['light_min'], aspect['light_max'])
            light_on = random.randint(aspect['light_min'], aspect['number_lights'])
            aspect['light']['status'][light_on][0] = 'on'

            for light_number in range(0, aspect['number_lights']):

                light = aspect['light']

                if light['status'] == 'blank':
                    blank_obj = draw_blank()
                    blank_obj.name = 'blank' + str(x_light)
                    
                    mat = bpy.data.materials['PBR_Dielectric']
                    blank_obj.data.materials.append(mat)

                    blank_obj = move_can()

                else:
                    bpy.ops.object.select_all(action='DESELECT')

                    can_obj = draw_can()
                    can_obj.name = 'can' + str(x_light)
                    
                    mat = bpy.data.materials['PBR_Dielectric']
                    can_obj.data.materials.append(mat)

                    can_obj = move_can()

                    light_obj = draw_light()
                    light_obj.name = 'light' + str(x_light)

                    if light['status'] == 'on':
                        mat = bpy.data.materials[light['colour']['status'][aspect['number_lights']][light_number]]                    
                    else:
                        mat = bpy.data.materials[light['colour']['status'][aspect['number_lights']][light_number]]

                    light_obj.data.materials.append(mat)

                    light_obj = move_can()

            # For each aspect join parts

            # Apply index

            # save meta for aspect
