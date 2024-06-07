import os
import shutil
from sklearn.model_selection import train_test_split
# Google Drive의 특정 폴더 경로 설정
data_dir = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\Datas_3000_2250\\'
train_dir = os.path.join(data_dir, 'train')
valid_dir = os.path.join(data_dir, 'valid')

# train 및 valid 디렉토리를 생성합니다.
os.makedirs(train_dir, exist_ok=True)
os.makedirs(valid_dir, exist_ok=True)
# Split ratio 설정
train_ratio = 0.8

# 서브폴더 목록을 가져옵니다.
subfolders = [f.name for f in os.scandir(data_dir) if f.is_dir() and f.name not in ['train', 'valid']]

for subfolder in subfolders:
    # 각각의 train 및 valid 서브폴더를 생성합니다.
    os.makedirs(os.path.join(train_dir, subfolder), exist_ok=True)
    os.makedirs(os.path.join(valid_dir, subfolder), exist_ok=True)
    
    # 현재 서브폴더 내의 파일 목록을 가져옵니다.
    file_list = [f for f in os.listdir(os.path.join(data_dir, subfolder)) if os.path.isfile(os.path.join(data_dir, subfolder, f))]
    
    # 파일 목록을 train과 valid 세트로 나눕니다.
    train_files, valid_files = train_test_split(file_list, train_size=train_ratio, random_state=42)
    
    # 파일들을 train 폴더로 복사합니다.
    for file in train_files:
        src = os.path.join(data_dir, subfolder, file)
        dst = os.path.join(train_dir, subfolder, file)
        shutil.copy2(src, dst)
    
    # 파일들을 valid 폴더로 복사합니다.
    for file in valid_files:
        src = os.path.join(data_dir, subfolder, file)
        dst = os.path.join(valid_dir, subfolder, file)
        shutil.copy2(src, dst)

print("Data split into train and valid sets successfully.")
