# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

import bpy
from bpy.app.handlers import persistent, depsgraph_update_post
from bpy.types import Object
from .bpy_plus.color import Color


class InstCol:

    @classmethod
    def sync(cls, context, data=None):
        # synchronize object viewport colors with mesh data colors 
        if data:
            # sync only for specified data
            objects = (obj for obj in context.blend_data.objects if
                       hasattr(obj, 'data') and obj.data == data and hasattr(obj, 'color'))
        else:
            # global sync for all objects
            objects = (obj for obj in context.blend_data.objects if
                       hasattr(obj, 'data') and hasattr(obj, 'color'))
        for obj in objects:
            obj.color = obj.data.color

    @classmethod
    def colorize_instances(cls, context):
        # Assign colors to mesh instances
        objects = (obj for obj in context.blend_data.objects)
        # set random
        for obj in objects:
            cls.colorize_data(
                obj=obj,
                context=context,
                force=True
            )

    @staticmethod
    def instance_color(context):
        # get color for instances
        if context.preferences.addons[__package__].preferences.colorize_mode == 'SINGLE_COLOR':
            return context.preferences.addons[__package__].preferences.instance_color_single
        else:
            return Color.random()

    @staticmethod
    def non_instance_color(context):
        # get color for non-instances
        return context.preferences.addons[__package__].preferences.non_instance_color

    @classmethod
    def colorize_data(cls, obj, context, force=False):
        # set color for data
        # if force == True - change color anyway, if force == False - change color only once from default
        if hasattr(obj, 'data') and obj.data is not None and hasattr(obj.data, 'color'):
            if obj.data.users > 1:
                if Color.equal(color_1=obj.data.color, color_2=cls.non_instance_color(context=context)) \
                        or force:
                    obj.data.color = cls.instance_color(context=context)
            else:
                obj.data.color = cls.non_instance_color(context=context)

    @classmethod
    def on_depsgraph_update_post(cls, scene, depsgraph):
        # check for added/deleted meshes
        if depsgraph.id_type_updated('SCENE'):
            for obj in depsgraph.updates:
                # if obj.is_updated_geometry and isinstance(obj.id, Object):
                if isinstance(obj.id, Object):
                    # through the bpy.data.objects because through obj.id.color doesn't work
                    cls.colorize_data(
                        obj=bpy.data.objects[obj.id.name],
                        context=bpy.context
                    )

    @classmethod
    def monitor_meshes_start(cls):
        # start monitor if the meshes added or deleted
        if cls.on_depsgraph_update_post not in depsgraph_update_post:
            depsgraph_update_post.append(cls.on_depsgraph_update_post)

    @classmethod
    def monitor_meshes_stop(cls):
        # stop monitor if the meshes added or deleted
        if cls.on_depsgraph_update_post in depsgraph_update_post:
            depsgraph_update_post.remove(cls.on_depsgraph_update_post)

    @classmethod
    def register(cls, context):
        # register
        # monitor meshes adding/removing
        cls.monitor_meshes_start()
        # re-register on scene reload
        if inst_col_on_scene_load_post not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(inst_col_on_scene_load_post)

    @classmethod
    def unregister(cls):
        # unregister
        # stop monitor meshes adding/removing
        cls.monitor_meshes_stop()
        # remove re-registering on scene reload
        if inst_col_on_scene_load_post in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(inst_col_on_scene_load_post)


@persistent
def inst_col_on_scene_load_post(*args):
    # on scene reload
    InstCol.monitor_meshes_start()
