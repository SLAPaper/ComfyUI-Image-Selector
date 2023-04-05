# ComfyUI-Image-Selector

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which can select one or some of images from a batch.

## Background

ComfyUI dosn't handle batch generation seeds like A1111 WebUI do, so you can't simply increase the generation seed to get the desire image from a batch generation.

So here is a simple node that can select some of the images from a batch and pipe through for further use, such as scaling up or "hires fix".

Or you can use PreviewImage Node to go through all the images, and then rewire SaveImage with ImageSelector to save the one you want.

## Usage

Input: a list of selected indexes, start with 1 (not 0, sorry), seperated by comma.

For example (no surronding quotes):

1. "1": select the first image
2. "1,3,4,6,7": select the 1st, 3rd, 4th, 6th and 7th image

All indexes that cannot convert to integer or out of bounds will be ignored.
