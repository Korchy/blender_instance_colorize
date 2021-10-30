# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

import bpy
from bpy.app.handlers import persistent
from . import inst_col_ops
from . import inst_col_prefs
from . import inst_col_props
from . import inst_col_ui
from .addon import Addon
from . inst_col import InstCol


bl_info = {
    'name': 'Instance Colorizer',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 93, 0),
    'location': '3D Viewport - N panel - IC tab',
    'wiki_url': 'https://b3d.interplanety.org/en/',
    'tracker_url': 'https://b3d.interplanety.org/en/',
    'description': 'Colorize object instances in viewport'
}


@persistent
def inst_col_register():
    # register InstCol
    if bpy.context and hasattr(bpy.context, 'scene'):
        InstCol.register(context=bpy.context)
    else:
        return 0.25


def register():
    if not Addon.dev_mode():
        inst_col_prefs.register()
        inst_col_props.register()
        inst_col_ops.register()
        inst_col_ui.register()
        bpy.app.timers.register(
            function=inst_col_register,
            first_interval=0.25
        )
    else:
        print('It seems you are trying to use the dev version of the '
              + bl_info['name']
              + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        InstCol.unregister()
        inst_col_ui.unregister()
        inst_col_ops.unregister()
        inst_col_props.unregister()
        inst_col_prefs.unregister()


if __name__ == '__main__':
    register()
