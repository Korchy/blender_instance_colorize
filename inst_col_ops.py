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


class INST_COL_OT_sync(Operator):
    bl_idname = 'inst_col.sync'
    bl_label = 'Synchronize colors'
    bl_description = 'Synchronize instance colors with object viewport colors'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        InstCol.sync(
            context=context
        )
        return {'FINISHED'}


class INST_COL_OT_assign_random(Operator):
    bl_idname = 'inst_col.assign_random'
    bl_label = 'Assign random colors'
    bl_description = 'Assign random colors to mesh instances'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        InstCol.assign_random(
            context=context
        )
        return {'FINISHED'}


def register():
    register_class(INST_COL_OT_viewport_shading_obj)
    register_class(INST_COL_OT_sync)
    register_class(INST_COL_OT_assign_random)


def unregister():
    unregister_class(INST_COL_OT_assign_random)
    unregister_class(INST_COL_OT_sync)
    unregister_class(INST_COL_OT_viewport_shading_obj)
