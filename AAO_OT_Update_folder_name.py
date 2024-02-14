import bpy
import os
from AAO_DB_FolderNames import create_and_populate
from AAO_DB_FolderNames import fetch_folder_name
from AAO_DB_FolderNames import update_folder_name
from AAO_OT_Onclick_Organise import blender_folder
from AAO_UT_FileHandler import database_connection

def get_downloads_folder():
    home_directory=os.path.expanduser('~')
    return os.path.join(home_directory,'Downloads')

def is_blend_file_saved():
    if bpy.data.filepath == "":
        return False
    else:
        return True
    
bpy.types.Scene.change_folder_name = bpy.props.BoolProperty(
        name="Change Folder Name",
        description="Enable Changing Folder Name",
        default=False,  
    )

bpy.types.Scene.folder_name = bpy.props.EnumProperty(
        items=[
            ('project_files', 'Project Files', 'Project Files'),
            ('image_files', 'Image Files', 'Image Files'),
            ('mocap_files', 'Mocap Files', 'Mocap Files'),
            ('model_files', 'Model Files', 'Model Files'),
        ],
        default='project_files',
    )


def change_in_system(old_folder_name,index):
    if is_blend_file_saved():
        for folder in os.listdir(blender_folder):
                    if folder==old_folder_name:
                        old_folder_path=os.path.join(blender_folder,old_folder_name)
                        new_folder_path=os.path.join(blender_folder,fetch_folder_name(database_connection,index))
                        os.rename(old_folder_path,new_folder_path)
    else:
        temp_folder=os.path.join(get_downloads_folder(),"Temp")
        for folder in os.listdir(temp_folder):
                    if folder==old_folder_name:
                        old_folder_path=os.path.join(temp_folder,old_folder_name)
                        new_folder_path=os.path.join(temp_folder,fetch_folder_name(database_connection,index))
                        os.rename(old_folder_path,new_folder_path)
    

class OBJECT_OT_update_foldername(bpy.types.Operator):
    bl_label="Change_foldername"
    bl_idname="object.updatefoldername"

    def execute(self,context):
        
        folder_name=context.scene.custom_folder_name
        selected_option=context.scene.folder_name
        if folder_name !="":
            if selected_option=='project_files':
                old_folder_name=fetch_folder_name(database_connection,2)
                update_folder_name(database_connection,2,folder_name)
                self.report({'INFO'},"Folder name updated successfully")
                change_in_system(old_folder_name,2)
                
            elif selected_option=='image_files':
                old_folder_name=fetch_folder_name(database_connection,1)
                update_folder_name(database_connection,1,folder_name)
                self.report({'INFO'},"Folder name updated successfully")
                change_in_system(old_folder_name,1)
            
            elif selected_option=='mocap_files':
                old_folder_name=fetch_folder_name(database_connection,4)
                update_folder_name(database_connection,4,folder_name)
                self.report({'INFO'},"Folder name updated successfully")
                change_in_system(old_folder_name,4)

            elif selected_option=='model_files':
                old_folder_name=fetch_folder_name(database_connection,3)
                update_folder_name(database_connection,3,folder_name)
                self.report({'INFO'},"Folder name updated successfully")
                change_in_system(old_folder_name,3)
        else:
            self.report({'ERROR'},"Please input a valid name")
            


        context.scene.custom_folder_name=""
        return {'FINISHED'}