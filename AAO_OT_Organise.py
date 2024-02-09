import bpy

bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('downloads', 'Monitor Downloads Folder', 'Monitor Downloads Folder'),
            ('files', 'Monitor File Folder', 'Monitor File Folder'),
        ],
        default='downloads',
    )

class OBJECT_PT_AssetManagerUI(bpy.types.Panel):
    bl_label="Offline Organiser test"
    bl_idname="OBJECT_PT_addonui"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="File Manager"

    def draw(self, context):
        layout=self.layout
        scene=context.scene

        layout.label(text="Select folder to monitor: ")

        layout.prop(scene,"monitor_folder",text="")

        layout.operator('object.printfoldername',text="Print folder name")

class OBJECT_OT_Selectedfoldername(bpy.types.Operator):
    bl_label='Print folder name'
    bl_idname="object.printfoldername"

    def execute(self,context):

        selected_folder=context.scene.monitor_folder

        if selected_folder=='downloads':
            print("download folder selected hai bhai")
        else:
            print("Blendfile ka folder selected hai bhai")

        return {'FINISHED'}

classes=[OBJECT_PT_AssetManagerUI,OBJECT_OT_Selectedfoldername]
def register():
    for kls in classes:
        bpy.utils.register_class(kls)
    

def unregister():
    for kls in classes:
        bpy.utils.unregister_class(kls)

register()

