import os
import shutil
import bpy
import zipfile
from Folder_namedb import create_and_populate
from Folder_namedb import fetch_folder_name
from Folder_namedb import update_folder_name
from Folder_namedb import psfn_fetch_folder_name
from Folder_namedb import psfn_createT
from Folder_namedb import psfn_closeconn
from Folder_namedb import psfn_updateName
from Folder_namedb import table_inMemory
from Folder_namedb import insert_inMemory
from Folder_namedb import close_connection
import itertools
# from AutoFileOrganiser import localtime_atStart

global folder_name_flag
folder_name_flag=None #idhar function daal diyo

# execute everytime at the beginning code (GLOBALLY DECLARED):

project_files   = ['max','3ds','blend','c4d','bgeo','geo']
     
model_files     = ['obj','fbx','usdz','dae','usd*','ply','glb','gltf','x3d']

image_files     = ['png','jpg','jpeg','exr','tiff','webp','gif','psd','indd','raw','svg','ai','tif',]

mocap_files     = ['bvh']

material_files  = ['sbsar','spsm','spp','sbs']



def organise_zip(folder_path,dest_folder):

    flag=False
    extension_dictionary={}
    folder_path_name=os.path.basename(folder_path).split('.')[0]
    
    combined_list = model_files + project_files
    subdirectory_name = os.path.splitext(os.path.basename(folder_path))[0]
    with zipfile.ZipFile(folder_path, 'r') as zip_ref:
        file_names=zip_ref.namelist()  
    
    
    for file in file_names:
        extension=file.split('.')[-1].lower()
        if extension in combined_list:
            extension_dictionary[extension]=extension_dictionary.get(extension,0)+1
    
        if extension in extension_dictionary:
            flag=True

            
    if flag==True:
        model_folder = os.path.join(dest_folder, "Model_Files")
        create_folder(model_folder)
            
        subdirectory_path=os.path.join(model_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(folder_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
                        
    else:
                        
        images_folder = os.path.join(dest_folder, "Model_Files")
        create_folder(images_folder)
            
        subdirectory_path=os.path.join(images_folder,subdirectory_name)
        create_folder(subdirectory_path)
        with zipfile.ZipFile(folder_path,'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)
               


def set_folder_names():
    global images_folder_name   
    global project_folder_name  
    global model_folder_name    
    global mocap_folder_name   

    if folder_name_flag =='0':
        images_folder_name=fetch_folder_name('1')
        project_folder_name=fetch_folder_name('2')
        model_folder_name=fetch_folder_name('3')
        mocap_folder_name=fetch_folder_name('4')
    else:
        images_folder_name=psfn_fetch_folder_name('1')
        project_folder_name=psfn_fetch_folder_name('2')
        model_folder_name=psfn_fetch_folder_name('3')
        mocap_folder_name=psfn_fetch_folder_name('4')

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
        hdri_folder_path=os.path.join(dest_folder,"HDRI_Images")
        create_folder(hdri_folder_path)
        shutil.move(file_path,hdri_folder_path)

    elif extension in material_files:
        material_folder_path=os.path.join(dest_folder,"Materials")
        create_folder(material_folder_path)
        shutil.move(file_path,material_folder_path)


def get_blendfile_folder():
    bfp=bpy.data.filepath
    if bfp:
        return bpy.path.abspath("//")
    else:
        return None
    

def organise():
    src_folder=R"C:\zipextracttest"
    dest_folder=R"C:\zipextracttest"

    for file in os.listdir(src_folder):
                                
        file_path=os.path.join(src_folder,file)

        if os.path.getmtime(file_path)>=localtime_atStart: # yaha file ka time check karra agar program start hone se pehle koi file hogi toh uspe operation nai hoga

            if os.path.isfile(file_path):
                extension=file.split('.')[-1].lower() # file ka extension extract karra hai
            
            organiser_utility(dest_folder,extension,file_path)
               
        else:
            break

zip_file_path=R"C:\zipextracttest\used-new-balance-574-classic-free.zip"
dest_folder=R"C:\zipextracttest"
organise_zip(zip_file_path,dest_folder)