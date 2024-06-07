'''
폴더 안에 있는 모든 이미지 파일들의 size 종류가 어떻게 되는지 체크하는 파일. 

이것을 통해 data_crop을 어떻게 해야할 지를 결정하려고 함. 

Input 되어지는 데이터들은 오직 '.jpg' 와 '.JPG'만을 받는다. 

ex) 
3024*3024: 1132개
4032*3024: 1292개
'''

import glob
from PIL import Image
from collections import defaultdict

# 폴더 경로 설정 (여기서는 'Datasets' 폴더 안을 대상으로 함)
folder_path = ' '

# 이미지 파일들의 사이즈와 해당 사이즈를 가진 파일의 개수를 저장할 딕셔너리
size_dict = defaultdict(int)

# 지정한 폴더 안의 .jpg 및 .JPG 파일들을 찾음
image_files = glob.glob(f'{folder_path}/**/*.[jJ][pP][gG]', recursive=True)

# 각 이미지 파일을 열어 사이즈를 확인하고, 사이즈별로 개수를 계산함
for image_file in image_files:
    with Image.open(image_file) as img:
        size = img.size  # (width, height) 형태의 튜플
        size_dict[size] += 1

# 사이즈별 이미지 파일의 개수를 출력함
for size, count in size_dict.items():
    print(f'{size[0]}*{size[1]}: {count}개')

