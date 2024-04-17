import os
import shutil
import bpy
import zipfile
import json
import datetime
from aao_ot_log import file_data
from aao_constants import PRESET_DEFAULT_ID,TAG_AUDIO,TAG_IMAGE,TAG_MATERIAL,TAG_MODEL,TAG_PROJECT,TAG_VIDEO,DEFAULT_IMAGE_DEST,DEFAULT_PROJECT_DEST,DEFAULT_MODEL_DEST,DEFAULT_AUDIO_DEST,DEFAULT_MATERIAL_DEST,DEFAULT_VIDEO_DEST,DEFAULT_TEMPORARY_DEST,DEFAULT_PRESET_DEST,ZIPMODE_KEY,PRESET_KEY

def get_package_path():
    script_path = os.path.abspath(__file__)
    return os.path.dirname(script_path)


blender_folder=''
filecount = 0
save_flag = False


package_path = get_package_path()
file_folder_path = os.path.join(package_path, DEFAULT_PRESET_DEST)
if not os.path.exists(file_folder_path):
    os.mkdir(file_folder_path)

images_folder_destination = DEFAULT_IMAGE_DEST
project_folder_destination = DEFAULT_PROJECT_DEST
model_folder_destination = DEFAULT_MODEL_DEST
material_folder_destination = DEFAULT_MATERIAL_DEST
video_folder_destination = DEFAULT_VIDEO_DEST
audio_folder_destination = DEFAULT_AUDIO_DEST
temporary_folder_name=DEFAULT_TEMPORARY_DEST


project_files = ['max', '3ds', 'blend', 'c4d', 'bgeo', 'geo','zpr','ma','mb','skp','3dm','sldprt','sldasm','zbp','hip']

model_files = ['obj', 'fbx', 'usdz', 'dae','usd*', 'ply', 'glb', 'gltf', 'x3d','ztl','stl','abc']

image_files = ['png', 'jpg', 'jpeg', 'exr', 'tiff', 'webp','gif', 'psd', 'indd', 'raw', 'svg', 'ai', 'tif','avif','hdr']

material_files = ['sbsar', 'spsm', 'spp', 'sbs']

video_files = ['mov', 'mp4', 'mkv', 'avi', 'wmv', 'avchd', 'webm', 'flv']

audio_files = ['wav', 'mp3', 'flac', 'ogg', 'm3u', 'acc','wma', 'wav', 'midi', 'aif', 'm4a', 'mpa', 'pls']

fType_dict={}

def default_setter(key,default):
    json_file_name =os.path.join(package_path,'addon_configuration','AddonDefaults.json')
    if os.path.exists(json_file_name):
        with open(json_file_name) as f:
            configs=json.load(f)
        if key==PRESET_KEY:
            if not os.path.exists(os.path.join(package_path,DEFAULT_PRESET_DEST,(f'{configs[key]}.json'))):
                return default
        return configs.get(key,default)
    return default

def dictionary_constructor():
    '''
    name             |  index
    -------------------------
    model_files      |   0   
    image_files      |   1  
    material_files   |   2
    video_files      |   3
    audio_files      |   4
    
    '''
    global fType_dict
    fType_list=[project_files+model_files,image_files,material_files,video_files,audio_files]
    fType_names=[model_folder_destination,images_folder_destination,material_folder_destination,video_folder_destination,audio_folder_destination]
    
    for index,extension_list in enumerate(fType_list):
        fType_dict[tuple(extension_list)]= fType_names[index]


# def update_recent_file_path(old_path, new_path):
    
#     config_directory = bpy.utils.user_resource('CONFIG')
#     recent_files_path = os.path.join(config_directory, "recent-files.txt")

    
#     if os.path.exists(recent_files_path):
        
#         with open(recent_files_path, "r") as file:
#             lines = file.readlines()

        
#         modified_lines = [line.strip().replace(old_path, new_path) if old_path in line else line.strip() for line in lines]

        
#         with open(recent_files_path, "w") as file:
#             file.write("\n".join(modified_lines))


# def get_blendfile_folder():
#     bfp = bpy.data.filepath
#     if bfp:
#         return bpy.path.abspath("//")
#     else:
#         return None

# def return_projectfile_name():
#     scene = bpy.context.scene
    
#     if scene.folder_presets!='DEFAULT':
#         preset_path=os.path.join(file_folder_path,scene.folder_presets+'.json')
#         with open(preset_path) as f:
#             f_names=json.load(f)
#         return f_names.get('PROJECT',project_folder_destination)
#     else:
#         return project_folder_destination
        

