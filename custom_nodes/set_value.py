import logging
import os
import shutil
import subprocess

import torch

import folder_paths


class SetValue:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {"default": 1, "min": 0, "max": 0xffffffffffffffff}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:SetValue"
    OUTPUT_NODE = True

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    FUNCTION = "doit"

    def doit(self, int=0,unique_id=None):

        return {"result": (int,)}


NODE_CLASS_MAPPINGS = {
    "Tools:SetValue": SetValue,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:SetValue": "SetValue 🅜🅒",
}
