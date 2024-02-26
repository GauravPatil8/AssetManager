import os
import shutil
import bpy
import zipfile
import sys
from AAO_DB_FolderNames import fetch_folder_name
from AAO_DB_FolderNames import create_and_populate
from AAO_OT_Log import file_data

filecount=0
database_connection=create_and_populate()
#temporary hai
images_folder_name=fetch_folder_name(database_connection,1)
project_folder_name=fetch_folder_name(database_connection,2)
model_folder_name=fetch_folder_name(database_connection,3)
mocap_folder_name=fetch_folder_name(database_connection,4)



# execute everytime at the beginning code (GLOBALLY DECLARED):

project_files   = ['max','3ds','blend','c4d','bgeo','geo']
     
model_files     = ['obj','fbx','usdz','dae','usd*','ply','glb','gltf','x3d']

image_files     = ['png','jpg','jpeg','exr','tiff','webp','gif','psd','indd','raw','svg','ai','tif',]

mocap_files     = ['bvh']

material_files  = ['sbsar','spsm','spp','sbs']


def log_info(file_name,file_path):
     info_list=[file_name,file_path]
     log_tuple=tuple(info_list)
     file_data.append(log_tuple)

def is_blend_file_saved():
    if bpy.data.filepath == "":
        return False
    else:
        return True
    
def get_source_folder(flag):
    if flag=='0':
        return get_downloads_folder()
    else:
        
        path= get_blendfile_folder()
        newpath_1=os.path.dirname(path)
        newpath_2=os.path.dirname(newpath_1)
        return newpath_2
     
     

def organise_zip(zip_file_path,destination_folder,file_name):

    flag=False                          
    extension_dictionary={}
    
    combined_list = model_files + project_files

    subdirectory_name = os.path.splitext(os.path.basename(zip_file_path))[0]

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_names=zip_ref.namelist()  
    
    blend_file_count=0
    gltf_file_count=0
    for file in file_names:
        extension=file.split('.')[-1].lower()
        if extension in combined_list:
            extension_dictionary[extension]=extension_dictionary.get(extension,0)+1

            ## handling polyhaven files

            if extension=='blend':
                blend_file_count+=1
            elif extension=='gltf':
                gltf_file_count+=1
                      
        if extension in extension_dictionary:
            if blend_file_count and gltf_file_count == 1:
                flag=False
            else:
                 flag=True
    

            
    if flag==True:
        model_folder = os.path.join(destination_folder, model_folder_name)
        create_folder(model_folder)
            
        subdirectory_path=os.path.join(model_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name,model_folder)
        
                        
    else:
                        
        images_folder = os.path.join(destination_folder,images_folder_name)
        create_folder(images_folder)
            
        subdirectory_path=os.path.join(images_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
        log_info(file_name,images_folder)
        
               

def create_folder(folder_path):
    os.makedirs(folder_path,exist_ok=True)



def get_downloads_folder():
    
    if os.name == 'nt':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
   
    elif sys.platform == 'darwin':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    
def duplicate_handler(file_path,file,folder_path,extension):
    global filecount
    if os.path.exists(os.path.join(folder_path,file)):
        new_file_name=file.split('.')[0]+'_'+str(filecount)
        new_file_path=os.path.join(os.path.dirname(file_path),new_file_name+'.'+extension)
        os.rename(file_path,new_file_path)
        shutil.move(new_file_path,folder_path)
    else:
         shutil.move(file_path,folder_path)
    filecount+=1

def organiser_utility(destination_folder,extension,file_path,file):
    if extension in image_files:
                    
                    images_folder_path=os.path.join(destination_folder,images_folder_name)
                    create_folder(images_folder_path)
                    duplicate_handler(file_path,file,images_folder_path,extension)
                    log_info(file,images_folder_path)
                    
    elif extension in project_files:
                    
                    project_folder_path=os.path.join(destination_folder,project_folder_name)
                    create_folder(project_folder_path)
                    duplicate_handler(file_path,file,project_folder_path,extension)
                    log_info(file,project_folder_path)
                    

    elif extension in model_files:

                    model_folder_path=os.path.join(destination_folder,model_folder_name)
                    create_folder(model_folder_path)
                    duplicate_handler(file_path,file,mocap_folder_path,extension)
                    log_info(file,model_folder_path)
                    
                        
    elif extension in mocap_files:

                    mocap_folder_path=os.path.join(destination_folder,mocap_folder_name)
                    create_folder(mocap_folder_path)
                    duplicate_handler(file_path,file,mocap_folder_path,extension)
                    log_info(file,mocap_folder_path)
                    

    elif extension =='zip':
        organise_zip(file_path,destination_folder,file)
        os.remove(file_path)
        


    elif extension =='hdr':
        hdri_folder_path=os.path.join(destination_folder,images_folder_name,"HDRI_Images")
        create_folder(hdri_folder_path)
        duplicate_handler(file_path,file,hdri_folder_path,extension)
        log_info(file,hdri_folder_path)
        

    elif extension in material_files:
        material_folder_path=os.path.join(destination_folder,project_folder_name,"Materials") #project files ke jagah db name daal diyo
        create_folder(material_folder_path)
        duplicate_handler(file_path,file,material_folder_path,extension)
        log_info(file,material_folder_path)
        


def get_blendfile_folder():
    bfp=bpy.data.filepath
    if bfp:
        return bpy.path.abspath("//")
    else:
        return None
    

def organise(source_folder_flag,destination_folder,localtime_at_Start):
    
    for file in os.listdir(get_source_folder(source_folder_flag)):
           
              
        file_path=os.path.join(get_source_folder(source_folder_flag),file)
        if os.path.isfile(file_path): 
            
            if os.path.getmtime(file_path)>=localtime_at_Start: # yaha file ka time check karra agar program start hone se pehle koi file hogi toh uspe operation nai hoga

                if os.path.isfile(file_path):
                        extension=file.split('.')[-1].lower() # file ka extension extract karra hai
                        
                        organiser_utility(destination_folder,extension,file_path,file)
                
