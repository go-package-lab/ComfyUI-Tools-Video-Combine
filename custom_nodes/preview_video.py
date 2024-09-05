import logging
import os
import shutil
import subprocess

import torch

import folder_paths


class PreviewVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"forceInput": True}),
            },
        }

    CATEGORY = "Tools:PreviewVideo"
    OUTPUT_NODE = True

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "doit"

    def doit(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui": {"video": [video_name, video_path_name]}}


NODE_CLASS_MAPPINGS = {
    "Tools:PreviewVideo": PreviewVideo,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:PreviewVideo": "PreviewVideo 🅜🅒",
}
