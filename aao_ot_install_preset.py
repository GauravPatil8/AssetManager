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
        self.report({'INFO'},"Preset Installed.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
