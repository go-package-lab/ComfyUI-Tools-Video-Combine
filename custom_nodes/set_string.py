import logging
import os
import shutil
import subprocess

import torch

import folder_paths


class SetString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": True}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:SetString"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "doit"

    def doit(self, string="",unique_id=None):

        return {"result": (string,)}


NODE_CLASS_MAPPINGS = {
    "Tools:SetString": SetString,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:SetString": "SetString 🅜🅒",
}
