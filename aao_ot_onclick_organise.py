from aao_ut_filehandler import get_blendfile_folder
from aao_ut_filehandler import get_downloads_folder
from aao_ut_filehandler import organise
from aao_ut_filehandler import return_projectfile_name
from bpy.props import StringProperty
import bpy
import os
import time
import threading

##Global Variables###
loop_flag=True
local_time_at_start = None
folder_paths=''
destination_paths=''
###
class OBJECT_OT_monitoringfolder(bpy.types.Operator):
    bl_label=""
    bl_idname="ot.foldertomonitor"
    bl_description="share any preset from local device."

    filepath: StringProperty(subtype="DIR_PATH")  #type: ignore

    def execute(self, context):
        global folder_paths
        folder_paths = self.filepath
        context.scene.folder_path=folder_paths
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
class OBJECT_OT_destinationfolder(bpy.types.Operator):
    bl_label=""
    bl_idname="ot.foldertostore"
    bl_description="share any preset from local device."

    filepath: StringProperty(subtype="DIR_PATH")  #type: ignore

    def execute(self, context):
        global destination_paths
        destination_paths = self.filepath
        context.scene.destination_path=destination_paths
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class STRING_PROPS_folder_path(bpy.types.PropertyGroup):
    bpy.types.Scene.folder_path = bpy.props.StringProperty(
        name="",
        description="Enter folder path",
        default="",
       
    )
class STRING_PROPS_destination_path(bpy.types.PropertyGroup):
    bpy.types.Scene.destination_path = bpy.props.StringProperty(
        name="",
        description="Enter destination path",
        default="",
       
    )
def get_blender_folder_path():
    
    global loop_flag
    blender_folder = get_blendfile_folder()
    project_file_name=return_projectfile_name()
    while loop_flag:
        if os.path.basename(blender_folder)==project_file_name:
            loop_flag=False
        blender_folder = os.path.dirname(blender_folder)
    loop_flag=True
    return blender_folder

def on_start(dummy):
    global local_time_at_start
    local_time_at_start = time.time()


class ENUM_PROPS_monitor_folder(bpy.types.PropertyGroup):
    bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('DOWNLOADS', 'Monitor Downloads Folder',
             'This option enables monitoring of the downloads folder for newly added files.'),
            ('CUSTOMFOLDER', 'Select Folder To Monitor',
             'This option enables monitoring of the folder that you choose for newly added files.'),
        ],
        default='DOWNLOADS',
    )


class OBJECT_OT_Onclick_Organise(bpy.types.Operator):
    bl_label = 'onlick_organise'
    bl_idname = "object.onclickorganise"
    bl_description = "Clicking this organizes downloaded files"
    
    def execute(self, context):
        selected_folder = context.scene.monitor_folder
        if selected_folder == 'DOWNLOADS':
            if destination_paths!='':
                threading.Thread(target=organise, daemon=True, args=(
                    get_downloads_folder(), destination_paths, local_time_at_start)).start()
                self.report({'INFO'}, "Organising Files")

            else:
                self.report({'ERROR'}, "Select a destination folder.")

        else:
            if folder_paths!='':
                if destination_paths!='':
                    threading.Thread(target=organise, daemon=True, args=(
                        folder_paths, destination_paths, local_time_at_start)).start()
                    self.report({'INFO'}, "Organising Files")
                else:
                    self.report({'ERROR'}, "Select a destination folder.")

            else:
                self.report({'ERROR'}, "Select a folder to monitor.")
                context.scene.monitor_folder = 'DOWNLOADS'

        return {'FINISHED'}
