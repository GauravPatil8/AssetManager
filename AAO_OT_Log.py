import bpy

file_data = []

class OBJECT_OT_log(bpy.types.Operator):
    bl_idname = "object.log"
    bl_label = "Redirection log"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description="File location log"

    def execute(self, context):
       
        bpy.ops.wm.call_menu(name=OBJECT_OT_log_popup.bl_idname)
        return {'FINISHED'}

class OBJECT_OT_log_popup(bpy.types.Menu):
    bl_idname = "OBJECT_MT_simple_popup"
    bl_label = "File location log"

    def draw(self, context):
        layout = self.layout

        
       
        if file_data != []:
            for file_name, file_path in list(reversed(file_data)):
                
                layout.label(text=file_name,icon='FILE')
                layout.label(text=file_path,icon='FOLDER_REDIRECT')
                layout.separator()
        else:
            layout.label(text="No file movement have been detected.",icon='INFO')


