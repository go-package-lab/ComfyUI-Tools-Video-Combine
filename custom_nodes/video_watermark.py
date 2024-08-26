import logging
import os
import subprocess

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
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:VideoWatermarkMultiline"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Filename",)
    FUNCTION = "doit"

    def doit(self, text, prompt=None, extra_pnginfo=None, unique_id=None, enable_watermark=None, watermark_image=None):
        logging.info("[ComfyUI-Tools-Watermark]校验是否需要添加水印,enable_watermark: {}, watermark_image:{}".format(enable_watermark, watermark_image))
        output_video = text
        output_dir = folder_paths.get_output_directory() + "/"

        if enable_watermark and watermark_image:
            logging.info("需要添加水印")
            input_dir = folder_paths.get_input_directory()
            watermark_filename = os.path.join(input_dir, watermark_image)
            logging.info(watermark_filename)

            # 生成新的文件名
            output_video = self.generate_new_filename(text, "-watermark")

            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-v", "error",
                "-y",
                "-i", text,
                "-i", watermark_filename,
                "-filter_complex", "overlay=W-w-100:H-h-26",
                output_video
            ]

            try:
                # 执行 ffmpeg 命令
                subprocess.run(command, check=True)
                logging.info(f"[ComfyUI-Tools-Watermark]Video processed successfully. Output saved to {output_video}")
            except subprocess.CalledProcessError as e:
                error_message = f"[ComfyUI-Tools-Watermark]Error processing video: {str(e)}"
                logging.error(error_message)
                raise Exception(error_message)
        else:
            logging.info("[ComfyUI-Tools-Watermark]Watermark not enabled, skipping watermark processing.")

        # return {"ui": {"string": [output_video, unique_id]}, "result": (output_video, unique_id)}

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
