# Copyright 2023 SLAPaper
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing as tg


class ImageSelector:
    """
    Select some of the images and pipe through
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Input: list of index of selected image, seperated by comma
        Indexes start with 1 for simplicity
        """
        return {
            "required": {
                "images": ("IMAGE", ),
                "selected_indexes": ("STRING", {
                    "multiline": False,
                    "default": "1,2,3"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "run"

    OUTPUT_NODE = False

    CATEGORY = "image"

    def run(self, images: tg.Sequence[tg.Any], selected_indexes: tg.Text):
        res_images: tg.List[tg.Any] = []
        for s in selected_indexes.strip().split(','):
            try:
                x: int = int(s.strip()) - 1
                if x < len(images):
                    res_images.append(images[x])
            except:
                pass

        if res_images:
            return (res_images, )

        return (images, )


class LatentSelector:
    """
    Select some of the latent images and pipe through
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Input: list of index of selected image, seperated by comma
        Indexes start with 1 for simplicity
        """
        return {
            "required": {
                "latent_image": ("LATENT", ),
                "selected_indexes": ("STRING", {
                    "multiline": False,
                    "default": "1,2,3"
                }),
            },
        }

    RETURN_TYPES = ("LATENT", )
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "run"

    OUTPUT_NODE = False

    CATEGORY = "latent"

    def run(self, latent_image: tg.Sequence[tg.Any],
            selected_indexes: tg.Text):
        samples = latent_image['samples']
        shape = samples.shape
        len_first_dim = shape[0]

        selected_index: tg.List[int] = []
        for s in selected_indexes.strip().split(','):
            try:
                x: int = int(s.strip()) - 1
                if x < len_first_dim:
                    selected_index.append(x)
            except:
                pass

        if selected_index:
            return ({'samples': samples[selected_index, :, :, :]}, )

        return (latent_image, )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageSelector": ImageSelector,
    "LatentSelector": LatentSelector
}
