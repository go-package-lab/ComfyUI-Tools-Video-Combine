import logging
import os
import shutil
import subprocess

import torch

import folder_paths


class CopyFile:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"forceInput": True, "multiline": False}),
                "target_dir": ("STRING", {"default": "nas"}),
                "subfolder": ("STRING", {"default": "taskid"}),
                "target_filename_suffix": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:CopyFile"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Filename",)
    FUNCTION = "doit"

    def doit(self, file_path,target_dir, subfolder,target_filename_suffix,seed,unique_id=None):
        logging.info("[ComfyUI-Tools-Video-Combine]文件拷贝,file_path: {}, target_dir:{},subfolder:{}".format(file_path, target_dir,subfolder))
        output_dir = folder_paths.get_output_directory()
        # 删除最后一层目录名
        parent_path = os.path.dirname(output_dir)

        nas_directory = os.path.join(parent_path, target_dir)

        # 获取文件名
        file_name = os.path.basename(file_path)
        # 获取文件名和扩展名
        base_name, ext = os.path.splitext(file_name)

        # 输出结果路径
        if subfolder=="":
            output_video_path = f"{nas_directory}/{base_name}{target_filename_suffix}{ext}"
        else:
            output_video_path = f"{nas_directory}/{subfolder}/video{target_filename_suffix}{ext}"

        # 获取目标目录路径
        destination_dir = os.path.dirname(output_video_path)
        # 如果目标目录不存在，则创建它
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # 拷贝文件
        shutil.copy(file_path, output_video_path)

        out_datas = [
            {
                "filename": output_video_path,
                "subfolder": subfolder,
                "type": "nas",
                "format": "video/h264-mp4",
                "frame_rate": -1
            }
        ]
        return {"ui": {"gifs": out_datas}, "result": (output_video_path,)}


NODE_CLASS_MAPPINGS = {
    "Tools:CopyFile": CopyFile,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:CopyFile": "CopyFile 🅜🅒",
}
