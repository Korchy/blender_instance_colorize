# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

import bpy
from bpy import msgbus
from bpy.app.handlers import persistent, depsgraph_update_post
from bpy.types import Mesh, Object
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
            objects = (obj for obj in context.blend_data.objects if hasattr(obj, 'color'))
        for obj in objects:
            obj.color = obj.data.color

    @classmethod
    def colorize_instances(cls, context):
        # Assign colors to mesh instances
        objects = (obj for obj in context.blend_data.objects)
        # set random
        for obj in objects:
            cls.colorize_data(obj=obj, force=True)

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
    def colorize_data(cls, obj, force=False):
        # set color for data
        # if force == True - change color anyway, if force == False - change color only once from default
        context = bpy.context
        if hasattr(obj, 'data') and obj.data is not None and hasattr(obj.data, 'color'):
            if obj.data.users > 1:
                if Color.equal(color_1=obj.data.color, color_2=cls.non_instance_color(context=context)) \
                        or force:
                    obj.data.color = cls.instance_color(context=context)
            else:
                obj.data.color = cls.non_instance_color(context=context)

    # def on_data_color_change(self, context):
    #     # on instance color changed
    #     self.sync(
    #         context=context,
    #         sync_object=context.object
    #     )

    # @classmethod
    # def monitor_data_color_changes_start(cls, context):
    #     # monitor if the user change the instance color
    #     msgbus.subscribe_rna(
    #         key=(Mesh, 'color'),
    #         owner=cls,
    #         args=(cls, context),
    #         notify=cls.on_data_color_change
    #     )

    # @classmethod
    # def monitor_data_color_changes_stop(cls):
    #     # stop to monitor if the user change the instance colors
    #     msgbus.clear_by_owner(cls)

    @classmethod
    def on_depsgraph_update_post(cls, scene, depsgraph):
        # check for added/deleted meshes
        if depsgraph.id_type_updated('SCENE'):
            for obj in depsgraph.updates:
                # if obj.is_updated_geometry and isinstance(obj.id, Object):
                if isinstance(obj.id, Object):
                    # through the bpy.data.objects because through obj.id.color doesn't work
                    cls.colorize_data(
                        obj=bpy.data.objects[obj.id.name]
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
        # # monitor instance color changes by user trough UI
        # cls.monitor_data_color_changes_start(
        #     context=context
        # )
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
        # # stop monitor color changes through the UI
        # cls.monitor_data_color_changes_stop()
        # re-register on scene reload
        if inst_col_on_scene_load_post in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(inst_col_on_scene_load_post)


@persistent
def inst_col_on_scene_load_post(*args):
    # on scene reload
    # InstCol.monitor_data_color_changes_start(
    #     context=bpy.context
    # )
    InstCol.monitor_meshes_start()
