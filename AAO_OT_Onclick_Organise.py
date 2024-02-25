import sys 
import bpy
import os
import time
import shutil
import threading
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)

from AAO_UT_FileHandler import organise
from AAO_UT_FileHandler import is_blend_file_saved
from AAO_UT_FileHandler import get_downloads_folder
from AAO_UT_FileHandler import create_folder
from AAO_UT_FileHandler import get_blendfile_folder
from AAO_UT_FileHandler import project_folder_name

blender_folder=None
save_count=0
local_time_at_start=None

def on_start(dummy):
    global local_time_at_start
    local_time_at_start=time.time()



def blender_folder_on_saved(dummy):
    global save_count
    global blender_folder
    blender_folder=get_blendfile_folder()
    if save_count==0:

       
        blender_folder=get_blendfile_folder()

        os.makedirs(os.path.join(blender_folder,project_folder_name),exist_ok=True)
        new_blender_folder=os.path.join(blender_folder,project_folder_name)

        old_file_path=bpy.data.filepath
        bpy.ops.wm.open_mainfile(filepath=old_file_path)

        shutil.move(bpy.data.filepath,new_blender_folder)

        new_file_path=os.path.join(blender_folder,project_folder_name,os.path.basename(old_file_path))
        bpy.ops.wm.save_mainfile(filepath=new_file_path)


        if os.path.exists(os.path.join(get_downloads_folder(),"Temp")):  
            for folder in os.listdir(os.path.join(get_downloads_folder(),"Temp")):
                shutil.move(os.path.join(get_downloads_folder(),"Temp",folder),blender_folder)
    
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
                threading.Thread(target=organise,daemon=True,args=('0', blender_folder, local_time_at_start)).start()
                

            else:
                temporary_folder = os.path.join(get_downloads_folder(), "Temp")
                create_folder(temporary_folder)
                print(temporary_folder)
                threading.Thread(target=organise,daemon=True,args=('0', temporary_folder,local_time_at_start)).start()
                self.report({'INFO'},"Organising Files")
                              
        else:
            if is_blend_file_saved():
                threading.Thread(target=organise,daemon=True,args=('1', blender_folder, local_time_at_start)).start()
                self.report({'INFO'},"Organising Files")
                
            else:
                self.report({'ERROR'},"Blender file has not been saved. Please save your Blender file before utilizing this option.")
                context.scene.monitor_folder='DOWNLOADS'
        
        return {'FINISHED'}

