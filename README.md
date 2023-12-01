# ComfyUI-Image-Selector

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which can select one or some of images from a batch.

## Background

ComfyUI dosn't handle batch generation seeds like A1111 WebUI do (See [Issue #165](https://github.com/comfyanonymous/ComfyUI/issues/165)), so you can't simply increase the generation seed to get the desire image from a batch generation.

So here is a simple node that can select some of the images from a batch and pipe through for further use, such as scaling up or "hires fix".

Or you can use PreviewImage Node to go through all the images, and then rewire SaveImage with ImageSelector to save the one you want.

## Install

Clone this repo into `custom_nodes` directory of ComfyUI location

## Usage

### ImageSelector & ImageDuplicator

Both nodes can be found in `image` category.

Selector takes a list of selected indexes, start with 1 (not 0, sorry), seperated by comma, and outputs only the selected images from input images.

**New in 2023/12/2:** Support range selection with left bound included and right bound excluded, see example below.

For example:

1. `1`: select the first image
2. `1,3,4,6,7`: select the 1st, 3rd, 4th, 6th and 7th image
3. `2:`: select 2nd, 3rd, ..., till the last image (omit the first image)
4. `:0`: select 1st, 2nd, ..., till the second last image (omit the last image)
5. `3:-1`: select 3rd, 4th, ..., till the third last image (omit first two and last two images)

All indexes that cannot convert to integer or out of bounds will be ignored.

Duplicator takes a number and duplicates input images by given times.

![Snipaste_2023-08-14_23-42-04](https://github.com/SLAPaper/ComfyUI-Image-Selector/assets/7543632/f8d4a3ca-4ee5-4947-9bf5-ea847f392716)


### LatentSelector & LatentDuplicator

Both nodes can be found in `latent` category.

The parameters and functionality is just like the image counterpart, but for latents

![Snipaste_2023-08-14_23-44-02](https://github.com/SLAPaper/ComfyUI-Image-Selector/assets/7543632/220759af-3b06-42fa-9332-43bff3744857)

## Tips

VAE Decode & Encode takes time and vram, so better avoid uneccessary VAE node. If must, do it with as few images/latents as possible. In general,
- `encode/decode -> duplicator` is better than `duplicator -> encode/decode`
- `selector -> encode/decode` is better than `encode/decode -> selector`
