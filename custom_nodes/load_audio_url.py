import hashlib
import logging
import os
import subprocess
import uuid
from urllib.parse import urlparse

import requests

import folder_paths

def strip_url_parameters(url):
    parsed_url = urlparse(url)
    clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    return clean_url

def md5_hash(url):
    hash_md5 = hashlib.md5(url.encode())
    return hash_md5.hexdigest()


class LoadAudioUrl:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("BOOLEAN", {"default": False}),
                "audio_url": ("STRING", {"default": "", "multiline": True}),
                "duration": ("FLOAT", {"default": 9}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional":{

            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:LoadAudioUrlMultiline"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Audio",)
    FUNCTION = "doit"

    def doit(self, audio_url, switch=False, duration=0, seed=0, unique_id=None):
        if switch==False or audio_url == '':
            return {"result": ("", 0,)}
        logging.info("[ComfyUI-Tools-Video-Combine]LoadAudioUrl,{},duration:{}".format(audio_url,duration))
        input_dir = folder_paths.get_input_directory()
        output_dir = folder_paths.get_output_directory()
        audio_file = audio_url.strip()

        if audio_file.startswith("http://") or audio_file.startswith("https://"):
            strip_url = strip_url_parameters(audio_file)
            md5_name = md5_hash(strip_url) + os.path.splitext(strip_url)[-1]
            local_file = os.path.join(input_dir, md5_name)

            # Check if the file already exists locally
            if not os.path.exists(local_file):
                # Download the file
                logging.info("下载音频文件: " + strip_url + "")
                response = requests.get(audio_file, timeout=(5, 10))
                if response.status_code == 200:
                    with open(local_file, 'wb') as f:
                        f.write(response.content)
                else:
                    raise Exception(f"Failed to download audio file from URL: {audio_file}")
            audio_file = local_file
        else:
            raise Exception("audio url error")
        # ffmpeg -i input.mp3 -ss 00:00:00 -to 00:02:00 -c copy cut_audio.mp3
        formatted_time = self.format_seconds(duration)
        print(f"Formatted time: {formatted_time}")

        uuid_str = uuid.uuid4()

        # 在 ffmpeg 命令中使用
        output_file = output_dir + "/" + str(uuid_str) + f".mp3"

        start_time = "00:00:00"

        # ffmpeg_command = f"ffmpeg -i {input_file} -ss {start_time} -to {formatted_time} -c copy {output_file}"
        # print(f"FFmpeg Command: {ffmpeg_command}")
        # 构建 ffmpeg 命令
        command = [
            "ffmpeg",
            "-v", "error",
            "-y",
            "-i", audio_file,
            "-ss", start_time,
            "-to", formatted_time,
            "-c", "copy",
            output_file
        ]
        # 将列表中的元素组合成一个字符串
        command_str = " ".join(command)
        logging.info(f"[ComfyUI-Tools-Video-Combine]command: {command_str}")

        try:
            # 执行 ffmpeg 命令
            subprocess.run(command, check=True)
            logging.info(f"[ComfyUI-Tools-Video-Combine]Video processed successfully. Output saved to {output_file}")
        except subprocess.CalledProcessError as e:
            error_message = f"[ComfyUI-Tools-Video-Combine]Error processing video: {str(e)}"
            logging.error(error_message)
            raise Exception(error_message)

        out_datas = [
            {
                "type": "output",
            }
        ]
        return {"ui": {"datas": out_datas}, "result": (output_file,duration,)}

    def generate_new_filename(self, file_path, suffix):
        # 获取文件名和扩展名
        base_name, ext = os.path.splitext(file_path)
        # 生成新的文件名
        new_file_path = f"{base_name}{suffix}{ext}"
        return new_file_path
    def format_seconds(self,seconds):
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
NODE_CLASS_MAPPINGS = {
    "Tools:LoadAudioUrl": LoadAudioUrl,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:LoadAudioUrl": "LoadAudioUrl 🅜🅒",
}
