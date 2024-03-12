import bpy


class OBJECT_PT_AssetManagerUI(bpy.types.Panel):
    bl_label = "Real-time Asset Organiser"
    bl_idname = "OBJECT_PT_addonui"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Organiser"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Select folder to monitor:")
        layout.prop(scene, "monitor_folder", text="")

        # layout.separator()

        layout.label(text="Folder presets:")
        row_preset = layout.row()
        row_preset.prop(scene, "folder_presets", text='')
        row_preset.operator('ot.updateenum', text='', icon='FILE_REFRESH')

        layout.separator()

        box_up = layout.box()
        box_up.label(text='Select organising type:')
        box_up.prop(scene, 'monitoring_type_prop', text='')
        if context.scene.monitoring_type_prop == 'REALTIME':
            box_up.prop(scene, 'delay_time_prop', text='Delay Time')
            box_up.operator("object.realtimeops", text='Start')
        else:
            box_up.operator('object.onclickorganise', text="Organise",
                            text_ctxt='Organise downloaded files')

        layout.separator()
        layout.operator("object.log", text="Log")
