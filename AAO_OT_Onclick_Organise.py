from aao_ut_filehandler import get_blendfile_folder
from aao_ut_filehandler import create_folder
from aao_ut_filehandler import get_downloads_folder
from aao_ut_filehandler import is_blend_file_saved
from aao_ut_filehandler import organise
from aao_ut_filehandler import return_projectfile_name
from aao_ut_filehandler import temporary_folder_name
import sys
import bpy
import os
import time
import threading

script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

loop_flag=True
local_time_at_start = None
blender_folder = None



def get_blender_folder_path():
    global blender_folder
    global loop_flag
    blender_folder = get_blendfile_folder()
    project_file_name=return_projectfile_name()
    while loop_flag:
        if os.path.basename(blender_folder)==project_file_name:
            loop_flag=False
        blender_folder = os.path.dirname(blender_folder)

def on_start(dummy):
    global local_time_at_start
    local_time_at_start = time.time()


class ENUM_PROPS_monitor_folder(bpy.types.PropertyGroup):
    bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('DOWNLOADS', 'Monitor Downloads Folder',
             'This option enables monitoring of the downloads folder for newly added files.'),
            ('BLENDFOLDER', 'Monitor Blender File Folder',
             'This option enables monitoring of the folder where your Blender file is saved for newly added files.'),
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
                threading.Thread(target=organise, daemon=True, args=(
                    '0', blender_folder, local_time_at_start)).start()

            else:
                temporary_folder = os.path.join(get_downloads_folder(), temporary_folder_name)
                create_folder(temporary_folder)
                
                threading.Thread(target=organise, daemon=True, args=(
                    '0', temporary_folder, local_time_at_start)).start()
                self.report({'INFO'}, "Organising Files")

        else:
            if is_blend_file_saved():
                threading.Thread(target=organise, daemon=True, args=(
                    '1', blender_folder, local_time_at_start)).start()
                self.report({'INFO'}, "Organising Files")

            else:
                self.report(
                    {'ERROR'}, "Blender file has not been saved. Please save your Blender file before utilizing this option.")
                context.scene.monitor_folder = 'DOWNLOADS'

        return {'FINISHED'}
