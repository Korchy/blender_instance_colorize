# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

from bpy.types import AddonPreferences
from bpy.props import FloatVectorProperty, EnumProperty
from bpy.utils import register_class, unregister_class


class INST_COL_preferences(AddonPreferences):
    bl_idname = __package__

    colorize_mode: EnumProperty(
        name='Colorize Mode',
        items=[
            ('SINGLE_COLOR', 'Single Color', 'Single Color'),
            ('MULTI_COLOR', 'Multi Color', 'Multi Color')
        ],
        default='MULTI_COLOR'
    )

    instance_color_single: FloatVectorProperty(
        name='Instance Color Single',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.3, 0.8, 0.8, 1.0)
    )

    non_instance_color: FloatVectorProperty(
        name='Non-instance Color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.8, 0.8, 1.0)
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text='Colorize Mode:')
        row = layout.row()
        row.prop(data=self, property='colorize_mode', expand=True)
        if self.colorize_mode == 'SINGLE_COLOR':
            layout.prop(data=self, property='instance_color_single', text='')


def register():
    register_class(INST_COL_preferences)


def unregister():
    unregister_class(INST_COL_preferences)
