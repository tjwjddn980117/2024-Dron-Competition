import os
from PIL import Image, ImageOps
import glob

class CFG:
    WIDTH = 3000
    HEIGHT = 2250

# 원본 폴더와 새 폴더 경로 설정
folder_path = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\'
original_folder = folder_path + 'Datas'
new_folder = folder_path + f'Datas_{CFG.WIDTH}_{CFG.HEIGHT}'

# 새 폴더가 없으면 생성
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# 폴더 내 이미지 파일을 순회하며 처리
for subdir, _, files in os.walk(original_folder):
    for file in files:
        if file.lower().endswith(('.jpg', '.JPG')):
            # 원본 파일 경로
            original_path = os.path.join(subdir, file)
            
            # 새로운 파일 경로 생성 (확장자 통일)
            relative_path = os.path.relpath(subdir, original_folder)
            new_subdir = os.path.join(new_folder, relative_path)
            if not os.path.exists(new_subdir):
                os.makedirs(new_subdir)
            
            new_file_name = os.path.splitext(file)[0] + '.jpg'
            new_path = os.path.join(new_subdir, new_file_name)

            # 이미지 열기 및 EXIF 데이터를 고려하여 올바른 방향으로 회전
            with Image.open(original_path) as img:
                img = ImageOps.exif_transpose(img)
                width, height = img.size
                new_width, new_height = CFG.WIDTH, CFG.HEIGHT
                left = (width - new_width) / 2
                top = (height - new_height) / 2
                right = (width + new_width) / 2
                bottom = (height + new_height) / 2

                # 크롭 및 저장
                img_cropped = img.crop((left, top, right, bottom))
                img_cropped.save(new_path)

print("이미지 크롭 및 저장이 완료되었습니다.")