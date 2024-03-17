from AAO_UT_FileHandler import get_blendfile_folder
from AAO_UT_FileHandler import create_folder
from AAO_UT_FileHandler import get_downloads_folder
from AAO_UT_FileHandler import is_blend_file_saved
from AAO_UT_FileHandler import organise
import sys
import bpy
import os
import time
import threading
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)


blender_folder = None


local_time_at_start = None

###ye function ko improve karna bhai######
def get_blender_folder_path():
    global blender_folder
    old_blender_folder = get_blendfile_folder()
    if old_blender_folder:
        one_blender_folder = os.path.dirname(old_blender_folder)
        blender_folder = os.path.dirname(one_blender_folder)

def on_start(dummy):
    global local_time_at_start
    local_time_at_start = time.time()
    print(f'hello dost time toh dekh {local_time_at_start}')





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

    

    def execute(self, context):
        selected_folder = context.scene.monitor_folder
        temporary_folder = None  # Define temporary_folder outside the if block

        if selected_folder == 'DOWNLOADS':
            if is_blend_file_saved():
                threading.Thread(target=organise, daemon=True, args=(
                    '0', blender_folder, local_time_at_start)).start()

            else:
                temporary_folder = os.path.join(get_downloads_folder(), "Temp")
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
