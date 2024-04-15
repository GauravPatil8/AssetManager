import bpy
from aao_constants import ZIPMODE_PREDOMINANT_ID,ZIPMODE_SEPERATE_ID,REALTIME_DELAY_ONE,REALTIME_DELAY_SEVEN,REALTIME_DELAY_THREE,SRCFOLDER_CUSTOM_ID,SRCFOLDER_DOWNLOADS_ID,DELAY_KEY,ZIPENUM_KEY,SRCFOLDER_KEY,SRCFOLDERPATH_KEY,DESTFOLDERPATH_KEY
from aao_ut_filehandler import default_setter

class ADDON_PROPERTYGROUP(bpy.types.PropertyGroup):

    bpy.types.Scene.default_config=bpy.props.BoolProperty(    #type:ignore
        name="Configure Defaults",
        description="Clicking this option will load current addon preferences everytime you start Blender",
        default=False
    )

    bpy.types.Scene.zip_extraction=bpy.props.EnumProperty(
        items=[
            (ZIPMODE_SEPERATE_ID, 'Separate Assets', 'This option organizes all assets into their respective folders during the extraction of a zipfile.'),
            (ZIPMODE_PREDOMINANT_ID, 'Predominant Asset Type', 'This option extracts a Zipfile into a specific folder based on the predominant type of asset it contains. For instance, if the Zipfile contains a significant number of video files, it will be extracted into the video files folder.'),
        ],
        default=default_setter(ZIPENUM_KEY,ZIPMODE_PREDOMINANT_ID)
    )# type: ignore

    bpy.types.Scene.delay_time_prop = bpy.props.EnumProperty(
        items=[
            (REALTIME_DELAY_ONE, '1 Seconds', 'Orgnises folder after every one seconds'),
            (REALTIME_DELAY_THREE, '3 Seconds', 'Orgnises folder after every three seconds'),
            (REALTIME_DELAY_SEVEN, '7 Seconds', 'Orgnises folder after every seven seconds')
        ],
        default=default_setter(DELAY_KEY,REALTIME_DELAY_THREE),
    )
    bpy.types.Scene.monitor_folder = bpy.props.EnumProperty(
        items=[
            (SRCFOLDER_DOWNLOADS_ID, 'Monitor Downloads Folder',
             'This option enables monitoring of the downloads folder for newly added files.'),
            (SRCFOLDER_CUSTOM_ID, 'Select Folder To Monitor',
             'This option enables monitoring of the folder that you choose for newly added files.'),
        ],
        default=default_setter(SRCFOLDER_KEY,SRCFOLDER_DOWNLOADS_ID),
    )

    bpy.types.Scene.folder_path = bpy.props.StringProperty(
        name="",
        description="Enter folder path",
        default=default_setter(SRCFOLDERPATH_KEY,''),
       
    )
    bpy.types.Scene.destination_path = bpy.props.StringProperty(
        name="",
        description="Enter destination path",
        default=default_setter(DESTFOLDERPATH_KEY,''),
       
    )
    bpy.types.Scene.preset_name = bpy.props.StringProperty(
        name="Enter Preset Name",
        description="Enter Preset name",
        default="",
       
    )
    bpy.types.Scene.preset_analysis_folder = bpy.props.StringProperty(
        name="Select Folder",
        description="Select folder to be Analysied",
        default="",
    )