import bpy

pos_head=

bpy.ops.mesh.primitive_monkey_add(location=(0, -0.3, pos_head), rotation=(0, 0, 0))

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))

bpy.ops.transform.resize(value=(1.2, 0.8, 1.5))


bpy.ops.mesh.primitive_cylinder_add(location=(2, 0, 0))
bpy.ops.transform.resize(value=(0.5, 0.5, 1.5))
bpy.context.object.rotation_euler.y= -0.5

bpy.ops.object.duplicate()
bpy.ops.transform.translate(value=(-4, 0, 0))
bpy.context.object.rotation_euler.y= 0.5

bpy.ops.mesh.primitive_cylinder_add(location=(0.8, 0, -3.5))
bpy.ops.transform.resize(value=(0.5, 0.5, 2))

bpy.ops.object.duplicate()
bpy.ops.transform.translate(value=(-1.6, 0, 0))