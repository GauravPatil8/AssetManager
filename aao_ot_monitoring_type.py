import bpy
import os
import time
import threading
from aao_ut_filehandler import organise
from aao_ot_onclick_organise import get_downloads_folder
from aao_ot_onclick_organise import get_blendfile_folder
from aao_ut_filehandler import return_projectfile_name
from aao_ut_filehandler  import default_setter
from aao_ot_onclick_organise import local_time_at_start
report_flag=False
loop_flag=True
thread_flag = False

stop_event = threading.Event()

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

def monitoring_type_prop_update_handler(self, context):
    global thread_flag
    global report_flag

    if self.monitoring_type_prop == 'ONCLICKOPERATOR':
        stop_event.set()
        thread_flag = False
        report_flag = False
        


class ENUM_PROPS_monitoring_type(bpy.types.PropertyGroup):
    bpy.types.Scene.monitoring_type_prop = bpy.props.EnumProperty(
        items=[
            ('REALTIME', 'Real-time', 'Organises folder in real-time'),
            ('ONCLICKOPERATOR', 'On-click', 'Organises folder on click'),
        ],
        default=default_setter('M_type','ONCLICKOPERATOR'),
        update=monitoring_type_prop_update_handler,
    )
    


class ENUM_PROPS_delay_time(bpy.types.PropertyGroup):
    bpy.types.Scene.delay_time_prop = bpy.props.EnumProperty(
        items=[
            ('ONE', '1 Seconds', 'Orgnises folder after every one seconds'),
            ('THREE', '3 Seconds', 'Orgnises folder after every three seconds'),
            ('SEVEN', '7 Seconds', 'Orgnises folder after every seven seconds')
        ],
        default=default_setter('R_time','THREE'),
    )


def realtime_monitoring(self, context, stop_event,monitoring_folder,destination_folder):
    global report_flag
    report_flag = True
    while not stop_event.is_set():
        selected_folder = context.scene.monitor_folder

        if selected_folder == 'DOWNLOADS':
            if destination_folder!='':
                organise(get_downloads_folder(), destination_folder, local_time_at_start)
        else:
            if monitoring_folder!='':
                if destination_folder!='':
                    organise(monitoring_folder, destination_folder, local_time_at_start)
            else:
                context.scene.monitor_folder = 'DOWNLOADS'

        if context.scene.delay_time_prop == 'ONE':
            time.sleep(1)
        elif context.scene.delay_time_prop == 'THREE':
            time.sleep(3)
        else:
            time.sleep(7)

class OBJECT_OT_monitor_type(bpy.types.Operator):
    bl_label = "Start"
    bl_idname = 'object.realtimeops'
    bl_description = 'Real-time monitoring will start'

    def execute(self, context):
        global thread_flag
        global stop_event
        global report_flag
        stop_event.clear()
        folder_path_realtime=context.scene.folder_path
        destination_path_realtime=context.scene.destination_path
        if report_flag==True:
            self.report({'WARNING'},f"Real-time monitoring has already started,currently monitoring {context.scene.monitor_folder}")
        else:
            if context.scene.monitor_folder == "DOWNLOADS":
                if destination_path_realtime!='':
                    self.report({'INFO'}, "Real-time monitoring has started")
            
                    if thread_flag == False:
                        thread_flag = True
                        threading.Thread(target=realtime_monitoring, daemon=True, args=(
                            self, context, stop_event,get_downloads_folder(),destination_path_realtime)).start()
                        self.report({'INFO'}, f"Real-time monitoring has started,currently monitoring {context.scene.monitor_folder}")
                else:
                    self.report({'ERROR'}, "Select a destination folder.")
            else:
                if thread_flag == False:
                    if folder_path_realtime!='':
                        if destination_path_realtime!='':
                            threading.Thread(target=realtime_monitoring, daemon=True, args=(
                                self, context, stop_event,folder_path_realtime,destination_path_realtime)).start()
                            self.report({'INFO'}, f"Real-time monitoring has started,currently monitoring {context.scene.monitor_folder}")
                            thread_flag = True
                        else:
                            self.report({'ERROR'}, "Select a destination folder.")
                    else:
                        self.report({'ERROR'}, "Select a folder to monitor.")
                        context.scene.monitor_folder='DOWNLOADS'
        return {'FINISHED'}
