# Realtime_Asset_Manager 
This is a addon for the 3D software package"Blender" <br>
Main features of the addon:<br>
1.Auto Organising project file.<br>
2.Searching across project folders.<br>
3.Auto texture organisation.<br>
4.Drag and drop image textures,3dmodels,etc
bl_label = "Monitor Folder Operator"
    bl_idname = "object.monitor_folder_operator"

    _monitoring_thread = None

    def modal_handler(self, context):
        if not context.scene.realtime:
            self.report({'INFO'}, "Realtime Monitoring Stopped.")
            return {'CANCELLED'}

        selected_folder = context.scene.monitor_folder
        self.report({'INFO'}, f"Realtime Monitoring of {selected_folder} Folder")
        organise()  # Modify as needed

        # Set the monitoring interval (in seconds)
        interval = 5
        return interval

    def modal(self, context, event):
        if event.type == 'TIMER':
            interval = self.modal_handler(context)
            return {'PASS_THROUGH'} if interval is None else {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        if context.scene.realtime:
            self.report({'INFO'}, "Realtime Monitoring Started...")
            # Start a new thread for monitoring
            self._monitoring_thread = threading.Thread(target=self.monitoring_thread, args=(context,))
            self._monitoring_thread.start()
            bpy.app.timers.register(self.modal, first_interval=0.1)
        else:
            self.report({'INFO'}, "Realtime Monitoring Stopped.")
        return {'FINISHED'}

    def monitoring_thread(self, context):
        while context.scene.realtime:
            time.sleep(3)  # Sleep for a short duration to allow the main thread to handle modal updates

        self.report({'INFO'}, "Realtime Monitoring Stopped.")