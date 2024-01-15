bl_info = {
    "name": "Asset Organiser test",
    "blender": (4, 00, 2),
    "category": "Object",
}
import sys 
sys.path.append(R'C:\AssetManager')
import AutoFileOrganiser   

def register():
  
        
    AutoFileOrganiser.register()

def unregister():
    
        
    AutoFileOrganiser.unregister()


register()
