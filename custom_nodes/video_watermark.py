import logging
import os
import subprocess

import torch

import folder_paths


class VideoWatermark:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
                "enable_watermark": ("BOOLEAN", {"default": False}),
                "watermark_image": ("STRING", {"default": "watermark.png"}),
            },
            "optional": {
                "audio": ("STRING", {"forceInput": True, "multiline": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:VideoWatermarkMultiline"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Filename",)
    FUNCTION = "doit"

    def doit(self, text,audio=None, prompt=None, extra_pnginfo=None, unique_id=None, enable_watermark=None, watermark_image=None):
        logging.info("[ComfyUI-Tools-Video-Combine]校验是否需要添加水印,enable_watermark: {}, watermark_image:{},audio:{}".format(enable_watermark, watermark_image, audio))
        output_video = text
        output_dir = folder_paths.get_output_directory() + "/"
        input_dir = folder_paths.get_input_directory()

        # 添加水印判断
        if enable_watermark and watermark_image:
            logging.info("需要添加水印")
            watermark_filename = os.path.join(input_dir, watermark_image)
            logging.info(watermark_filename)

            # 生成新的文件名
            output_video = self.generate_new_filename(text, "-watermark")
# -c:v libx264
            device = "cuda" if torch.cuda.is_available() else "cpu"
            cv_name = "libx264"
            if device=="cuda":
                cv_name = "h264_nvenc"
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-v", "error",
                "-y",
                "-i", text,
                "-i", watermark_filename,
                "-c:v", cv_name,
                "-filter_complex", "overlay=W-w-100:H-h-26",
                output_video
            ]
            # -c:v h264_nvenc

            # 将列表中的元素组合成一个字符串
            command_str = " ".join(command)
            logging.info(f"[ComfyUI-Tools-Video-Combine]command: {command_str}")

            try:
                # 执行 ffmpeg 命令
                subprocess.run(command, check=True)
                logging.info(f"[ComfyUI-Tools-Video-Combine]Video processed successfully. Output saved to {output_video}")
            except subprocess.CalledProcessError as e:
                error_message = f"[ComfyUI-Tools-Video-Combine]Error processing video: {str(e)}"
                logging.error(error_message)
                raise Exception(error_message)
        else:
            logging.info("[ComfyUI-Tools-Video-Combine]Watermark not enabled, skipping watermark processing.")

        # 添加音频判断
        if audio is not None and audio!= "":
            logging.info("需要添加音频")
            watermark_filename = os.path.join(input_dir, watermark_image)
            logging.info(watermark_filename)

            src_video = output_video
            # 生成新的文件名
            output_video = self.generate_new_filename(output_video, "-au")

            # ffmpeg -v error -y -i /Users/wcj/workspace/ai/ComfyUI/output/ai_00038-watermark.mp4 -i /Users/wcj/workspace/ai/ComfyUI/output/eea0abe2-8131-4729-af0e-955b8dd23f4a.mp3 -c:v copy -c:a aac -b:a 192k -map 0:v -map 1:a /Users/wcj/workspace/ai/ComfyUI/output/ai_00038-watermark-au.mp4
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-v", "error",
                "-y",
                "-i", src_video,
                "-i", audio,
                "-c:v", "copy",
                "-c:a", "aac",
                "-strict", "experimental",
                "-map", "0:v",
                "-map", "1:a",
                output_video
            ]


            # 将列表中的元素组合成一个字符串
            command_str = " ".join(command)
            logging.info(f"[ComfyUI-Tools-Video-Combine]command: {command_str}")

            try:
                # 执行 ffmpeg 命令
                subprocess.run(command, check=True)
                logging.info(f"[ComfyUI-Tools-Video-Combine]Video processed successfully. Output saved to {output_video}")
            except subprocess.CalledProcessError as e:
                error_message = f"[ComfyUI-Tools-Video-Combine]Error processing video: {str(e)}"
                logging.error(error_message)
                raise Exception(error_message)
        else:
            logging.info("[ComfyUI-Tools-Video-Combine]audio not enabled, skipping audio processing.")

        short_output_video = output_video.replace(output_dir,"")
        short_input_video = text.replace(output_dir,"")

        out_datas = [
            {
                "input": short_input_video,
                "out_video": short_output_video,
                "type": "output",
            }
        ]
        return {"ui": {"datas": out_datas}, "result": (output_video,)}

    def generate_new_filename(self, file_path, suffix):
        # 获取文件名和扩展名
        base_name, ext = os.path.splitext(file_path)
        # 生成新的文件名
        new_file_path = f"{base_name}{suffix}{ext}"
        return new_file_path

NODE_CLASS_MAPPINGS = {
    "Tools:VideoWatermark": VideoWatermark,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:VideoWatermark": "VideoWatermark 🅜🅒",
}
