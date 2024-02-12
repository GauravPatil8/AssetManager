import bpy

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

        
        sample_data = [
            ("Option 1", "This is the description for Option 1"),
            ("Option 2", "This is the description for Option 2"),
            ("Option 3", "This is the description for Option 3"),
            ("Option 4", "This is the description for Option 4"),
            ("Option 5", "This is the description for Option 5"),
            ("Option 6", "This is the description for Option 6"),
            ("Option 7", "This is the description for Option 7"),
            ("Option 8", "This is the description for Option 8"),
            ("Option 9", "This is the description for Option 9"),
            ("Option 10", "This is the description for Option 10"),
            ("Option 11", "This is the description for Option 11"),
            ("Option 12", "This is the description for Option 12"),
            ("Option 13", "This is the description for Option 13"),
            ("Option 14", "This is the description for Option 14"),
            ("Option 15", "This is the description for Option 15"),
            ("Option 16", "This is the description for Option 16"),
            ("Option 17", "This is the description for Option 17"),
            ("Option 18", "This is the description for Option 18"),
            ("Option 19", "This is the description for Option 19"),
            ("Option 20", "This is the description for Option 20")
        ]


        for option, description in list(reversed(sample_data)):
            layout.label(text=option,icon='MATERIAL')
            layout.label(text=description,icon='FOLDER_REDIRECT')
            layout.separator()


