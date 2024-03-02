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
        
        layout.label(text="Folder presets:")
        layout.prop(scene,"folder_presets",text='')
        


        box_up = layout.box()
        box_up.label(text='Select organising type:')
        box_up.prop(scene, 'monitoring_type_prop', text='')
        if context.scene.monitoring_type_prop == 'REALTIME':
            box_up.prop(scene, 'delay_time_prop', text='Delay Time')
            box_up.operator("object.realtimeops", text='Start')
        else:
            box_up.operator('object.onclickorganise', text="Organise", text_ctxt='Organise downloaded files')

    
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.scene, "change_folder_name", text="Change Folder Name")
        
        if context.scene.change_folder_name:
            box.prop(context.scene, "folder_name", text="Select Folder Name")
            box.prop(context.scene, "custom_folder_name", text="Enter Folder Name")
            box.operator("object.updatefoldername", text="Set")

        layout.separator()

        layout.operator("object.log", text="Log")

class OBJECT_PT_preset_creator(bpy.types.Panel):
    bl_label = "Preset Creator"
    bl_idname = "OBJECT_PT_presetcreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Organiser"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout=self.layout
        layout.label(text="acha hai")
