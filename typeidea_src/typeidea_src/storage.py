from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont

class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # 逻辑处理
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, 'Damon', 'red')
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    @staticmethod
    def convert_image_to_file(image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    @staticmethod
    def watermark_with_text(file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            # 默认字体
            font = ImageFont.truetype("consola.ttf", 30)
        text_width, text_height = draw.textsize(text, font)
        text_x = (width - text_width - margin) / 2 # 计算横轴位置
        text_y = height - text_height - margin # 计算纵轴位置
        draw.text((text_x, text_y), text, color, font)
        return image
