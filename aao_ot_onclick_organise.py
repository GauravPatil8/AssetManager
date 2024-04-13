from aao_ut_filehandler import get_downloads_folder
from aao_ut_filehandler import organise
from aao_ut_filehandler import return_projectfile_name
from aao_ut_filehandler import default_setter
from aao_pt_addonui     import OBJECT_PT_AssetManagerUI
from bpy.props import StringProperty
import bpy
import os
import time
import threading


##Global Variables###
loop_flag=True
local_time_at_start = None
folder_paths=default_setter('M_folder','')
destination_paths=default_setter('D_folder','')
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
###

def reload_ui():
    bpy.utils.unregister_class(OBJECT_PT_AssetManagerUI)
    bpy.utils.register_class(OBJECT_PT_AssetManagerUI)
class OBJECT_OT_monitoringfolder(bpy.types.Operator):
    bl_label=""
    bl_idname="ot.foldertomonitor"
    bl_description="share any preset from local device."

    filepath: StringProperty(subtype="DIR_PATH")  #type: ignore

    def execute(self, context):
        global folder_paths
        folder_paths = self.filepath
        context.scene.folder_path=folder_paths
        reload_ui()
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
        context.scene.destination_path=self.filepath
        reload_ui()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class STRING_PROPS_folder_path(bpy.types.PropertyGroup):
    bpy.types.Scene.folder_path = bpy.props.StringProperty(
        name="",
        description="Enter folder path",
        default=default_setter('M_folder',''),
       
    )
class STRING_PROPS_destination_path(bpy.types.PropertyGroup):
    bpy.types.Scene.destination_path = bpy.props.StringProperty(
        name="",
        description="Enter destination path",
        default=default_setter('D_folder',''),
       
    )

def on_start():
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
        default=default_setter('analysis_folder','DOWNLOADS'),
    )


class OBJECT_OT_Onclick_Organise(bpy.types.Operator):
    bl_label = 'onlick_organise'
    bl_idname = "object.onclickorganise"
    bl_description = "Clicking this organizes downloaded files"
    on_start()
    def execute(self, context):
        selected_folder = context.scene.monitor_folder
        if selected_folder == 'DOWNLOADS':
            if context.scene.destination_path!='':
                threading.Thread(target=organise, daemon=True, args=(
                    get_downloads_folder(), context.scene.destination_path, local_time_at_start)).start()
                self.report({'INFO'}, "Organising Files")
            else:
                self.report({'ERROR'}, "Select a destination folder.")

        else:
            if context.scene.folder_path!='':
                if context.scene.destination_path!='':
                    threading.Thread(target=organise, daemon=True, args=(
                        context.scene.folder_path, context.scene.destination_path, local_time_at_start)).start()
                    self.report({'INFO'}, "Organising Files")
                else:
                    self.report({'ERROR'}, "Select a destination folder.")
            else:
                self.report({'ERROR'}, "Select a folder to monitor.")
                context.scene.monitor_folder = 'DOWNLOADS'

        return {'FINISHED'}
