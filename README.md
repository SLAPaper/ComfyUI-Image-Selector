# ComfyUI-Image-Selector

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which can select one or some of images from a batch.

## Background

ComfyUI dosn't handle batch generation seeds like A1111 WebUI do (See [Issue #165](https://github.com/comfyanonymous/ComfyUI/issues/165)), so you can't simply increase the generation seed to get the desire image from a batch generation.

So here is a simple node that can select some of the images from a batch and pipe through for further use, such as scaling up or "hires fix".

Or you can use PreviewImage Node to go through all the images, and then rewire SaveImage with ImageSelector to save the one you want.

## Install

Clone this repo into `custom_nodes` directory of ComfyUI location

## Usage

### Selectors

There are two Selector nodes, one is `ImageSelector` under `image` category, another is `LatentSelecotr` under `latent` category. One is for images and one for latent images.

Input: a list of selected indexes, start with 1 (not 0, sorry), seperated by comma.

For example:

1. `1`: select the first image
2. `1,3,4,6,7`: select the 1st, 3rd, 4th, 6th and 7th image

All indexes that cannot convert to integer or out of bounds will be ignored.

### Duplicators

There are two Duplicator nodes, `ImageDuplicator` and `LatentDuplicator`.

These two can duplicate the image / latent image (after you selected), so that in further steps you still can run in batch.

Example in txt2img:

`EmptyLatentImage(batch 4) -> KSampler(batch 4) -> LatentSelector(select 1) -> LatentDuplicator(duplicate 4) -> LatentUpscale(batch 4) -> VaeDecode(batch 4) -> ImageSelector(select 1) -> SaveImage`

Or in img2img:

`LoadImage(batch 1) -> ImageDuplicator(duplicate 4) -> VaeEncode(batch 4) -> KSampler(batch 4) -> VaeDecode(batch 4) -> ImageSelector(select 1) -> SaveImage`
