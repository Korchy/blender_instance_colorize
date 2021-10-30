# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

import bpy
from bpy.props import FloatVectorProperty
from bpy.types import Mesh
from .inst_col import InstCol


def register():
    Mesh.color = FloatVectorProperty(
         name='Color',
         subtype='COLOR',
         size=4,
         min=0.0,
         max=1.0,
         default=bpy.context.preferences.addons[__package__].preferences.non_instance_color,
         update=lambda self, context: InstCol.sync(
             context=context,
             data=self
         )

    )


def unregister():
    del Mesh.color
