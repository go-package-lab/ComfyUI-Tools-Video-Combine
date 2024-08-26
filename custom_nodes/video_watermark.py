import logging


class VideoWatermark:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
                "watermark_enable": ("BOOLEAN", {"default": False}),
                "watermark_filename": ("STRING", {"default": "watermark.png"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    CATEGORY = "Tools:VideoWatermarkMultiline"
    OUTPUT_NODE = True

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "doit"

    # def doit(self, text, prompt=None, extra_pnginfo=None, unique_id=None):
    def doit(self, text,  prompt=None, extra_pnginfo=None, unique_id=None,watermark_enable=None, watermark_filename=None):
        logging.info("[ComfyUI-Tools-Watermark]watermark_enable: {},watermark_filename:{}".format(watermark_enable,                                                                                         watermark_filename))
        return {"ui": {"string": [text, unique_id, ]}, "result": (text, unique_id,)}

NODE_CLASS_MAPPINGS = {
    "Tools:VideoWatermark": VideoWatermark,
}

# 节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Tools:VideoWatermark": "VideoWatermark 🅜🅒",
}
