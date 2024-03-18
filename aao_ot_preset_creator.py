import bpy
import os
import json
from bpy.types import Context, Operator
from bpy.props import StringProperty
from aao_ut_filehandler import get_package_path
from aao_ut_filehandler import path_constructor

preset_folder_name="Presets"
subdirectories_relpath_dict = {}
json_data = {}
subdirectory = []
selected_folder_path = None
preset_list = [('DEFAULT', 'Default','Stores downloaded files in a simple folder structure based on their type'),]
package_path = get_package_path()
target_folder = os.path.join(package_path,preset_folder_name)

clearance_flag=False


def update_folder_path(self,context):
    path_constructor()

def reload_panel():
    bpy.utils.unregister_class(OBJECT_PT_preset_creator)
    bpy.utils.register_class(OBJECT_PT_preset_creator)


def duplicate_tags_checker(context):
    seen = set()
    for tag_enum in context.scene.enum_properties:
        if tag_enum.tag != 'NONE' and tag_enum.tag in seen:
            return True
        seen.add(tag_enum.tag)
    return False


def generator_list(self, context):
    global preset_list
    preset_list[1:] = []
    for file in os.listdir(target_folder):
        if os.path.isfile(os.path.join(target_folder, file)):
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
    tag: bpy.props.EnumProperty(
        items=[
            ('NONE', 'none', 'No Tags'),
            ('PROJECT', 'project_files', "This tag is designated for storing files with extensions such as 'max,' '3ds,' 'blend,' 'c4d,' 'bgeo,' and 'geo.' Any files with these extensions will be organized and kept in this folder."),
            ('MODEL', 'model_files', "This tag will be used to categorize and store files with specific extensions, including 'obj', 'fbx', 'usdz', 'dae', 'usd*', 'ply', 'glb', 'gltf', and 'x3d'. These files will be organized and kept in this designated folder."),
            ('IMAGE', 'image_files', "This tag designates a folder where files with the following extensions will be stored: ['png', 'jpg', 'jpeg', 'exr', 'tiff', 'webp', 'gif', 'psd', 'indd', 'raw', 'svg', 'ai', 'tif']. These file types will be saved in the specified location."),
            ('MATERIAL', 'material_files', "This tag designates a folder for storing files with specific extensions such as 'sbsar', 'spsm', 'spp', and 'sbs'."),
            ('VIDEO', 'video_files', "This tag designates a folder where files with extensions such as 'mov', 'mp4', 'mkv', 'avi', 'wmv', 'avchd', 'webm', and 'flv' will be organized and stored."),
            ('AUDIO', 'audio_files', "This tag designates the types of files that will be stored in a specific folder. It includes a variety of audio file extensions such as 'wav,' 'mp3,' 'flac,' 'ogg,' 'm3u,' 'acc,' 'wma,' 'midi,' 'aif,' 'm4a,' 'mpa,' and 'pls.'")
        ],
        name="tag"
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
        global clearance_flag
        indices_to_remove=[]
        enum_properties = context.scene.enum_properties
        selected_folder_path = self.filepath
        subdirectories = get_subdirectories(selected_folder_path)
            
        

        if clearance_flag==False: 
            clearance_flag=True
        else:
            for index,enum_property in enumerate(enum_properties):
                indices_to_remove.append(index)

            for index in reversed(indices_to_remove):
                enum_properties.remove(index)


        subdirectory = subdirectories

        context.scene.preset_analysis_folder = selected_folder_path
            

        for sub_dir in subdirectories:
                new_enum_property = context.scene.enum_properties.add()
                new_enum_property.name = sub_dir
                new_enum_property.tag = "NONE"
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
                        json_data[enum_property.tag] = final_path
                    else:
                        path = subdirectories_relpath_dict[subdir_keys[i]]
                        json_data[enum_property.tag] = path

                    json_preset_path = os.path.join(
                        package_path, preset_folder_name, context.scene.preset_name+'.json')
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
                new_row.prop(enum_property, "tag", text="")
            layout.prop(context.scene, 'preset_name', text="Enter preset name")
            layout.operator('object.savepreset', text='Save Preset')
