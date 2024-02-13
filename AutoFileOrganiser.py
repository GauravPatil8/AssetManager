#Folder Names List in Database:
# ('1',"Textures"),
# ('2',"Project_Files"),
# ('3',"Models"),
# ('4',"Mocap_data")

#CODE STARTS:

import sqlite3
import time
import bpy
import threading
from AAO_UT_FileHandler import organise
from AAO_UT_FileHandler import get_downloads_folder
from AAO_UT_FileHandler import get_blendfile_folder
from AAO_DB_FolderNames import create_and_populate
from AAO_DB_FolderNames import fetch_folder_name
from AAO_DB_FolderNames import update_folder_name
from AAO_DB_FolderNames import psfn_fetch_folder_name
from AAO_DB_FolderNames import psfn_createT
from AAO_DB_FolderNames import psfn_closeconn
from AAO_DB_FolderNames import psfn_updateName
from AAO_DB_FolderNames import table_inMemory
from AAO_DB_FolderNames import insert_inMemory
from AAO_DB_FolderNames import close_connection



localtime_atStart=time.time()
connection=sqlite3.connect(':memory:') # temporary db banaya memory ke andar localtime store karne keliye

db_conn=create_and_populate() #database banra
folder_name_flag='0' #idhar function daal diyo
if folder_name_flag =='0':
    images_folder_name=fetch_folder_name(db_conn,'1')
    project_folder_name=fetch_folder_name(db_conn,'2')
    model_folder_name=fetch_folder_name(db_conn,'3')
    mocap_folder_name=fetch_folder_name(db_conn,'4')
else:
    images_folder_name=psfn_fetch_folder_name('1')
    project_folder_name=psfn_fetch_folder_name('2')
    model_folder_name=psfn_fetch_folder_name('3')
    mocap_folder_name=psfn_fetch_folder_name('4')
#upar wala code har bar start hone par run hona mangta

##### BLENDER UI AND OPERATORS ######
def is_blend_file_saved():
    if bpy.data.filepath == "":
        return False
    else:
        return True
    
class SimpleErrorDialogOperator(bpy.types.Operator):
    bl_idname = "object.simple_error_dialog"
    bl_label = "Show Error Dialog"
    
    # error_message: bpy.props.StringProperty(default="This is a sample error message.")
    
    def execute(self, context):
        # Display a popup dialog box with the error message
        bpy.context.window_manager.popup_menu(lambda menu, context: self.popup_function(menu, context, self.error_message),
                                               title="Error", icon='ERROR')
        return {'FINISHED'}

    def popup_function(self, menu, context, error_message):
        layout = menu.layout
        layout.label(text=error_message)

    
class OBJECT_PT_assetOrganiserUI(bpy.types.Panel):
    bl_label="Asset Organiser"
    bl_idname="PT_Auto_AO"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="Asset Organiser"

    def draw(self,context):
        layout = self.layout

        # Folder Monitoring Option
        layout.label(text="Select Folder to Monitor:")
        layout.prop(context.scene, "monitor_folder", text="")

        # Realtime bool operator
        layout.separator()
        row = layout.row(align=True)
        row.prop(context.scene, "realtime", text="Enable Realtime Monitoring")

        # Change Folder Name bool operator and user input
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.scene, "change_folder_name", text="Change Folder Name")
        if context.scene.change_folder_name:
            box.prop(context.scene, "folder_name", text="Select Folder Name")
            box.prop(context.scene, "custom_folder_name", text="Custom Folder Name")
            
            # New bool operator for "Project Specific"
            box.prop(context.scene, "project_specific", text="Project Specific")

        # Always show Change Log operator button
        layout.separator()
        layout.operator("object.change_log_operator", text="Change Log")

        if not context.scene.realtime:
            layout.separator()
            row = layout.row(align=True)
            row.operator("object.organize_folder_operator", text="Organize Folder")

# class OBJECT_OT_MonitorFolderOperator(bpy.types.Operator):
#     bl_label = "Monitor Folder Operator"
#     bl_idname = "object.monitor_folder_operator"

#     _thread = None
#     selected_folder = None  # Class attribute to store selected_folder

#     def execute(self, context):

#         monitor_option = bpy.context.scene.monitor_folder  # Assuming you have a property named 'monitor_option'

#         # Set 'selected_folder' based on the user's choice
#         if monitor_option == 'downloads':
#             self.selected_folder = get_downloads_folder()

#         elif monitor_option == 'files':
#             self.selected_folder = get_blendfile_folder()

#         else:
#             # Handle the case when the user's choice is unexpected
#             self.selected_folder = get_downloads_folder()  # Replace this with an appropriate default

