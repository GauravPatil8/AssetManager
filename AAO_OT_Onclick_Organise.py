import bpy

bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            ('downloads', 'Monitor Downloads Folder', 'Monitor Downloads Folder'),
            ('files', 'Monitor File Folder', 'Monitor File Folder'),
        ],
        default='downloads',
    )

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



