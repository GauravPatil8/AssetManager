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
import atexit
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from AAO_OT_Onclick_Organise   import OBJECT_OT_Onclick_Organise #classes
from AAO_OT_Onclick_Organise   import ENUM_PROPS_monitor_folder
from AAO_OT_Update_folder_name import OBJECT_OT_update_foldername
from AAO_OT_Update_folder_name import Bool_PROPS_Change_folder_name
from AAO_OT_Update_folder_name import ENUM_PROPS_Folder_name
from AAO_OT_Update_folder_name import STRING_PROPS_custom_folder_name
from AAO_PT_AddonUI            import OBJECT_PT_AssetManagerUI
from AAO_PT_AddonUI            import OBJECT_PT_preset_creator
from AAO_OT_Log                import OBJECT_OT_log_popup
from AAO_OT_Log                import OBJECT_OT_log
from AAO_OT_Monitoring_Type    import OBJECT_OT_monitor_type
from AAO_OT_Monitoring_Type    import ENUM_PROPS_delay_time
from AAO_OT_Monitoring_Type    import ENUM_PROPS_monitoring_type
from AAO_OT_Preset_creator     import ENUM_PROPS_folder_presets
from AAO_OT_Preset_creator     import Bool_PROPS_Create_preset
from AAO_OT_Preset_creator     import STRING_PROPS_preset_analysis_folder
from AAO_OT_Preset_creator     import OBJECT_OT_save_preset
from AAO_OT_Preset_creator     import OBJECT_OT_OpenFolderOperator
from AAO_OT_Onclick_Organise   import on_start                   #functions
from AAO_OT_Onclick_Organise   import blender_folder_on_saved
from AAO_DB_FolderNames        import close_connection         
from AAO_UT_FileHandler        import database_connection #variables



def on_exit():
    close_connection(database_connection)
     
     

classes=(OBJECT_OT_Onclick_Organise,OBJECT_PT_AssetManagerUI,OBJECT_PT_preset_creator,OBJECT_OT_update_foldername,OBJECT_OT_log,OBJECT_OT_log_popup,OBJECT_OT_monitor_type,Bool_PROPS_Change_folder_name,ENUM_PROPS_Folder_name,ENUM_PROPS_delay_time,ENUM_PROPS_monitoring_type,STRING_PROPS_custom_folder_name,ENUM_PROPS_monitor_folder,ENUM_PROPS_folder_presets,Bool_PROPS_Create_preset,OBJECT_OT_save_preset,STRING_PROPS_preset_analysis_folder,OBJECT_OT_OpenFolderOperator) 


def register(): 
    bpy.app.handlers.load_post.append(on_start)
    
    atexit.register(on_exit)   
    bpy.app.handlers.save_post.append(blender_folder_on_saved)
    for kls in classes:
            bpy.utils.register_class(kls)
    
    


def unregister():
    bpy.app.handlers.save_post.remove(blender_folder_on_saved)
    
    for kls in reversed(classes):
        bpy.utils.unregister_class(kls)
    del bpy.types.Scene.custom_folder_name
    bpy.app.handlers.load_post.remove(on_start)
    
    atexit.unregister(on_exit)
    
  
register()

