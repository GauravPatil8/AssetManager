import bpy
class ENUM_PROPS_monitoring_type(bpy.types.PropertyGroup):
    bpy.types.Scene.monitoring_type_prop = bpy.props.EnumProperty(
            items=[
                ('REALTIME','Real-time','Organises folder in real-time'),
                ('on-click','On-click','Organises folder on click'),
            ],
            default='on-click'
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


class OBJECT_OT_monitor_type(bpy.types.Operator):
    bl_label="Start"
    bl_idname='object.realtimeops'
    bl_description='Real-time monitoring will start'

    def execute(self,context):
        print("Realtime hora bhai")
        return {'FINISHED'}
