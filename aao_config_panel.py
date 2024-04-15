import bpy
import os
import json
from aao_ut_filehandler import create_folder
from aao_constants import ZIPMODE_PREDOMINANT_ID,ZIPMODE_SEPERATE_ID,SRCFOLDER_DOWNLOADS_ID,MONTIORING_ONCLICK_ID,MONTIORING_REALTIME_ID,PRESET_KEY,SRCFOLDER_KEY,MONITORING_KEY,DESTFOLDERPATH_KEY,SRCFOLDERPATH_KEY,DELAY_KEY,ZIPENUM_KEY,ZIPMODE_KEY

script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)


class OBJECT_OT_Save_configs(bpy.types.Operator):
    bl_label='Save Defaults'
    bl_idname='ot.savedefaultconfigs'

    def execute(self, context):
        config_dict={}
        config_dict['Enable']=True
        config_dict[PRESET_KEY]=context.scene.folder_presets
        config_dict[SRCFOLDER_KEY]=context.scene.monitor_folder
        if context.scene.monitor_folder!=SRCFOLDER_DOWNLOADS_ID:
            config_dict[SRCFOLDERPATH_KEY]=context.scene.folder_path
        config_dict[DESTFOLDERPATH_KEY]=context.scene.destination_path
        
        if context.scene.monitoring_type_prop==MONTIORING_ONCLICK_ID:
            config_dict[MONITORING_KEY]=MONTIORING_ONCLICK_ID
        else:
            config_dict[MONITORING_KEY]=MONTIORING_REALTIME_ID
            config_dict[DELAY_KEY]=context.scene.delay_time_prop

        if context.scene.zip_extraction==ZIPMODE_SEPERATE_ID:
            config_dict[ZIPENUM_KEY]=ZIPMODE_SEPERATE_ID
            config_dict[ZIPMODE_KEY]=True
        else:
            config_dict[ZIPMODE_KEY]=False
            config_dict[ZIPENUM_KEY]=ZIPMODE_PREDOMINANT_ID
        
        json_file_name =os.path.join(package_path,'addon_configuration','AddonDefaults.json')
        create_folder(os.path.join(package_path,'addon_configuration'))

        with open(json_file_name, 'w') as json_file:
            json.dump(config_dict, json_file,indent=4)

        self.report({'INFO'},'Saved Current configuration.')
        return {'FINISHED'}