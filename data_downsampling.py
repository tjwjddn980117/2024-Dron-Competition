import os
from PIL import Image

class CFG:
    DOWNSAMPLED_WIDTH = 100
    DOWNSAMPLED_HEIGHT = 100

# 원본 폴더와 새 폴더 경로 설정
folder_path = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\'
original_folder = folder_path + 'Datas_3000_3000'
new_folder = folder_path + 'Datas_3000_3000_downsampling'

# 새 폴더가 없으면 생성
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# 다운샘플링할 이미지 크기
new_size = (100, 100)

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