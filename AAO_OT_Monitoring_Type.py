import bpy
import os
import time
import threading
from AAO_UT_FileHandler      import organise
from AAO_OT_Onclick_Organise import is_blend_file_saved
from AAO_OT_Onclick_Organise import get_downloads_folder
from AAO_OT_Onclick_Organise import create_folder
from AAO_OT_Onclick_Organise import local_time_at_start
from AAO_OT_Onclick_Organise import blender_folder

stop_event = threading.Event()
def monitoring_type_prop_update_handler(self, context):
    if self.monitoring_type_prop == 'on-click':
        stop_event.set() 
    
        
class ENUM_PROPS_monitoring_type(bpy.types.PropertyGroup):
    bpy.types.Scene.monitoring_type_prop = bpy.props.EnumProperty(
            items=[
                ('REALTIME','Real-time','Organises folder in real-time'),
                ('on-click','On-click','Organises folder on click'),
            ],
            default='on-click',
            update=monitoring_type_prop_update_handler
        )

class ENUM_PROPS_delay_time(bpy.types.PropertyGroup):
    bpy.types.Scene.delay_time_prop = bpy.props.EnumProperty(
        items=[
            ('THREE','3 Seconds','Orgnises folder every three seconds'),
            ('SEVEN','7 Seconds','Orgnises folder every seven seconds'),
            ('THREE','10 Seconds','Orgnises folder every ten seconds')
        ],
        default='THREE'
    )

def realtime_monitoring(self,context,stop_event):
        while not stop_event.is_set():
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
                    print("realtime pe time: ",local_time_at_start)
                    organise('0', temporary_folder,local_time_at_start)                
            else:
                if is_blend_file_saved():
                    organise('1', blender_folder, local_time_at_start)
                else:
                    self.report({'ERROR'},"Blender file has not been saved. Please save your Blender file before utilizing this option.")
                    context.scene.monitor_folder='DOWNLOADS'    
                
            if context.scene.delay_time_prop == 'THREE':
                    print("delay hoga jee 3 sec")
                    time.sleep(3)
            elif context.scene.delay_time_prop == 'SEVEN':
                    print("delay hoga jee 7 sec")
                    time.sleep(7)
            else:
                    print("delay hoga jee 10 sec")
                    time.sleep(10)
        
    
            

class OBJECT_OT_monitor_type(bpy.types.Operator):
    bl_label="Start"
    bl_idname='object.realtimeops'
    bl_description='Real-time monitoring will start'

    
    

    def execute(self, context):
        global stop_event
        stop_event.clear()
        
        threading.Thread(target=realtime_monitoring,daemon=True, args=(self,context,stop_event)).start()
        
        
        self.report({'INFO'},"Real-time monitoring has started.")

        
        return {'FINISHED'}





