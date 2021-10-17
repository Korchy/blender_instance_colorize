# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_instance_colorize

import bpy
from bpy import msgbus
from bpy.app.handlers import persistent
from bpy.types import Mesh
import random


class InstCol:

    @classmethod
    def sync(cls, context, sync_object=None):
        # synchronize mesh colors with object viewport colors
        if sync_object:
            # sync only for sync_object
            mesh_objects = (obj for obj in context.blend_data.objects if obj.data == sync_object.data)
        else:
            # global sync for all objects
            mesh_objects = (obj for obj in context.blend_data.objects if obj.type == 'MESH')
        for obj in mesh_objects:
            obj.color = obj.data.instance_color

    @classmethod
    def assign_random(cls, context):
        # Assign random colors to mesh instances
        # set random
        for mesh in context.blend_data.meshes:
            mesh.instance_color[0] = random.uniform(0, 1)
            mesh.instance_color[1] = random.uniform(0, 1)
            mesh.instance_color[2] = random.uniform(0, 1)
        # sync with object colors
        cls.sync(context=context)

    def on_instance_color_change(self, context):
        # on instance color changed
        self.sync(
            context=context,
            sync_object=context.object
        )

    @classmethod
    def monitor_instance_color_changes_start(cls, context):
        # monitor if the user change the instance color
        msgbus.subscribe_rna(
            key=(Mesh, 'instance_color'),
            owner=cls,
            args=(cls, context),
            notify=cls.on_instance_color_change
        )

    @classmethod
    def monitor_instance_color_changes_stop(cls):
        # stop to monitor if the user change the instance colors
        msgbus.clear_by_owner(cls)

    @classmethod
    def register(cls, context):
        # monitor instance color changes by user
        cls.monitor_instance_color_changes_start(
            context=context
        )
        # re-register on scene reload
        if inst_col_on_scene_load_post not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(inst_col_on_scene_load_post)

    @classmethod
    def unregister(cls):
        # unregister
        cls.monitor_instance_color_changes_stop()
        # re-register on scene reload
        if inst_col_on_scene_load_post in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(inst_col_on_scene_load_post)


@persistent
def inst_col_on_scene_load_post(*args):
    # on scene reload
    InstCol.monitor_instance_color_changes_start(
        context=bpy.context
    )
