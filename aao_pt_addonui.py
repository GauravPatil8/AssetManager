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

        layout.label(text="Presets:")
        layout.prop(scene, "folder_presets", text='')
        row_preset = layout.row()
        row_preset.operator('ot.updateenum', text='Refresh', icon='FILE_REFRESH')
        row_preset.operator('ot.installpreset', text='Install', icon='IMPORT')
        row_preset.operator('ot.sharepreset', text='Share', icon='FOLDER_REDIRECT')
        row_preset.operator('ot.removepreset', text='Remove', icon='TRASH')

        box=layout.box()

        box.label(text="Select folder to monitor:")
        box.prop(scene, "monitor_folder", text="")
        
        if scene.monitor_folder!='DOWNLOADS':
            row=box.row()
            row.prop(scene,'folder_path',icon='FILE_FOLDER')
            row.operator('ot.foldertomonitor',text='',icon='FILE_FOLDER')
        box.label(text='Choose Destination Folder:')
        row=box.row()
        row.prop(scene,'destination_path',icon='FILE_FOLDER')
        row.operator('ot.foldertostore',text='',icon='FILE_FOLDER')

        layout.separator()

        box_up = layout.box()
        box_up.label(text='Select organising type:')
        box_up.prop(scene, 'monitoring_type_prop', text='')
        if context.scene.monitoring_type_prop == 'REALTIME':
            box_up.prop(scene, 'delay_time_prop', text='Delay Time')
            box_up.operator("object.realtimeops", text='Start')
        else:
            box_up.operator('object.onclickorganise', text="Organise",
                            text_ctxt='Organise downloaded files')

        layout.separator()
        layout.operator("object.log", text=" Transfer log")