def path_constructor(presetname):
    global images_folder_destination 
    global project_folder_destination 
    global model_folder_destination 
    global material_folder_destination 
    global video_folder_destination 
    global audio_folder_destination 
    
    if presetname!=PRESET_DEFAULT_ID:
        json_file_name =os.path.join(package_path,'addon_configuration','AddonDefaults.json')
        if os.path.exists(json_file_name):
            with open(json_file_name) as f:
                configs=json.load(f)
            try:
                if configs[PRESET_KEY]!=PRESET_DEFAULT_ID:
                    preset_path=os.path.join(file_folder_path,(f"{configs[PRESET_KEY]}.json"))
                    
                    with open(preset_path) as f:
                        f_names=json.load(f)
                    
                    images_folder_destination = f_names.get(TAG_IMAGE,images_folder_destination)
                    project_folder_destination = f_names.get(TAG_PROJECT,project_folder_destination)
                    model_folder_destination = f_names.get(TAG_MODEL,model_folder_destination)
                    material_folder_destination =f_names.get(TAG_MATERIAL,material_folder_destination)
                    video_folder_destination = f_names.get(TAG_VIDEO,video_folder_destination)
                    audio_folder_destination = f_names.get(TAG_AUDIO,audio_folder_destination)
            except:
                images_folder_destination = DEFAULT_IMAGE_DEST
                project_folder_destination = DEFAULT_PROJECT_DEST
                model_folder_destination = DEFAULT_MODEL_DEST
                material_folder_destination = DEFAULT_MATERIAL_DEST
                video_folder_destination = DEFAULT_VIDEO_DEST
                audio_folder_destination = DEFAULT_AUDIO_DEST
        else:
            
            preset_path=os.path.join(file_folder_path,(f"{presetname}.json"))
            if os.path.exists(preset_path):
                with open(preset_path) as f:
                    f_names=json.load(f)
            
                images_folder_destination = f_names.get(TAG_IMAGE,images_folder_destination)
                project_folder_destination = f_names.get(TAG_PROJECT,project_folder_destination)
                model_folder_destination = f_names.get(TAG_MODEL,model_folder_destination)
                material_folder_destination =f_names.get(TAG_MATERIAL,material_folder_destination)
                video_folder_destination = f_names.get(TAG_VIDEO,video_folder_destination)
                audio_folder_destination = f_names.get(TAG_AUDIO,audio_folder_destination)
            else:
                images_folder_destination = DEFAULT_IMAGE_DEST
                project_folder_destination = DEFAULT_PROJECT_DEST
                model_folder_destination = DEFAULT_MODEL_DEST
                material_folder_destination = DEFAULT_MATERIAL_DEST
                video_folder_destination = DEFAULT_VIDEO_DEST
                audio_folder_destination = DEFAULT_AUDIO_DEST
            
    else:
        images_folder_destination = DEFAULT_IMAGE_DEST
        project_folder_destination = DEFAULT_PROJECT_DEST
        model_folder_destination = DEFAULT_MODEL_DEST
        material_folder_destination = DEFAULT_MATERIAL_DEST
        video_folder_destination = DEFAULT_VIDEO_DEST
        audio_folder_destination = DEFAULT_AUDIO_DEST

    dictionary_constructor()
    
        
# def blender_folder_on_saved(dummy):
#     global save_flag
#     global blender_folder

#     blender_folder = get_blendfile_folder()
#     if save_flag == False:

#         blender_folder = get_blendfile_folder()
#         new_blender_folder = os.path.join(blender_folder, project_folder_destination)
#         if not os.path.exists(new_blender_folder):
#             os.makedirs(new_blender_folder)
        

#         old_file_path = bpy.data.filepath
        

#         shutil.move(bpy.data.filepath, new_blender_folder)

#         new_file_path = os.path.join(
#             blender_folder, project_folder_destination, os.path.basename(old_file_path))
        
        
        
#         bpy.ops.wm.open_mainfile(filepath=new_file_path)
#         bpy.ops.wm.save_mainfile(filepath=new_file_path)

#         temporary_folder_path=os.path.join(get_downloads_folder(), temporary_folder_name)
        
#         if os.path.exists(temporary_folder_path):

#             for folder in os.listdir(temporary_folder_path):
#                 transfer_dest=os.path.join(os.path.join(blender_folder,folder))

#                 if os.path.exists(transfer_dest):
#                     current_folder=os.path.join(temporary_folder_path,folder)
                    
#                     for downloads_file in os.listdir(current_folder):
#                         shutil.move(os.path.join(current_folder,downloads_file),transfer_dest) 

#                 else:
#                     shutil.move(os.path.join(temporary_folder_path, folder), blender_folder)
                
#         reload_image_textures(os.path.join(blender_folder,images_folder_destination))
#         update_recent_file_path(old_file_path,new_file_path)
#         save_flag =True

def log_info(file_name, file_path):
    info_list = [file_name, file_path]
    log_tuple = tuple(info_list)
    file_data.append(log_tuple)

# def is_blend_file_saved():
#     if bpy.data.filepath == "":
#         return False
#     else:
#         return True

# def get_source_folder(flag):
#     if flag == '0':
#         return get_downloads_folder()
#     else:

#         path = get_blendfile_folder()
#         newpath_1 = os.path.dirname(path)
#         newpath_2 = os.path.dirname(newpath_1)
#         return newpath_2

