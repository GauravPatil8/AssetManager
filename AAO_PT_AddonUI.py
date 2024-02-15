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

        # Folder monitoring section
        layout.label(text="Select folder to monitor:")
        layout.prop(scene, "monitor_folder", text="")

        # Organizing type section
        box1 = layout.box()
        box1.label(text='Select organising type:')
        box1.prop(scene, 'monitoring_type_prop', text='')
        if context.scene.monitoring_type_prop == 'REALTIME':
            box1.prop(scene, 'delay_time_prop', text='Delay Time')
            box1.operator("object.realtimeops", text='Start')
        else:
            box1.operator('object.onclickorganise', text="Organise", text_ctxt='Organise downloaded files')

        # Change folder name section
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.scene, "change_folder_name", text="Change Folder Name")
        if context.scene.change_folder_name:
            box.prop(context.scene, "folder_name", text="Select Folder Name")
            box.prop(context.scene, "custom_folder_name", text="Enter Folder Name")
            box.operator("object.updatefoldername", text="Set")

        layout.separator()

        # Log section
        layout.operator("object.log", text="Log")
