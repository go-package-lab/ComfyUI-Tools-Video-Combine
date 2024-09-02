import os
import subprocess

import logging
import time
from datetime import datetime

import torch

import folder_paths
from nodes import SaveImage

effect = ["fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown",
          "circlecrop", "rectcrop", "distance", "fadeblack", "fadewhite", "radial", "smoothleft", "smoothright",
          "smoothup", "smoothdown", "circleopen", "circleclose", "vertopen", "vertclose", "horzopen", "horzclose",
          "dissolve", "pixelize", "diagtl", "diagtr", "diagbl", "diagbr", "hlslice", "hrslice", "vuslice", "vdslice",
          "hblur", "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr", "squeezeh", "squeezev", "zoomin", "fadefast",
          "fadeslow", "hlwind", "hrwind", "vuwind", "vdwind", "coverleft", "coverright", "coverup", "coverdown",
          "revealleft", "revealright", "revealup", "revealdown"]


class Image2video:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE", ),
                "image_2": ("IMAGE", ),
                "image_effect_1_2": (effect,),
                "image_effect_2_3": (effect,),
                "image_effect_3_4": (effect,),
                "image_effect_4_5": (effect,),
                "image_duration": ("INT", {"default": 3}),
                "effect_duration": ("INT", {"default": 3}),
                "video_width": ("INT", {"default": 720}),
                "video_height": ("INT", {"default": 1280}),
                "filename_prefix": ("STRING", {"default": "TaskId"}),
            },
            "optional": {
                "image_3": ("IMAGE", ),
                "image_4": ("IMAGE", ),
                "image_5": ("IMAGE", ),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:Image2videoMultiline"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Filename",)
    FUNCTION = "doit"



    def doit(self, image_1, image_2, image_duration, effect_duration, video_width,video_height,image_3=None, image_4=None, image_5=None, image_effect_1_2=None, image_effect_2_3=None, image_effect_3_4=None, image_effect_4_5=None, unique_id=None,filename_prefix=None):
        logging.info("[ComfyUI-Tools-Video-Combine] 图片转视频image_effect_1_2: {}".format(image_effect_1_2))
        output_dir = folder_paths.get_output_directory()

        save_data=SaveImage().save_images(image_1, filename_prefix)
        image_1_path = output_dir+"/"+save_data['ui']['images'][0]['filename']

        save_data=SaveImage().save_images(image_2, filename_prefix)
        image_2_path = output_dir+"/"+save_data['ui']['images'][0]['filename']
        # 视频尺寸
        scale=f"{video_width}:{video_height}"

        # 生成新的文件名
        custom_time_str = datetime.now().strftime("%m%d-%H_%M_%S")
        output_video_path = os.path.join(output_dir, filename_prefix + custom_time_str+".mp4")

        command = []
        total_image=2
        image_3_path=""
        image_4_path=""
        image_5_path=""


        if image_3 is not None:
            total_image=3
            save_data = SaveImage().save_images(image_3, filename_prefix)
            image_3_path = output_dir + "/" + save_data['ui']['images'][0]['filename']
        if image_4 is not None:
            total_image=4
            save_data = SaveImage().save_images(image_4, filename_prefix)
            image_4_path = output_dir + "/" + save_data['ui']['images'][0]['filename']
        if image_5 is not None:
            total_image=5
            save_data = SaveImage().save_images(image_5, filename_prefix)
            image_5_path = output_dir + "/" + save_data['ui']['images'][0]['filename']

        image_total_basic_second = image_duration + effect_duration
        image_total_effect_second = image_duration + effect_duration + effect_duration

        if total_image==2:
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_1_path,
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_2_path,
                "-filter_complex", (
                    f"[0:v]scale={scale},setsar=1[v0];"
                    f"[1:v]scale={scale},setsar=1[v1];"
                    f"[v0][v1]xfade=transition={image_effect_1_2}:duration={effect_duration}:offset={image_duration}[v01];"
                ),
                "-map", "[v01]",
                "-pix_fmt", "yuv420p",
                output_video_path
            ]
        elif total_image==3:
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_1_path,
                "-loop", "1",
                "-t", str(image_total_effect_second),
                "-i", image_2_path,
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_3_path,
                "-filter_complex", (
                    f"[0:v]scale={scale},setsar=1[v0];"
                    f"[1:v]scale={scale},setsar=1[v1];"
                    f"[2:v]scale={scale},setsar=1[v2];"
                    f"[v0][v1]xfade=transition={image_effect_1_2}:duration={effect_duration}:offset={image_duration}[v01];"
                    f"[v01][v2]xfade=transition={image_effect_2_3}:duration={effect_duration}:offset={image_duration*2+effect_duration}[v02];"
                ),
                "-map", "[v02]",
                "-pix_fmt", "yuv420p",
                output_video_path
            ]
        elif total_image==4:
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_1_path,
                "-loop", "1",
                "-t", str(image_total_effect_second),
                "-i", image_2_path,
                "-loop", "1",
                "-t", str(image_total_effect_second),
                "-i", image_3_path,
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_4_path,
                "-filter_complex", (
                    f"[0:v]scale={scale},setsar=1[v0];"
                    f"[1:v]scale={scale},setsar=1[v1];"
                    f"[2:v]scale={scale},setsar=1[v2];"
                    f"[3:v]scale={scale},setsar=1[v3];"
                    f"[v0][v1]xfade=transition={image_effect_1_2}:duration={effect_duration}:offset={image_duration}[v01];"
                    f"[v01][v2]xfade=transition={image_effect_2_3}:duration={effect_duration}:offset={image_duration*2+effect_duration}[v02];"
                    f"[v02][v3]xfade=transition={image_effect_3_4}:duration={effect_duration}:offset={image_duration*3+effect_duration}[v03];"
                ),
                "-map", "[v03]",
                "-pix_fmt", "yuv420p",
                output_video_path
            ]
        elif total_image==5:
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_1_path,
                "-loop", "1",
                "-t", str(image_total_effect_second),
                "-i", image_2_path,
                "-loop", "1",
                "-t", str(image_total_effect_second),
                "-i", image_3_path,
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_4_path,
                "-loop", "1",
                "-t", str(image_total_basic_second),
                "-i", image_5_path,
                "-filter_complex", (
                    f"[0:v]scale={scale},setsar=1[v0];"
                    f"[1:v]scale={scale},setsar=1[v1];"
                    f"[2:v]scale={scale},setsar=1[v2];"
                    f"[3:v]scale={scale},setsar=1[v3];"
                    f"[4:v]scale={scale},setsar=1[v4];"
                    f"[v0][v1]xfade=transition={image_effect_1_2}:duration={effect_duration}:offset={image_duration}[v01];"
                    f"[v01][v2]xfade=transition={image_effect_2_3}:duration={effect_duration}:offset={image_duration*2+effect_duration}[v02];"
                    f"[v02][v3]xfade=transition={image_effect_3_4}:duration={effect_duration}:offset={image_duration*3+effect_duration}[v03];"
                    f"[v03][v4]xfade=transition={image_effect_4_5}:duration={effect_duration}:offset={image_duration*4+effect_duration}[v04];"
                ),
                "-map", "[v04]",
                "-pix_fmt", "yuv420p",
                output_video_path
            ]

        # 将列表中的元素组合成一个字符串
        command_str = " ".join(command)
        logging.info(f"[ComfyUI-Tools-Video-Combine]image2video command: {command_str}")

        try:
            # 执行 ffmpeg 命令
            subprocess.run(command, check=True)
            logging.info(f"[ComfyUI-Tools-Video-Combine] Video processed successfully. Output saved to {output_video_path}")
        except subprocess.CalledProcessError as e:
            error_message = f"[ComfyUI-Tools-Video-Combine] Error processing video: {str(e)}"
            logging.error(error_message)
            raise Exception(error_message)

        short_output_video = os.path.basename(output_video_path)

        out_datas = [
            {
                "filename": short_output_video,
                "subfolder": "",
                "type": "output",
                "format": "video/h264-mp4",
                "frame_rate": -1
            }
        ]
        return {"ui": {"gifs": out_datas}, "result": (output_video_path,)}

    def generate_new_filename(self, file_path, suffix):
        # 获取文件名和扩展名
        base_name, ext = os.path.splitext(file_path)
        # 生成新的文件名
        new_file_path = f"{base_name}{suffix}{ext}"
        return new_file_path


NODE_CLASS_MAPPINGS = {
    "Tools:Image2video": Image2video,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:Image2video": "Image2video 🅜🅒",
}