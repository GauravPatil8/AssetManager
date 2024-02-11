import bpy

bpy.types.Scene.change_folder_name = bpy.props.BoolProperty(
        name="Change Folder Name",
        description="Enable Changing Folder Name",
        default=False,  
    )

bpy.types.Scene.folder_name = bpy.props.EnumProperty(
        items=[
            ('project_files', 'Project Files', 'Project Files'),
            ('image_files', 'Image Files', 'Image Files'),
            ('mocap_files', 'Mocap Files', 'Mocap Files'),
            ('model_files', 'Model Files', 'Model Files'),
        ],
        default='project_files',
    )

bpy.types.Scene.project_specific = bpy.props.BoolProperty(
        name="Project Specific",
        description="Enable Project Specific",
        default=False,
    )


class OBJECT_OT_update_foldername(bpy.types.Operator):
    bl_label="Change_foldername"
    bl_idname="object.updatefoldername"

    def execute(self,context):
        #Working test
        printkarnekastring=context.scene.custom_folder_name
        selected_option=context.scene.folder_name
        print("ye enter kiya na bhai: ",printkarnekastring)
        print("ye select kiya na bhai: ",selected_option)
        context.scene.custom_folder_name=""
        return {'FINISHED'}