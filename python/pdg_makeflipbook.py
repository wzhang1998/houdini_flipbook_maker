import hou
import subprocess
import os
import glob
import shlex

def encodeVideo(input_path, output_path, framerate=24, codec="libx264", overlay_text=""):
    # # Create a dummy Fontconfig configuration file
    # with open("dummy.conf", "w") as file:
    #     file.write("<fontconfig></fontconfig>")

    # Set the FONTCONFIG_FILE environment variable
    # os.environ["FONTCONFIG_PATH"] = "C:/Windows/Fonts"

    # Run ffmpeg command to encode video
    ffmpeg_command = [
        "ffmpeg",
        "-framerate", str(framerate),
        "-i", input_path.replace("$F4", "%04d"),
        # "-vf", "drawtext=fontfile=C\\:/Windows/Fonts/calibril.ttf:text='{overlay_text}':x=10:y=50:fontsize=24:fontcolor=white",
        "-c:v", codec,
        "-pix_fmt", "yuv420p",
        output_path
    ]
    # subprocess.run(ffmpeg_command)
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # If the command failed, print the error
    if result.returncode != 0:
        print(result.stderr.decode())

def flipbookMaker(encode_to="mp4"):

    if os.path.exists('cancel.txt'):
        os.remove('cancel.txt')

    output_directory = pdg.workItem().attrib("output_directory").asString()

    # Get a list of all jpg files in the output directory
    jpg_files = glob.glob(os.path.join(output_directory, '*.jpg'))

    # Loop through the list and delete each file
    for jpg_file in jpg_files:
        os.remove(jpg_file)

    # Access the "camera" attribute as a string
    cams =  pdg.workItem().attribArray("camera")
    resolution_percentage = pdg.workItem().attribValue(name="resolution_percentage", index=0)
    start_frame = pdg.workItem().attribValue(name="start_frame", index=0)
    end_frame = pdg.workItem().attribValue(name="end_frame", index=0)
    # print(cams)
    
    use_note = hou.parm("../../if_overlay_text").eval()
    add_viewport_cam = hou.parm("../../add_viewport_cam").eval()

    if add_viewport_cam == 1:
        # Get the current viewport
        pane = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        viewport = pane.curViewport()

        # Check if a viewport camera already exists
        existing_cam = hou.node("/obj/cam_viewport")
        if existing_cam is not None:
            # If it does, delete it
            existing_cam.destroy()

        # Create a new camera
        new_cam = hou.node("/obj").createNode("cam", "cam_viewport")

        # Set the camera's view transform to the current view transform
        new_cam.setParms({"tx": viewport.viewTransform().extractTranslates()[0],
                        "ty": viewport.viewTransform().extractTranslates()[1],
                        "tz": viewport.viewTransform().extractTranslates()[2],
                        "rx": viewport.viewTransform().extractRotates()[0],
                        "ry": viewport.viewTransform().extractRotates()[1],
                        "rz": viewport.viewTransform().extractRotates()[2]})

        # Add the new camera to the beginning of the cams list
        cams.insert(0, new_cam.path())

    
    for cam in cams:

        # Get attributes from work item
        output_filename = pdg.workItem().attrib("output_filename").asString() + "_" + str(hou.node(cam).name()) + "_v" +  hou.parm("../../versions").evalAsString()
        # Get custom text from node parameter and change line breaks to spaces
        custom_text = "Note:" + hou.parm("../../overlay_text").evalAsString() + "\n" + str(hou.node(cam).name()) + " v" +  hou.parm("../../versions").evalAsString()


        # Get camera resolution
        cam = hou.node(cam)
    
        cam_resx = cam.parm("resx")
        cam_resx = cam_resx.eval()
        cam_resy = cam.parm("resy")
        cam_resy = cam_resy.eval()
    
        # Apply resolution percentage
        cam_resx *= resolution_percentage
        cam_resy *= resolution_percentage
    
        # Quantize values for camera resolution to avoid problems with ffmpeg and uneven resolutions
        cam_resx /= 2
        cam_resx = int(cam_resx)
        cam_resx *= 2
    
        cam_resy /= 2
        cam_resy = int(cam_resy)
        cam_resy *= 2
    
        # Set output filename for flipbook frames
        output_frames_path = output_directory + output_filename + "_$F4.jpg"
    
        # Define viewport variables
        cur_desktop = hou.ui.curDesktop()
        scene_viewer = hou.paneTabType.SceneViewer
        scene = cur_desktop.paneTabOfType(scene_viewer)
        
        # Set viewport camera
        viewport = scene.findViewport(name="persp1")
        viewport_settings = viewport.settings()
        viewport_settings.setCamera(cam)
        
        # Set flipbook settings
        scene.flipbookSettings().stash()
        flip_book_options = scene.flipbookSettings()
        
        # Configure flipbook options
        flip_book_options.output( output_frames_path)  # Provide flipbook full path with padding.
        flip_book_options.frameRange((start_frame, end_frame))  # Enter Frame Range Here in x & y
        flip_book_options.useResolution(1)
        flip_book_options.resolution((cam_resx, cam_resy))  # Based on your camera resolution
        
        # Initiate flipbook rendering in the current viewport
        scene.flipbook(scene.curViewport(), flip_book_options)
        
        if use_note == 1:
             
            # Add text overlay to each frame using ImageMagick
            for i in range(start_frame, end_frame + 1):

                # Check if the cancel button has been pressed
                if os.path.exists('cancel.txt'):
                    print("Cancel button pressed, stopping execution.")
                    return

                input_frame_path = output_frames_path.replace("$F4", f"{i:04}")
                output_frame_path = input_frame_path.replace(".jpg", "_text.jpg")
                frame_text = f"{custom_text}\n Frame:{i:04}"
                
                # Convert file paths to use correct slashes for the current operating system
                input_frame_path = os.path.normpath(input_frame_path)
                output_frame_path = os.path.normpath(output_frame_path)
    
                # Calculate point size based on resolution percentage
                point_size = int(30 * resolution_percentage)

                # Create a STARTUPINFO object
                startupinfo = subprocess.STARTUPINFO()

                # Set the STARTF_USESHOWWINDOW flag
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                # Set the wShowWindow field to SW_HIDE
                startupinfo.wShowWindow = subprocess.SW_HIDE

                imagemagick_command = [
                    "magick",
                    input_frame_path,
                    "-font", "Arial",
                    "-pointsize", str(point_size),
                    "-fill", "white",
                    "-gravity", "southeast",
                    "-annotate", "+10+10",
                    f'{frame_text}',
                    output_frame_path
                ]

                # Pass the startupinfo object to the subprocess.run function
                result = subprocess.run(imagemagick_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    
                # If the command failed, print the error
                if result.returncode != 0:
                    print(result.stderr.decode())
        
            # Set output path for frames with text overlay
            output_frames_path_text = output_frames_path.replace(".jpg", "_text.jpg")
            
        else:
             output_frames_path_text = output_frames_path

       # Choose video format based on user input
        if encode_to == "mp4":
            mp4_output_path = output_directory + output_filename + ".mp4"
            encodeVideo( output_frames_path_text, mp4_output_path, overlay_text = custom_text)
        elif encode_to == "gif":
            gif_output_path = output_directory + output_filename + ".gif"
            encodeVideo( output_frames_path_text, gif_output_path, codec="gif", overlay_text = custom_text)
        else:
            print("Invalid output format specified. Please choose 'mp4' or 'gif'.")
    
        # Optionally, clean up individual frames
        jpg_files = glob.glob(os.path.join(output_directory, output_filename + '*.jpg'))

        # Iterate over the list of files and delete each one
        for jpg_file in jpg_files:
            try:
                os.remove(jpg_file)
            except Exception as e:
                print(f"Error deleting {jpg_file}: {e}")

# Get the value of the output format parameter
encode_format_value = hou.parm("../../output_format").eval()
# Set the output format based on the value of the output format parameter
if encode_format_value == 1:
    encode_format = "gif"
else:
    encode_format = "mp4"



flipbookMaker(encode_to=encode_format)



