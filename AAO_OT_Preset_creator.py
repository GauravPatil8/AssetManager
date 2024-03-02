from typing import Set
import bpy
import os
import json

from bpy.types import Context
from AAO_UT_FileHandler import get_package_path

selected_folder_path = ""

preset_list=[('DEFAULT','Default','Stores downloaded files in a simple folder structure based on their type'),]

package_path=get_package_path()
target_folder=os.path.join(package_path,"Presets")

for file in os.listdir(target_folder):
    if os.path.isfile(os.path.join(target_folder,file)) and file !='Default.db':
        file_name=file.split('.')[0]
        file_id=file_name.upper()
        file_description=''
        preset_details_list=[file_id,file_name,file_description]
        preset_details_tuple=tuple(preset_details_list)
        preset_list.append(preset_details_tuple)

def update_selected_folder(self, context):
    global selected_folder_path
    selected_folder_path = self.preset_analysis_folder


class STRING_PROPS_preset_name(bpy.types.PropertyGroup):   
    bpy.types.Scene.preset_name = bpy.props.StringProperty(
        name="Enter Preset Name",
        description="Enter Preset name",
        default="",
    )
class STRING_PROPS_preset_analysis_folder(bpy.types.PropertyGroup):   
    bpy.types.Scene.preset_analysis_folder = bpy.props.StringProperty(
        name="Select Folder",
        description="Select folder to be Analysied",
        default="",
        update=update_selected_folder,
    )


class Bool_PROPS_Create_preset(bpy.types.PropertyGroup):
    bpy.types.Scene.create_preset = bpy.props.BoolProperty(
            name="Create Preset",
            description="Enable create Preset",
            default=False,  
        )

class ENUM_PROPS_folder_presets(bpy.types.PropertyGroup):

    bpy.types.Scene.folder_presets = bpy.props.EnumProperty(
        items=preset_list,
        description="Select a folder structure",   
        default='DEFAULT', 
        )
    
class OBJECT_OT_save_preset(bpy.types.Operator):
    bl_label='Save Preset'
    bl_idname='object.savepreset'

    def execute(self, context: Context):
        print("sample text")
        return{'FINISHED'}
    
class OBJECT_OT_OpenFolderOperator(bpy.types.Operator):
    bl_idname = "ui.open_folder_operator"
    bl_label = "Open Folder"
    bl_description = "Open folder viewer"

    def execute(self, context):
        print(selected_folder_path)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "preset_analysis_folder")
    


    
bpy.types.Scene.selected_folder_path = bpy.props.StringProperty()