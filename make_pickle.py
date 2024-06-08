import pickle
import os

def create_or_load_class_mapping(pickle_file_path):
    # 미리 정의된 클래스 매핑
    class_mapping = {
        'Bonobono': 0,
        'Eagle': 1,
        'Gmarket': 2,
        'Hp': 3,
        'Intel': 4,
        'Underwood': 5,
        'Wonju': 6,
        'Yonsei': 7,
        'Zeroground': 8
    }
    
    # pickle 파일이 존재하지 않으면 생성
    if not os.path.exists(pickle_file_path):
        print("Pickle 파일을 생성합니다.")
        
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(class_mapping, f)
        
        return class_mapping
    else:
        # pickle 파일이 존재하면 로드
        print("Pickle 파일을 로드합니다.")
        with open(pickle_file_path, 'rb') as f:
            class_mapping = pickle.load(f)
        
        return class_mapping
    
# 함수를 호출하여 class_mapping 생성 또는 로드
pickle_file_path = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\class9.pickle'
class_mapping = create_or_load_class_mapping(pickle_file_path)