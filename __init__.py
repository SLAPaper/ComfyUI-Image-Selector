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

import torch


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

    def run(self, images: torch.Tensor, selected_indexes: tg.Text):
        shape = images.shape
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
            print(f"ImageSelector: selected: {len(selected_index)} latents")
            return (images[selected_index, :, :, :], )

        print(f"ImageSelector: selected no latents, passthrough")
        return (images, )


class ImageDuplicator:
    """
    Duplicate each images and pipe through
    """

    def __init__(self):
        self._name = "ImageDuplicator"
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Input: copies you want to get
        """
        return {
            "required": {
                "images": ("IMAGE", ),
                "dup_times": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 16,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "run"

    OUTPUT_NODE = False

    CATEGORY = "image"

    def run(self, images: torch.Tensor, dup_times: int):

        tensor_list = [images
                       ] + [torch.clone(images) for _ in range(dup_times - 1)]

        print(
            f"ImageDuplicator: dup {dup_times} times,",
            f"return {len(tensor_list)} images",
        )
        return (torch.cat(tensor_list), )


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

    def run(self, latent_image: tg.Mapping[tg.Text, torch.Tensor],
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
            print(f"LatentSelector: selected: {len(selected_index)} latents")
            return ({'samples': samples[selected_index, :, :, :]}, )

        print(f"LatentSelector: selected no latents, passthrough")
        return (latent_image, )


class LatentDuplicator:
    """
    Duplicate each latent images and pipe through
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Input: copies you want to get
        """
        return {
            "required": {
                "latent_image": ("LATENT", ),
                "dup_times": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 16,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("LATENT", )
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "run"

    OUTPUT_NODE = False

    CATEGORY = "latent"

    def run(self, latent_image: tg.Mapping[tg.Text, torch.Tensor],
            dup_times: int):
        samples = latent_image['samples']

        sample_list = [samples] + [
            torch.clone(samples) for _ in range(dup_times - 1)
        ]

        print(
            f"LatentDuplicator: dup {dup_times} times,",
            f"return {len(sample_list)} images",
        )
        return ({
            'samples': torch.cat(sample_list),
        }, )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageSelector": ImageSelector,
    "ImageDuplicator": ImageDuplicator,
    "LatentSelector": LatentSelector,
    "LatentDuplicator": LatentDuplicator
}
