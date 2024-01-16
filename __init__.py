bl_info = {
    "name": "Realtime Asset Manager",
    "blender": (4, 0, 2),
    "category": "System", 
    "author": "Swami",
    "version": (1, 0, 0),
    "location": "View3D > UI> Asset Organiser",
    "description": "Real-time Asset Organizer for 3D Artists is a powerful Blender addon designed to streamline and enhance the workflow of 3D artists by providing a dynamic and efficient asset management system.",
    "warning": "",
    # "wiki_url": "URL to your addon's documentation or wiki",
    # "tracker_url": "URL to your addon's issue tracker",
    "support": "COMMUNITY",
    
}
import sys 
import os
script_path = os.path.abspath(__file__)
package_path = os.path.dirname(script_path)
sys.path.append(package_path)
import AutoFileOrganiser   

def register():

    AutoFileOrganiser.register()

def unregister():
 
    AutoFileOrganiser.unregister()


register()
