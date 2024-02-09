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