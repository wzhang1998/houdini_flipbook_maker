# Houdini Flipbook Maker

A plugin for Houdini that allows you to render multiple cameras at once, supports multiple resolutions, adds overlay text for camera/frame/notes, and exports the output in GIF or MP4 format.
Inspired by Danny Laursen's [Houdini Easy Flipbook HDA](https://dannylrsn.gumroad.com/l/lfgcnh)

## Usage

Before using this plugin, make sure you have installed [ffmpeg](https://ffmpeg.org/) and [ImageMagick](https://imagemagick.org/) on your system.

To add the `object_Wenyi.flipbook_maker.1.1.hdanc` to your Houdini project, follow these steps:

1. Download the HDA file from the plugin repository.
2. Open your Houdini project.
3. Go to the "Assets" tab in the Houdini interface.
4. Click on the "Install Digital Asset Library" button.
5. Browse and select the downloaded HDA file.
6. The plugin will be added to your Houdini project.

## Functions

The plugin provides the following functions: 

<img src="https://github.com/wzhang1998/houdini_flipbook_maker/assets/67906283/cd36f7bd-ae72-46c3-b41a-e3543e7b903c" width='600'>\
<img src="httpsttps://github.com/wzhang1998/houdini_flipbook_maker/assets/67906283/17257050-cd27-4485-b477-b0e6591e4968" width='600'>\
<img src="httpsttps://github.com/wzhang1998/houdini_flipbook_maker/assets/67906283/3b3fadec-89f5-4d41-b643-ae4cfc139e6a" width='600'>

- Generate flipbooks from one or multiple cameras.
- Add a text overlay to each frame: suport versioning and notes.
- Control the size and position of the text overlay.
- Encode the flipbook frames into a video file (MP4 or GIF).
- Support for multiple resolutions: You can choose different resolutions: 100% 50% 75% 25%.

