import bpy
import os
import time
import threading
from aao_ut_filehandler import organise
from aao_ut_filehandler import temporary_folder_name
from aao_ot_onclick_organise import is_blend_file_saved
from aao_ot_onclick_organise import get_downloads_folder
from aao_ot_onclick_organise import get_blendfile_folder
from aao_ot_onclick_organise import create_folder
from aao_ut_filehandler import return_projectfile_name
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
        default='ONCLICKOPERATOR',
        update=monitoring_type_prop_update_handler,
    )


class ENUM_PROPS_delay_time(bpy.types.PropertyGroup):
    bpy.types.Scene.delay_time_prop = bpy.props.EnumProperty(
        items=[
            ('THREE', '3 Seconds', 'Orgnises folder every three seconds'),
            ('SEVEN', '7 Seconds', 'Orgnises folder every seven seconds'),
            ('THREE', '10 Seconds', 'Orgnises folder every ten seconds')
        ],
        default='THREE',
    )


def realtime_monitoring(self, context, stop_event,destination_folder):
    global report_flag
    report_flag = True
    while not stop_event.is_set():
        selected_folder = context.scene.monitor_folder
        temporary_folder = None  # Define temporary_folder outside the if block

        if selected_folder == 'DOWNLOADS':
            if is_blend_file_saved():
                organise('0', destination_folder, local_time_at_start)
            else:
                temporary_folder = os.path.join(get_downloads_folder(), temporary_folder_name)
                create_folder(temporary_folder)
                organise('0', temporary_folder, local_time_at_start)
        else:
            if is_blend_file_saved():
                organise('1', destination_folder, local_time_at_start)
            else:
                context.scene.monitor_folder = 'DOWNLOADS'

        if context.scene.delay_time_prop == 'THREE':
            time.sleep(3)
        elif context.scene.delay_time_prop == 'SEVEN':
            time.sleep(7)
        else:
            time.sleep(10)

class OBJECT_OT_monitor_type(bpy.types.Operator):
    bl_label = "Start"
    bl_idname = 'object.realtimeops'
    bl_description = 'Real-time monitoring will start'

    def execute(self, context):
        global thread_flag
        global stop_event
        global report_flag
        stop_event.clear()

        if report_flag==True:
            self.report({'WARNING'},f"Real-time monitoring has already started,currently monitoring {context.scene.monitor_folder}")
        else:
            if context.scene.monitor_folder != "DOWNLOADS":
                if is_blend_file_saved():
                    self.report({'INFO'}, "Real-time monitoring has started")
                    dest_blender_folder=get_blender_folder_path()

                    if thread_flag == False:
                        thread_flag = True
                        threading.Thread(target=realtime_monitoring, daemon=True, args=(
                            self, context, stop_event,dest_blender_folder)).start()
                        self.report({'INFO'}, f"Real-time monitoring has started,currently monitoring {context.scene.monitor_folder.label}")
                else:
                    self.report(
                        {'ERROR'}, "Blender file has not been saved. Please save your Blender file before utilizing this option.")
                    context.scene.monitor_folder = "DOWNLOADS"
            else:
                if thread_flag == False:
                    threading.Thread(target=realtime_monitoring, daemon=True, args=(
                        self, context, stop_event," ")).start()
                    self.report({'INFO'}, f"Real-time monitoring has started,currently monitoring {context.scene.monitor_folder}")
                    thread_flag = True
        return {'FINISHED'}
