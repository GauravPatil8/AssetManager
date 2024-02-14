# bl_info = {
#     "name": "Realtime Asset Manager",
#     "blender": (4, 0, 2),
#     "category": "System", 
#     "author": "Swami",
#     "version": (0, 0, 1),
#     "location": "View3D > UI> Asset Organiser",
#     "description": "Real-time Asset Organizer for 3D Artists is a powerful Blender addon designed to streamline and enhance the workflow of 3D artists by providing a dynamic and efficient asset management system.",
#     "warning": "",
#     # "wiki_url": "URL to your addon's documentation or wiki",
#     # "tracker_url": "URL to your addon's issue tracker",
#     "support": "COMMUNITY",
# }


import sys 
import bpy
import os
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from AAO_OT_Onclick_Organise import OBJECT_OT_Onclick_Organise
from AAO_OT_Onclick_Organise import on_start
from AAO_OT_Onclick_Organise import blender_folder_on_saved
from AAO_OT_Update_folder_name import OBJECT_OT_update_foldername
from AAO_PT_AddonUI import OBJECT_PT_AssetManagerUI
from AAO_OT_Log import OBJECT_OT_log_popup
from AAO_OT_Log import OBJECT_OT_log
from AAO_DB_FolderNames import close_connection
from AAO_UT_FileHandler import memory_connection
from AAO_UT_FileHandler import database_connection


def on_exit(dummy):
    close_connection(memory_connection)
    close_connection(database_connection)
     
     

classes=(OBJECT_OT_Onclick_Organise,OBJECT_PT_AssetManagerUI,OBJECT_OT_update_foldername,OBJECT_OT_log,OBJECT_OT_log_popup) 



def register():
    bpy.types.Scene.custom_folder_name = bpy.props.StringProperty(
        name="Enter Folder Name",
        description="Enter a custom folder name",
        default="",
    )
    
    bpy.app.handlers.load_post.append(on_start)
    bpy.app.handlers.save_post.append(blender_folder_on_saved)
    for kls in classes:
            bpy.utils.register_class(kls)
    bpy.app.handlers.persistent.append(on_exit)

def unregister():
    
    bpy.app.handlers.load_post.remove(on_start)
    bpy.app.handlers.save_post.remove(blender_folder_on_saved)
    for kls in reversed(classes):
        bpy.utils.unregister_class(kls)
    del bpy.types.Scene.custom_folder_name
    bpy.app.handlers.persistent.remove(on_exit)

register()

