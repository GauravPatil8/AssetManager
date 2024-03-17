import bpy
import os
import json
from bpy.types import Context, Operator
from bpy.props import StringProperty
from AAO_UT_FileHandler import get_package_path
from AAO_UT_FileHandler import path_constructor

subdirectories_relpath_dict = {}
json_data = {}
selected_folder_path = None
preset_list = [('DEFAULT', 'Default',
                'Stores downloaded files in a simple folder structure based on their type'),]
package_path = get_package_path()
subdirectory = []
target_folder = os.path.join(package_path, "Presets")


def update_folder_path(self,context):
        path_constructor()

def reload_panel():
    bpy.utils.unregister_class(OBJECT_PT_preset_creator)
    bpy.utils.register_class(OBJECT_PT_preset_creator)


def duplicate_tags_checker(context):
    seen = set()
    for tag in context.scene.enum_properties:
        if tag.value != 'NONE' and tag.value in seen:
            return True
        seen.add(tag.value)
    return False


def generator_list(self, context):
    global preset_list
    preset_list[1:] = []
    for file in os.listdir(target_folder):
        if os.path.isfile(os.path.join(target_folder, file)) and file != 'Default.db':
            file_name = file.split('.')[0]
            file_description = ''
            preset_list.append(tuple([file_name, file_name, file_description]))
    return preset_list


def get_subdirectories(directory):

    subdirectories = []

    for item in os.listdir(directory):

        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            base_folder_name = os.path.basename(item_path)
            subdirectories.append(base_folder_name)
            subdirectories_relpath_dict[base_folder_name] = os.path.relpath(
                item_path, selected_folder_path)
            subdirectories.extend(get_subdirectories(item_path))
    return subdirectories


class ENUM_PROPS_Tags(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()  # type: ignore
    value: bpy.props.EnumProperty(
        items=[
            ('NONE', 'none', ''),
            ('PROJECT', 'project_files', ''),
            ('MODEL', 'model_files', ''),
            ('IMAGE', 'image_files', ''),
            ('MOCAP', 'mocap_files', ''),
            ('MATERIAL', 'material_files', ''),
            ('VIDEO', 'video_files', ''),
            ('AUDIO', 'audio_files', '')
        ],
        name="Value"
    )  # type: ignore


class OBJECT_OT_update_preset_list(Operator):
    bl_idname = 'ot.updateenum'
    bl_label = 'update'

    def execute(self, context):
        global preset_list
        preset_list[1:] = []
        for file in os.listdir(target_folder):
            if os.path.isfile(os.path.join(target_folder, file)) and file != 'Default.db':
                file_name = file.split('.')[0]
                file_description = ''
                preset_list.append(
                    tuple([file_name, file_name, file_description]))
        bpy.types.Scene.folder_presets = bpy.props.EnumProperty(
            items=preset_list,
            description="Select a folder structure",
            default='DEFAULT',
        )
        return {'FINISHED'}


class STRING_PROPS_preset_name(bpy.types.PropertyGroup):
    bpy.types.Scene.preset_name = bpy.props.StringProperty(
        name="Enter Preset Name",
        description="Enter Preset name",
        default="",
       
    )


class STRING_PROPS_preset_analysis_folder(bpy.types.PropertyGroup):
    bpy.types.Scene.preset_analysis_folder = bpy.props.StringProperty(
        name="Select Folder",
        description="Select folder to be Analysied",
        default="",
    )


class OPEN_FOLDER_OT_OpenFolder(Operator):
    bl_idname = "folder_selector.open_folder"
    bl_label = "Open Folder"
    bl_description = "Select a folder"

    filepath: StringProperty(subtype="DIR_PATH")  # type: ignore

    def execute(self, context):
        global selected_folder_path
        global subdirectories_relpath_dict
        global json_data
        global subdirectory

        selected_folder_path = self.filepath

        subdirectories = get_subdirectories(selected_folder_path)
        
        subdirectory = subdirectories

        context.scene.preset_analysis_folder = selected_folder_path
        

        for sub_dir in subdirectories:
            new_enum_property = context.scene.enum_properties.add()
            new_enum_property.name = sub_dir
            new_enum_property.value = "NONE"
        reload_panel()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ENUM_PROPS_folder_presets(bpy.types.PropertyGroup):
    global preset_list
    for file in os.listdir(target_folder):
        if os.path.isfile(os.path.join(target_folder, file)) and file != 'Default.db':
            file_name = file.split('.')[0]
            file_description = ''
            preset_list.append(tuple([file_name, file_name, file_description]))

    bpy.types.Scene.folder_presets = bpy.props.EnumProperty(
        items=preset_list,
        description="Select a folder structure",
        default='DEFAULT',
        update=update_folder_path
    )


class OBJECT_OT_save_preset(bpy.types.Operator):
    bl_label = 'Save Preset'
    bl_idname = 'object.savepreset'

    def execute(self, context: Context):
        global selected_folder_path
        global subdirectories
        global subdirectories_relpath_dict
        global json_data
        if context.scene.preset_name != '':

            if not duplicate_tags_checker(context):
                subdir_keys = list(subdirectories_relpath_dict.keys())

                for i, enum_property in enumerate(context.scene.enum_properties):
                    if enum_property.name != subdir_keys[i]:
                        path = subdirectories_relpath_dict[subdir_keys[i]]
                        base_dir = os.path.dirname(path)
                        final_path = os.path.join(base_dir, enum_property.name)
                        json_data[enum_property.value] = final_path
                    else:
                        path = subdirectories_relpath_dict[subdir_keys[i]]
                        json_data[enum_property.value] = path

                    json_preset_path = os.path.join(
                        package_path, 'Presets', context.scene.preset_name+'.json')
                    with open(json_preset_path, 'w') as json_file:
                        json.dump(json_data, json_file, indent=4)
                self.report(
                    {'INFO'}, f'{context.scene.preset_name} preset saved')
                subdirectory.clear()
                subdirectories_relpath_dict.clear()
                json_data.clear()
                context.scene.preset_name = ''
                context.scene.preset_analysis_folder = ''
            else:
                self.report(
                    {'ERROR'}, 'Select distinct tags for each directory')

        else:
            self.report({'ERROR'}, "Please name your preset")
        return {'FINISHED'}


class OBJECT_PT_preset_creator(bpy.types.Panel):
    bl_label = "Preset Creator"
    bl_idname = "OBJECT_PT_presetcreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Organiser"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global subdirectories
        layout = self.layout

        layout.label(text='Select a folder')
        row = layout.row()
        row.prop(context.scene, 'preset_analysis_folder',
                 text='', icon='FILE_FOLDER')
        row.operator('folder_selector.open_folder',
                     icon='FILE_FOLDER', text='')
        
        if subdirectory != []:
            for enum_property in context.scene.enum_properties:
                new_row = layout.row()
                new_row.prop(enum_property, "name", text="")
                new_row.prop(enum_property, "value", text="")
            layout.prop(context.scene, 'preset_name', text="Enter preset name")
            layout.operator('object.savepreset', text='Save Preset')


        
