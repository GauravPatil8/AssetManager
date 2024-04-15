#Copyright (c) 2024 Gaurav 
# bl_info = {
#     "name": "Realtime Asset Organiser",
#     "author": "Gaurav",
#     "version": (0, 1, 0),
#     "blender": (4, 0, 0),
#     "location": "View3D > Sidebar > Asset Organiser",
#     "description": "Real-time Asset Organizer for 3D Artists is a powerful Blender addon designed to streamline and enhance the workflow of 3D artists by providing a dynamic and efficient asset organisation system.Support:assetorganiser.help@gmail.com",
#     "doc_url": "https://github.com/Gauravpatil-8/Real-Time-Asset-Organiser/blob/main/Documentation/Setup.md",
#     "tracker_url": "https://github.com/Gauravpatil-8/Real-Time-Asset-Organiser/issues",
#     "category": "System"
# }

import sys
import bpy
import os


script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from aao_ot_onclick_organise import on_start
from aao_ot_onclick_organise import OBJECT_OT_Onclick_Organise  
from aao_ot_monitoring_type  import OBJECT_OT_monitor_type
from aao_ot_log              import OBJECT_OT_log
from aao_ot_log              import OBJECT_OT_log_popup
from aao_ot_install_preset   import OBJECT_OT_Install_preset
from aao_ot_install_preset   import OBJECT_OT_share_preset
from aao_ot_install_preset   import OBJECT_OT_remove_preset
from aao_ot_preset_creator   import OBJECT_OT_update_preset_list
from aao_ot_preset_creator   import OBJECT_OT_save_preset
from aao_ot_preset_creator   import ENUM_PROPS_Tags
from aao_propertygroups      import ADDON_PROPERTYGROUP
from aao_ot_preset_creator   import OPEN_FOLDER_OT_OpenFolder
from aao_ot_preset_creator   import ENUM_PROPS_folder_presets
from aao_ot_monitoring_type  import ENUM_PROPS_monitoring_type
from aao_ot_preset_creator   import OBJECT_PT_preset_creator
from aao_pt_addonui          import OBJECT_PT_AssetManagerUI
from aao_ot_onclick_organise import OBJECT_OT_monitoringfolder
from aao_ot_onclick_organise import OBJECT_OT_destinationfolder
from aao_config_panel        import OBJECT_OT_Save_configs

classes = (ADDON_PROPERTYGROUP,ENUM_PROPS_monitoring_type, ENUM_PROPS_folder_presets,ENUM_PROPS_Tags, OBJECT_OT_monitoringfolder,OBJECT_OT_destinationfolder,
           OBJECT_OT_update_preset_list, OBJECT_OT_Install_preset,OBJECT_OT_share_preset,OBJECT_OT_remove_preset,OBJECT_OT_Onclick_Organise, OBJECT_OT_save_preset, OBJECT_OT_log_popup, OBJECT_OT_log, OBJECT_OT_monitor_type,OBJECT_OT_Save_configs, OPEN_FOLDER_OT_OpenFolder, OBJECT_PT_AssetManagerUI, OBJECT_PT_preset_creator)

def register():
    
    bpy.app.handlers.load_post.append(on_start)
    for kls in classes:
        bpy.utils.register_class(kls)
    bpy.types.Scene.enum_properties = bpy.props.CollectionProperty(type=ENUM_PROPS_Tags)
    
def unregister():
    for kls in reversed(classes):
        bpy.utils.unregister_class(kls)
    del bpy.types.Scene.enum_properties
    sys.path.remove(package_path)
register()
