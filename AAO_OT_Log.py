import bpy
from AAO_DB_FolderNames import changelog_table_in_memory
from AAO_DB_FolderNames import get_file_info_change_log

memory_connection=changelog_table_in_memory()

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
        
        file_data = []
        file_info=get_file_info_change_log(memory_connection)
        for row in file_info:
            file_data.append(row)

        for option, description in list(reversed(file_data)):
            layout.label(text=option,icon='MATERIAL')
            layout.label(text=description,icon='FOLDER_REDIRECT')
            layout.separator()


