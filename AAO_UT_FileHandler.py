import os
import shutil
import bpy
import zipfile
from AAO_DB_FolderNames import create_and_populate
from AAO_DB_FolderNames import fetch_folder_name
from AAO_DB_FolderNames import update_folder_name
from AAO_DB_FolderNames import psfn_fetch_folder_name
from AAO_DB_FolderNames import psfn_createT
from AAO_DB_FolderNames import psfn_closeconn
from AAO_DB_FolderNames import psfn_updateName
from AAO_DB_FolderNames import table_inMemory
from AAO_DB_FolderNames import insert_inMemory
from AAO_DB_FolderNames import close_connection

#temporary hai
images_folder_name="Textures"
project_folder_name="Project_files"
model_folder_name="Model_files"
mocap_folder_name="Mocap_files"



# execute everytime at the beginning code (GLOBALLY DECLARED):

project_files   = ['max','3ds','blend','c4d','bgeo','geo']
     
model_files     = ['obj','fbx','usdz','dae','usd*','ply','glb','gltf','x3d']

image_files     = ['png','jpg','jpeg','exr','tiff','webp','gif','psd','indd','raw','svg','ai','tif',]

mocap_files     = ['bvh']

material_files  = ['sbsar','spsm','spp','sbs']



def organise_zip(folder_path,dest_folder):

    flag=False                          
    extension_dictionary={}
    
    combined_list = model_files + project_files

    subdirectory_name = os.path.splitext(os.path.basename(folder_path))[0]

    with zipfile.ZipFile(folder_path, 'r') as zip_ref:
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
            if not  blend_file_count and gltf_file_count == 1:
                flag=True
    

            
    if flag==True:
        model_folder = os.path.join(dest_folder, "Model_Files")
        create_folder(model_folder)
            
        subdirectory_path=os.path.join(model_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(folder_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
                        
    else:
                        
        images_folder = os.path.join(dest_folder, "Image_Files")
        create_folder(images_folder)
            
        subdirectory_path=os.path.join(images_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(folder_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
               

def create_folder(folder_path):
    os.makedirs(folder_path,exist_ok=True)



def get_downloads_folder():
    home_directory=os.path.expanduser('~')

    if os.name=='posix':
        downloads_folder=os.path.join(home_directory,'Downloads')
    
    elif os.name=='nt':
        downloads_folder=os.path.join(home_directory,'Downloads')
    else:
        raise OSError("Unsupported Operating System")
    return downloads_folder


def organiser_utility(dest_folder,extension,file_path):
    if extension in image_files:

                    images_folder_path=os.path.join(dest_folder,images_folder_name)
                    create_folder(images_folder_path)
                    shutil.move(file_path,images_folder_path)

    elif extension in project_files:

                    project_folder_path=os.path.join(dest_folder,project_folder_name)
                    create_folder(project_folder_path)
                    shutil.move(file_path,project_folder_path)

    elif extension in model_files:

                    model_folder_path=os.path.join(dest_folder,model_folder_name)
                    create_folder(model_folder_path)
                    shutil.move(file_path,model_folder_path)
                        
    elif extension in mocap_files:

                    mocap_folder_path=os.path.join(dest_folder,mocap_folder_name)
                    create_folder(mocap_folder_path)
                    shutil.move(file_path,mocap_folder_path)

    elif extension =='zip':
        organise_zip(file_path,dest_folder)
        os.remove(file_path)


    elif extension =='hdr':
        hdri_folder_path=os.path.join(dest_folder,images_folder_name,"HDRI_Images")
        create_folder(hdri_folder_path)
        shutil.move(file_path,hdri_folder_path)

    elif extension in material_files:
        material_folder_path=os.path.join(dest_folder,project_folder_name,"Materials") #project files ke jagah db name daal diyo
        create_folder(material_folder_path)
        shutil.move(file_path,material_folder_path)


def get_blendfile_folder():
    bfp=bpy.data.filepath
    if bfp:
        return bpy.path.abspath("//")
    else:
        return None
    

def organise(src_folder,destination_folder,localtime_atStart):
    
    if destination_folder != None:
        for file in os.listdir(src_folder):
                                    
            file_path=os.path.join(src_folder,file)

            if os.path.getmtime(file_path)>=localtime_atStart: # yaha file ka time check karra agar program start hone se pehle koi file hogi toh uspe operation nai hoga

                if os.path.isfile(file_path):
                    extension=file.split('.')[-1].lower() # file ka extension extract karra hai
                
                organiser_utility(destination_folder,extension,file_path)
                
            else:
                break

