import logging
import os
import subprocess

import folder_paths


class VideoWatermark:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
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

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "doit"

    def doit(self, text,  prompt=None, extra_pnginfo=None, unique_id=None,enable_watermark=None, watermark_image=None):
        logging.info("[ComfyUI-Tools-Watermark]enable_watermark: {},watermark_image:{}".format(enable_watermark,watermark_image))
        logging.info("校验是否需要添加水印")
        if enable_watermark and watermark_image != "":
            logging.info("需要添加水印")
            # output_file_with_audio = f"{filename}_{counter:05}-watermark.{video_format['extension']}"
            # output_file_with_audio_path = os.path.join(full_output_folder, output_file_with_audio)
            input_dir = folder_paths.get_input_directory()
            watermark_filename = os.path.join(input_dir, watermark_image)
            logging.info(watermark_filename)
            output_video = "/Users/wcj/workspace/ai/ComfyUI/output/test.mp4"
            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-v", "error",
                "-n", ""
                "-i", text,
                "-i", watermark_filename,
                "-filter_complex", "overlay=W-w-100:H-h-26",
                output_video
            ]

            try:
                # 执行 ffmpeg 命令
                subprocess.run(command, check=True)
                logging.info(f"Video processed successfully. Output saved to {output_video}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error processing video: {e}")
        else:
            logging.info("Watermark not enabled, skipping watermark processing.")


        return {"ui": {"string": [text, unique_id, ]}, "result": (text, unique_id,)}

NODE_CLASS_MAPPINGS = {
    "Tools:VideoWatermark": VideoWatermark,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:VideoWatermark": "VideoWatermark 🅜🅒",
}
