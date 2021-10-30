# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .inst_col import InstCol


class INST_COL_OT_viewport_shading_obj(Operator):
    bl_idname = 'inst_col.viewport_shading_obj'
    bl_label = 'Viewport Shading mode: Object'
    bl_description = 'Switch to the Viewport Shading mode: Object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.shading.color_type = 'OBJECT'
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'


class INST_COL_OT_colorize_instances(Operator):
    bl_idname = 'inst_col.colorize_instances'
    bl_label = 'Colorize Instances'
    bl_description = 'Assign colors for objects instances'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        InstCol.colorize_instances(
            context=context
        )
        return {'FINISHED'}


def register():
    register_class(INST_COL_OT_viewport_shading_obj)
    register_class(INST_COL_OT_colorize_instances)


def unregister():
    unregister_class(INST_COL_OT_colorize_instances)
    unregister_class(INST_COL_OT_viewport_shading_obj)
