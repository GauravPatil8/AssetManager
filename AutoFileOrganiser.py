#Folder Names List in Database:
# ('1',"Textures"),
# ('2',"Project_Files"),
# ('3',"Models"),
# ('4',"Mocap_data")

#CODE STARTS:
import sqlite3
import os
import shutil
import time
import bpy
import threading
from Folder_namedb import create_and_populate
from Folder_namedb import fetch_folder_name
from Folder_namedb import update_folder_name
from Folder_namedb import psfn_fetch_folder_name
from Folder_namedb import psfn_createT
from Folder_namedb import psfn_closeconn
from Folder_namedb import psfn_updateName
from Folder_namedb import table_inMemory
from Folder_namedb import insert_inMemory
from Folder_namedb import close_connection

folder_name_flag=None #isse dekh liyo bhai

localtime_atStart=time.time()
connection=sqlite3.connect(':memory:') # temporary db banaya memory ke andar localtime store karne keliye
organise_lock = threading.Lock() #THREAD SAFTEY KE LIYE

# execute everytime at the beginning code (GLOBALLY DECLARED):
project_files   = ['max','3ds','blend','c4d','bgeo','geo']
model_files     = ['obj','fbx','usdz','dae','usd*','ply','glb','gltf','x3d']
image_files     = ['png','jpg','jpeg','exr','tiff','webp','gif','psd','indd','raw','svg','ai','tif',]
mocap_files     = ['bvh']


bfp=bpy.data.filepath
if bfp:
    blender_folder_path=bpy.path.abspath("//")


db_conn=create_and_populate() #database banra
#upar wala code har bar start hone par run hona mangta


def set_folder_names():
    global images_folder_name   
    global project_folder_name  
    global model_folder_name    
    global mocap_folder_name   

    if folder_name_flag =='0':
        images_folder_name=fetch_folder_name('1')
        project_folder_name=fetch_folder_name('2')
        model_folder_name=fetch_folder_name('3')
        mocap_folder_name=fetch_folder_name('4')
    else:
        images_folder_name=psfn_fetch_folder_name('1')
        project_folder_name=psfn_fetch_folder_name('2')
        model_folder_name=psfn_fetch_folder_name('3')
        mocap_folder_name=psfn_fetch_folder_name('4')



def folder_to_monitor(Flag):
    if Flag=='0':
        return get_downloads_folder()
    else: 
        if blender_folder_path==None:
                pass
        # return blender_folder_path

def create_folder(folder_path):
    os.makedirs(folder_path,exist_ok=True)



def get_downloads_folder():
    home_directory=os.path.expanduser('~')

    if os.name=='posix':
        downloads_folder=os.path.join(home_directory,'Downloads')
    
    elif os.name=='nt':
        downloads_folder=os.path.join(home_directory,'Downloads')
    else:
        raise OSError("Unsupported Operating System")
    return downloads_folder



def organise():
    src_folder=folder_to_monitor()
    dest_folder=blender_folder_path


    with organise_lock:
        for file in os.listdir(src_folder):
                
                file_path=os.path.join(src_folder,file)

                if os.path.getmtime(file_path)>=localtime_atStart: # yaha file ka time check karra agar program start hone se pehle koi file hogi toh uspe operation nai hoga

                    if os.path.isfile(file_path):
                        extension=file.split('.')[-1] # file ka extension extract karra hai

                        if extension in image_files:

                            images_folder_path=os.path.join(dest_folder,images_folder_name)
                            create_folder(images_folder_path)
                            shutil.move(file_path,images_folder_path)

                        elif extension in project_files:

                            project_folder_path=os.path.join(dest_folder,project_folder_name)
                            create_folder(project_folder_path)
                            shutil.move(file_path,project_folder_path)

                        elif extension in model_files:

                            model_folder_path=os.path.join(dest_folder,model_folder_name)
                            create_folder(model_folder_path)
                            shutil.move(file_path,model_folder_path)
                        
                        elif extension in mocap_files:

                            mocap_folder_path=os.path.join(dest_folder,mocap_folder_name)
                            create_folder(mocap_folder_path)
                            shutil.move(file_path,mocap_folder_path)
            




##### BLENDER UI AND OPERATORS ######

class assetOrganiserUI(bpy.types.Panel):
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

class OBJECT_OT_MonitorFolderOperator(bpy.types.Operator):
    bl_label = "Monitor Folder Operator"
    bl_idname = "object.monitor_folder_operator"

    _monitoring_thread = None

    def modal_handler(self, context):
        if not context.scene.realtime:
            self.report({'INFO'}, "Realtime Monitoring Stopped.")
            return {'CANCELLED'}

        selected_folder = context.scene.monitor_folder
        self.report({'INFO'}, f"Realtime Monitoring of {selected_folder} Folder")
        organise()  # Modify as needed

        # Set the monitoring interval (in seconds)
        interval = 5
        return interval

    def modal(self, context, event):
        if event.type == 'TIMER':
            interval = self.modal_handler(context)
            return {'PASS_THROUGH'} if interval is None else {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        if context.scene.realtime:
            self.report({'INFO'}, "Realtime Monitoring Started...")
            # Start a new thread for monitoring
            self._monitoring_thread = threading.Thread(target=self.monitoring_thread, args=(context,))
            self._monitoring_thread.start()
            bpy.app.timers.register(self.modal, first_interval=0.1)
        else:
            self.report({'INFO'}, "Realtime Monitoring Stopped.")
        return {'FINISHED'}

    def monitoring_thread(self, context):
        while context.scene.realtime:
            time.sleep(3)  # Sleep for a short duration to allow the main thread to handle modal updates

        self.report({'INFO'}, "Realtime Monitoring Stopped.")
    
class OBJECT_OT_OrganizeFolderOperator(bpy.types.Operator):
    bl_label = "Organize Folder Operator"
    bl_idname = "object.organize_folder_operator"

    def execute(self, context):
        self.report({'INFO'}, "Organizing Folder")
        organise()
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
    table_inMemory(connection)
    insert_inMemory(connection,localtime_atStart)
    

def on_exit():
    connection.close()
    close_connection()




def register():
    
    bpy.app.handlers.load_post.append(on_start)
    bpy.app.handlers.save_pre.append(on_exit)
    bpy.utils.register_class(assetOrganiserUI)
    bpy.utils.register_class(OBJECT_OT_MonitorFolderOperator)
    bpy.utils.register_class(OBJECT_OT_OrganizeFolderOperator)
    bpy.utils.register_class(OBJECT_OT_ChangeLogOperator)
    bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('downloads', 'Monitor Downloads Folder', 'Monitor Downloads Folder'),
            ('files', 'Monitor File Folder', 'Monitor File Folder'),
        ],
        default='downloads',
    )
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
    bpy.utils.unregister_class(assetOrganiserUI)
    bpy.utils.unregister_class(OBJECT_OT_MonitorFolderOperator)
    bpy.utils.unregister_class(OBJECT_OT_OrganizeFolderOperator)
    bpy.utils.unregister_class(OBJECT_OT_ChangeLogOperator)
    del bpy.types.Scene.monitor_folder
    del bpy.types.Scene.realtime
    del bpy.types.Scene.change_folder_name
    del bpy.types.Scene.folder_name
    del bpy.types.Scene.custom_folder_name
    del bpy.types.Scene.project_specific
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

# register()