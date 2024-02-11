import bpy 

class OBJECT_PT_AssetManagerUI(bpy.types.Panel):
    bl_label="Real-time Asset Organiser"
    bl_idname="OBJECT_PT_addonui"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="Asset Organiser"

    def draw(self, context):
        layout=self.layout
        scene=context.scene

        layout.label(text="Select folder to monitor: ")

        layout.prop(scene,"monitor_folder",text="")

        layout.operator('object.onclickorganise',text="Organise",text_ctxt='Organise downloaded files')

        layout.separator()

        box = layout.box()
        row = box.row(align=True)
        row.prop(context.scene, "change_folder_name", text="Change Folder Name")

        if context.scene.change_folder_name:
            box.prop(context.scene, "folder_name", text="Select Folder Name")

            box.prop(context.scene, "custom_folder_name", text="Enter Folder Name")

            box.operator("object.updatefoldername", text="Set")
            box.prop(context.scene, "project_specific", text="Project Specific")