#         if context.scene.realtime:
#             self.report({'INFO'}, f"Realtime Monitoring of {self.selected_folder} Folder")
#             # Start a new thread for monitoring
#             self._thread = threading.Thread(target=self.realtime_monitoring_thread)
#             self._thread.start()
#         else:
#             self.report({'INFO'}, f"Monitoring {self.selected_folder} Folder")
#             # Perform non-realtime monitoring directly
#             self.organise()

#         return {'FINISHED'}

#     def realtime_monitoring_thread(self):
#         while bpy.context.scene.realtime:
#             time.sleep(1)
#             # Perform realtime monitoring in a separate thread
#             self.organise()

#         self.report({'INFO'}, "Realtime Monitoring Stopped.")

#     def organise(self):
#         # Call the organise function with the stored selected_folder
#         organise(self.selected_folder)

#     def cancel(self, context):
#         # Stop the thread when the operator is canceled
#         if self._thread and self._thread.is_alive():
#             bpy.context.scene.realtime = False  # Stop the realtime condition
#             self._thread.join()  # Wait for the thread to finis
            

bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('downloads', 'Monitor Downloads Folder', 'Monitor Downloads Folder'),
            ('files', 'Monitor File Folder', 'Monitor File Folder'),
        ],
        default='downloads',
    )
   
class OBJECT_OT_OrganizeFolderOperator(bpy.types.Operator):
    bl_label = "Organize Folder Operator"
    bl_idname = "object.organize_folder_operator"

    def execute(self, context):

        self.report({'INFO'}, "Organizing Folder")

        

        folder_to_monitor=context.scene.monitor_folder

        if is_blend_file_saved():
            destination_folder=get_blendfile_folder()
        else:
            destination_folder=None


        if folder_to_monitor =="downloads":
            src_folder=get_downloads_folder()
            
        else:
            if is_blend_file_saved():
                src_folder=get_blendfile_folder()
                
            else:
                bpy.ops.object.simple_error_dialog(error_message="Blend file is not saved, and monitor_folder is not 'downloads'")
                bpy.context.scene.monitor_folder = 'downloads'
                return {'CANCELLED'}


        organise(src_folder,destination_folder,localtime_atStart)
        return {'FINISHED'}
    
class OBJECT_OT_ChangeLogOperator(bpy.types.Operator):
    bl_label = "Change Log Operator"
    bl_idname = "object.change_log_operator"

    def execute(self, context):
        # Create a text block with your custom text
        bpy.data.texts.new(name="ChangeLogText").write("bing chilling")

        # Create the popup displaying the text
        bpy.context.window_manager.popup_menu(draw_func, title="Change Log")

        return {'FINISHED'}
    
def draw_func(self, context):
    layout = self.layout
    text_block = bpy.data.texts.get("ChangeLogText")

    if text_block:
        # Display the text block content in the popup
        layout.label(text=text_block.as_string(), icon='TEXT')
    else:
        layout.label(text="No change log available.")

def menu_func(self, context):
    # No need to add OBJECT_OT_MonitorFolderOperator to the layout
    pass


def on_start():
    print(f"Time at start of program: {localtime_atStart}")
    table_inMemory(connection)
    insert_inMemory(connection,localtime_atStart)
    

def on_exit():
    connection.close()
    close_connection()




def register():
    
    bpy.app.handlers.load_post.append(on_start)
    bpy.app.handlers.save_pre.append(on_exit)
    bpy.utils.register_class(OBJECT_PT_assetOrganiserUI)
    # bpy.utils.register_class(OBJECT_OT_MonitorFolderOperator)
    bpy.utils.register_class(OBJECT_OT_OrganizeFolderOperator)
    bpy.utils.register_class(OBJECT_OT_ChangeLogOperator)

    bpy.types.Scene.realtime = bpy.props.BoolProperty(
        name="Realtime Monitoring",
        description="Enable Realtime Monitoring",
        default=False,
    )
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
    bpy.types.Scene.custom_folder_name = bpy.props.StringProperty(
        name="Custom Folder Name",
        description="Enter a custom folder name",
        default="",
    )
    bpy.types.Scene.project_specific = bpy.props.BoolProperty(
        name="Project Specific",
        description="Enable Project Specific",
        default=False,
    )
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    
    bpy.app.handlers.load_post.remove(on_start)
    bpy.app.handlers.save_pre.remove(on_exit)
    bpy.utils.unregister_class(OBJECT_PT_assetOrganiserUI)
    # bpy.utils.unregister_class(OBJECT_OT_MonitorFolderOperator)
    bpy.utils.unregister_class(OBJECT_OT_OrganizeFolderOperator)
    bpy.utils.unregister_class(OBJECT_OT_ChangeLogOperator)
    del bpy.types.Scene.monitor_folder
    del bpy.types.Scene.realtime
    del bpy.types.Scene.change_folder_name
    del bpy.types.Scene.folder_name
    del bpy.types.Scene.custom_folder_name
    del bpy.types.Scene.project_specific
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

register()
