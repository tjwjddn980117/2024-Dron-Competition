'''
가지고 있는 image를 new_size에 맞추어서 강제로 해상도를 낮춘 후 데이터를 저장한다. 
이 코드는 '.jpg' 확장자만 읽는다. 

folder_path (str): 데이터들이 저장되어있는 주소. 
original_folder (str): 원본 데이터의 디렉토리 주소.
new_folder (str): 복사된 후 결과가 나올 디렉토리 주소. 
new_size (int, int): 낮출 해상도 (100, 100). 
'''

import os
from PIL import Image

class CFG:
    DOWNSAMPLED_WIDTH = 100
    DOWNSAMPLED_HEIGHT = 100

# 원본 폴더와 새 폴더 경로 설정
folder_path = ' '
original_folder = folder_path + 'Datas_3000_3000'
new_folder = folder_path + 'Datas_3000_3000_downsampling'

# 다운샘플링할 이미지 크기
new_size = (100, 100)

# 새 폴더가 없으면 생성
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# 폴더 구조를 유지하면서 이미지를 다운샘플링하여 새 폴더에 저장
for root, dirs, files in os.walk(original_folder):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jgp'):  # 확장자 필터링
            # 원본 이미지 경로
            original_path = os.path.join(root, file)
            # 새 이미지 경로
            new_path = original_path.replace(original_folder, new_folder)

            # 디렉토리 생성 (없으면)
            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            # 이미지 열기 및 리사이즈
            with Image.open(original_path) as img:
                img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
                img_resized.save(new_path)

print("다운샘플링 완료!")