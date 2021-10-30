# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class INST_COL_PT_panel(Panel):
    bl_idname = 'INST_COL_PT_panel'
    bl_label = 'Instance Colorize'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'IC'

    def draw(self, context):
        layout = self.layout
        preferences = context.preferences.addons[__package__].preferences
        # check viewport mode
        if context.space_data.shading.color_type == 'OBJECT':
            layout.label(text='Viewport Shading Mode: Object', icon='CHECKMARK')
        else:
            layout.operator(
                operator='inst_col.viewport_shading_obj',
                icon='OBJECT_DATAMODE'
            )
        # colorize mode
        layout.prop(
            data=preferences,
            property='colorize_mode',
            expand=True
        )
        # changing color
        box = layout.box()
        # if preferences.colorize_mode == 'SINGLE_COLOR':
        #     box.label(text='Instance Single Color')
        #     box.prop(
        #         data=preferences,
        #         property='color',
        #         text=''
        #     )
        # else:
        if context.object:
            box.label(text='Instance Color')
            box.prop(
                data=context.object.data,
                property='color',
                text=''
            )
        # tools
        row = layout.row()
        row.operator(
            operator='inst_col.assign_random',
            icon='MOD_HUE_SATURATION',
            text='Random'
        )
        row.operator(
            operator='inst_col.sync',
            icon='FILE_REFRESH',
            text=''
        )


def register():
    register_class(INST_COL_PT_panel)


def unregister():
    unregister_class(INST_COL_PT_panel)
