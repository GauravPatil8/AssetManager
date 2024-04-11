import bpy
from bpy.props import StringProperty
from aao_ut_filehandler import get_package_path
from aao_ot_preset_creator import preset_folder_name
import os 
import shutil

preset_destination_path=os.path.join(get_package_path(),preset_folder_name)

class OBJECT_OT_Install_preset(bpy.types.Operator):
    bl_label="Install Preset"
    bl_idname="ot.installpreset"
    bl_description="Install any preset from local device."

    filepath: StringProperty(subtype="FILE_PATH")  #type: ignore

    def execute(self, context):
        preset_path = self.filepath
        shutil.move(preset_path,preset_destination_path)
        self.report({'INFO'},"Preset installed.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class OBJECT_OT_share_preset(bpy.types.Operator):
    bl_label="share Preset"
    bl_idname="ot.sharepreset"
    bl_description="share any preset from local device."

    filepath: StringProperty(subtype="DIR_PATH")  #type: ignore

    def execute(self, context):
        preset_basename=context.scene.folder_presets
        folder_path = self.filepath
        preset_path=os.path.join(preset_destination_path,preset_basename+'.json')
        shutil.copy(preset_path,folder_path)
        self.report({'INFO'},"Preset shared.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class OBJECT_OT_remove_preset(bpy.types.Operator):
    bl_label="Remove Preset"
    bl_idname="ot.removepreset"
    bl_description="remove any preset from local device."

    def execute(self, context):
        preset_basename=context.scene.folder_presets
        os.remove(os.path.join(preset_destination_path,preset_basename+'.json')) 
        context.scene.folder_presets='DEFAULT'
        return {'FINISHED'}
   