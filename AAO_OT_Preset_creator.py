from typing import Set
import bpy
import os
import json
from bpy.types import Context,Operator
from bpy.props import StringProperty
from AAO_UT_FileHandler import get_package_path

subdirectories=[]
selected_folder_path = None

tag_items=[
    ('PROJECT','project_files',''),
    ('MODEL','model_files',''),
    ('IMAGE','image_files',''),
    ('MOCAP','mocap_files',''),
    ('MATERIAL','material_files',''),
    ('VIDEO','video_files',''),
    ('AUDIO','audio_files','')
    ]

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

def get_subdirectories(directory):
    subdirectories = []
    
    for item in os.listdir(directory):
        
        item_path = os.path.join(directory, item)
       
        if os.path.isdir(item_path):
            subdirectories.append(os.path.basename(item_path))
            
            subdirectories.extend(get_subdirectories(item_path))
    return subdirectories


class ENUM_PROPS_Tags(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty() # type: ignore
    value: bpy.props.EnumProperty(
        items=[
            ('NONE','none',''),
            ('PROJECT','project_files',''),
            ('MODEL','model_files',''),
            ('IMAGE','image_files',''),
            ('MOCAP','mocap_files',''),
            ('MATERIAL','material_files',''),
            ('VIDEO','video_files',''),
            ('AUDIO','audio_files','')
        ],
        name="Value"
    ) # type: ignore#  type: ignore
    

    

class OPEN_FOLDER_OT_OpenFolder(Operator):
    bl_idname = "folder_selector.open_folder"
    bl_label = "Open Folder"
    bl_description = "Select a folder"
    
    filepath: StringProperty(subtype="DIR_PATH") # type: ignore

    def execute(self, context):
        global selected_folder_path
        global subdirectories

        selected_folder_path=self.filepath
        subdirectories=get_subdirectories(selected_folder_path)
        context.scene.preset_analysis_folder=selected_folder_path
        for sub_dir in subdirectories:
            new_enum_property = context.scene.enum_properties.add()
            new_enum_property.name = sub_dir
            new_enum_property.value = "NONE"    
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


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
    
    
class OBJECT_PT_preset_creator(bpy.types.Panel):
    bl_label = "Preset Creator"
    bl_idname = "OBJECT_PT_presetcreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Organiser"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global subdirectories
        layout=self.layout
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.scene, "change_folder_name", text="Change Folder Name")
        
        if context.scene.change_folder_name:
            box.prop(context.scene, "folder_name", text="Select Folder Name")
            box.prop(context.scene, "custom_folder_name", text="Enter Folder Name")
            box.operator("object.updatefoldername", text="Set")


        
        layout.label(text='Select a folder')
        row=layout.row()
        row.prop(context.scene,'preset_analysis_folder',text='')
        row.operator('folder_selector.open_folder',icon='FILE_FOLDER',text='')

        

        if subdirectories!=[]:
            for enum_property in context.scene.enum_properties:
                new_row=layout.row()
                new_row.prop(enum_property, "name", text="")
                new_row.prop(enum_property, "value", text="")

            
