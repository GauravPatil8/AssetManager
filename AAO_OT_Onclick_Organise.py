import sys 
import bpy
import os

script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from AAO_UT_FileHandler import organise
from AAO_UT_FileHandler import is_blend_file_saved
from AAO_UT_FileHandler import get_blendfile_folder
from AAO_UT_FileHandler import get_downloads_folder
from AAO_UT_FileHandler import create_folder

localtime_atStart = 1707375615.0  # temporary

bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
    items=[
        ('DOWNLOADS', 'Monitor Downloads Folder', 'This option enables monitoring of the downloads folder for newly added files.'),
        ('BLENDFOLDER', 'Monitor Blender File Folder', 'This option enables monitoring of the folder where your Blender file is saved for newly added files.'),
    ],
    default='DOWNLOADS',
)

class OBJECT_OT_Onclick_Organise(bpy.types.Operator):
    bl_label = 'onlick_organise'
    bl_idname = "object.onclickorganise"
    bl_description = "Clicking this organizes downloaded files"

    def execute(self, context):
        selected_folder = context.scene.monitor_folder
        temporary_folder = None  # Define temporary_folder outside the if block
        
        if selected_folder == 'DOWNLOADS':
            if is_blend_file_saved():
                organise('0', get_blendfile_folder(), localtime_atStart)
            else:
                temporary_folder = os.path.join(get_downloads_folder(), "Temp")
                create_folder(temporary_folder)
                print(temporary_folder)
                print("kaam karra hu")  
                organise('0', temporary_folder,localtime_atStart)                
        else:
            organise('1', get_blendfile_folder(), localtime_atStart)

        
        return {'FINISHED'}
