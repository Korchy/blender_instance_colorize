# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

from bpy.props import FloatVectorProperty
from bpy.types import Mesh


def register():
    Mesh.instance_color = FloatVectorProperty(
         name='Instance Color',
         subtype='COLOR',
         size=4,
         min=0.0,
         max=1.0,
         default=(0.8, 0.8, 0.8, 1.0)
     )


def unregister():
    del Mesh.instance_color
