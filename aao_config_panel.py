import bpy
import os
import json
from aao_ut_filehandler import create_folder,default_setter

script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
class BOOL_PROPS_defaults(bpy.types.PropertyGroup):
    bpy.types.Scene.default_config=bpy.props.BoolProperty(    #type:ignore
        name="Configure Defaults",
        description="Clicking this option will load current addon preferences everytime you start Blender",
        default=False
    )
class ENUM_Zip_extract(bpy.types.PropertyGroup):
    
    bpy.types.Scene.zip_extraction=bpy.props.EnumProperty(
        items=[
            ('SEP', 'Separate Assets', 'This option organizes all assets into their respective folders during the extraction of a zipfile.'),
            ('NOSEP', 'Predominant Asset Type', 'This option extracts a Zipfile into a specific folder based on the predominant type of asset it contains. For instance, if the Zipfile contains a significant number of video files, it will be extracted into the video files folder.'),
        ],
        default=default_setter('zip_enum','NOSEP')
    )# type: ignore

class OBJECT_OT_Save_configs(bpy.types.Operator):
    bl_label='Save Defaults'
    bl_idname='ot.savedefaultconfigs'

    def execute(self, context):
        config_dict={}
        config_dict['Enable']=True
        config_dict['preset']=context.scene.folder_presets
        config_dict['analysis_folder']=context.scene.monitor_folder
        if context.scene.monitor_folder!='DOWNLOADS':
            config_dict['M_folder']=context.scene.folder_path
        config_dict['D_folder']=context.scene.destination_path
        
        if context.scene.monitoring_type_prop=='ONCLICKOPERATOR':
            config_dict['M_type']='ONCLICKOPERATOR'
        else:
            config_dict['M_type']='REALTIME'
        if context.scene.monitoring_type_prop=='REALTIME':
            config_dict['R_time']=context.scene.delay_time_prop
        else:
            config_dict['R_time']=None
        if context.scene.zip_extraction=='SEP':
            config_dict['zip_enum']='SEP'
            config_dict['zip_mode']=True
        else:
            config_dict['zip_mode']=False
            config_dict['zip_enum']='NOSEP'
        
        json_file_name =os.path.join(package_path,'addon_configuration','AddonDefaults.json')
        create_folder(os.path.join(package_path,'addon_configuration'))

        with open(json_file_name, 'w') as json_file:
            json.dump(config_dict, json_file,indent=4)

        self.report({'INFO'},'Saved Current configuration.')
        return {'FINISHED'}