# def reload_image_textures(target_folder):
#     for material in bpy.data.materials:
#         if material.node_tree:
#             for node in material.node_tree.nodes:
#                 if node.type == 'TEX_IMAGE':
#                     image_texture = node.image
#                     if image_texture:
                        
#                         if image_texture.filepath:
                            
#                             filename = os.path.basename(image_texture.filepath)
#                             new_filepath = os.path.join(target_folder, filename)
#                             image_texture.filepath = bpy.path.abspath(new_filepath)
#                             image_texture.reload()
                            
def organise_zip(zip_file_path, destination_folder, file_name):
    video_count=0
    audio_count=0
    image_count=0
    flag_dictionary={'model_flag': False,'Video_flag':False,'Audio_flag':False,'image_flag':False}

    combined_list = model_files + project_files
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")

    subdirectory_name = os.path.splitext(os.path.basename(zip_file_path))[0]+' '+formatted_date
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_names = zip_ref.namelist()

    
    for file in file_names:
        extension = file.split('.')[-1].lower()
        if extension in combined_list:
            flag_dictionary['model_flag'] = True
        elif extension in video_files:
            video_count+=1
            flag_dictionary['Video_flag'] = True
        elif extension in audio_files:
            audio_count+=1
            flag_dictionary['Audio_flag'] = True
        elif extension in image_files:
            image_count+=1
            flag_dictionary['image_flag'] = True
    if flag_dictionary['model_flag']!=True:
        num_dict={'Video_flag':video_count,'Audio_flag':audio_count,'image_flag':image_count}
        largest_num = max(num_dict.values())
        variable_with_max = [name for name, value in num_dict.items() if value == largest_num][0]
        for key in flag_dictionary:
            if key==variable_with_max:
                flag_dictionary[key]=True
            else:
                flag_dictionary[key]=False

    if flag_dictionary['model_flag'] == True:
        model_folder = os.path.join(destination_folder, model_folder_destination)
        create_folder(model_folder)
        
        subdirectory_path = os.path.join(model_folder, subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name, model_folder)

    elif flag_dictionary['Video_flag'] == True:

        video_folder = os.path.join(destination_folder, video_folder_destination)
        create_folder(video_folder)

        subdirectory_path = os.path.join(video_folder, subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name, video_folder)
    elif flag_dictionary['Audio_flag']==True:
        audio_folder = os.path.join(destination_folder, audio_folder_destination)
        create_folder(audio_folder)

        subdirectory_path = os.path.join(audio_folder, subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name, audio_folder)
    elif flag_dictionary['image_flag']==True:
        image_folder = os.path.join(destination_folder, images_folder_destination)
        create_folder(image_folder)

        subdirectory_path = os.path.join(image_folder, subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name, image_folder)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_downloads_folder():
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def duplicate_handler(file_path, file, folder_path, extension):
    #CHeck this function for duplicate files
    global filecount
    try:
        if os.path.exists(os.path.join(folder_path, file)):
            new_file_name = file.split('.')[0]+(f'({str(filecount)})')
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name+'.'+extension)
            os.rename(file_path, new_file_path)
            shutil.move(new_file_path, folder_path)
        else:
            shutil.move(file_path, folder_path)
        filecount += 1
    except Exception as e:
        print(e)
    

def organiser_utility(destination_folder, extension, file_path, file):
    extracted_flag=False
    if extension!='zip':
        for key in fType_dict.keys():
            if extension in key:
                folder_path = os.path.join(destination_folder, fType_dict[key])
                create_folder(folder_path)
                duplicate_handler(file_path, file, folder_path, extension)
                log_info(file, folder_path)
    else:
        json_file_name =os.path.join(package_path,'addon_configuration','AddonDefaults.json')
        if not extracted_flag:
            if os.path.exists(json_file_name):
                with open(json_file_name) as f:
                    configs=json.load(f)
                if not configs.get(ZIPMODE_KEY):
                    organise_zip(file_path, destination_folder, file)
                else:  
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        file_names = zip_ref.namelist()
                        for files in file_names:
                            now = datetime.datetime.now()
                            formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
                            extension_in_zip = files.split('.')[-1].lower()
                            for keyforzip in fType_dict.keys():
                                if extension_in_zip in keyforzip:
                                    output_dir = os.path.join(destination_folder, fType_dict[keyforzip],file.split('.')[0]+' '+formatted_date)
                                    log_info(os.path.basename(files), output_dir)
                                    create_folder(output_dir)
                                    output_file_path = os.path.join(output_dir, os.path.basename(files))
                                    with zip_ref.open(files) as source_file, open(output_file_path, "wb") as target_file:
                                        target_file.write(source_file.read())                     
        else:
            organise_zip(file_path, destination_folder, file)
        os.remove(file_path)

def organise(source_folder, destination_folder, localtime_at_Start):
    
    for file in os.listdir(source_folder):
                                
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path):

            if os.path.getmtime(file_path) >= localtime_at_Start:
                    
                extension = file.split('.')[-1].lower()

                organiser_utility(destination_folder,extension, file_path, file)
            