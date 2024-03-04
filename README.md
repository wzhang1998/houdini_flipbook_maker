# Houdini Flipbook Maker

A plugin for Houdini that allows you to render multiple cameras at once, supports multiple resolutions, adds overlay text for camera/frame/notes, and exports the output in GIF or MP4 format.
Inspired by Danny Laursen's [Houdini Easy Flipbook HDA](https://dannylrsn.gumroad.com/l/lfgcnh)

## Usage

Before using this plugin, make sure you have installed [ffmpeg](https://ffmpeg.org/) and [ImageMagick](https://imagemagick.org/) on your system.
Download the HDA file from the latest release in the plugin repository.

To add the `object_Wenyi.flipbook_maker.1.3.hdanc` to your Houdini project, follow these steps:

1. Download the HDA file from the plugin repository.
2. Open your Houdini project.
3. Go to the "Assets" tab in the Houdini interface.
4. Click on the "Install Digital Asset Library" button.
5. Browse and select the downloaded HDA file.
6. The plugin will be added to your Houdini project.

## Functions

The plugin provides the following functions: 

<img src="https://github.com/wzhang1998/houdini_flipbook_maker/assets/67906283/b52efa24-7421-47c2-864d-d7a1d7de3871" width='700'>\
<img src="https://github.com/wzhang1998/houdini_flipbook_maker/assets/67906283/d3625a24-6352-411a-a3a9-0216136627e9" width='700'>

- Generate flipbooks from one or multiple cameras.
- Add a text overlay to each frame: suport versioning and notes.
- Control the size and position of the text overlay.
- Encode the flipbook frames into a video file (MP4 or GIF).
- Support for multiple resolutions: You can choose different resolutions: 100% 50% 75% 25%.

