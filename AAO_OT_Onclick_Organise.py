import sys 
import bpy
import os
import time

script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from AAO_UT_FileHandler import organise
from AAO_UT_FileHandler import is_blend_file_saved
from AAO_UT_FileHandler import get_downloads_folder
from AAO_UT_FileHandler import create_folder
from AAO_UT_FileHandler import get_blendfile_folder

blender_folder=None
save_count=0
local_time_at_start=None

def on_start(dummy):
    global local_time_at_start
    local_time_at_start=time.time()
    print("on start time: ",local_time_at_start)


def blender_folder_on_saved(dummy):
    
    global save_count
    if save_count==0:
        global blender_folder
        blender_folder=get_blendfile_folder()
    save_count+=1

class ENUM_PROPS_monitor_folder(bpy.types.PropertyGroup):
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

    on_start(None)

    def execute(self, context):
        selected_folder = context.scene.monitor_folder
        temporary_folder = None  # Define temporary_folder outside the if block
        
        if selected_folder == 'DOWNLOADS':
            if is_blend_file_saved():
                organise('0', blender_folder, local_time_at_start)

            else:
                temporary_folder = os.path.join(get_downloads_folder(), "Temp")
                create_folder(temporary_folder)
                print(temporary_folder)
                print("kaam karra hu")  
                print("onclick pe time: ",local_time_at_start)
                organise('0', temporary_folder,local_time_at_start)                
        else:
            if is_blend_file_saved():
                organise('1', blender_folder, local_time_at_start)
            else:
                self.report({'ERROR'},"Blender file has not been saved. Please save your Blender file before utilizing this option.")
                context.scene.monitor_folder='DOWNLOADS'
        
        return {'FINISHED'}

