# 환경 설정 및 필요한 라이브러리 설치
!pip install tensorflow tensorflow_hub tf2onnx openvino-dev

# Google Drive 마운트
from google.colab import drive
drive.mount('/content/drive')

# 데이터셋 준비
import tensorflow as tf
import tensorflow_hub as hub
import os
import numpy as np
import pickle  # pickle 임포트 추가

# 데이터셋 경로 설정 (Google Drive에 있는 경로)
train_dir = '/content/drive/MyDrive/dataset/train'  # 'train' 폴더 경로
validation_dir = '/content/drive/MyDrive/dataset/validation'  # 'validation' 폴더 경로

# 클래스 레이블 추출 및 저장 (한 번 실행 후 주석 처리 가능)
class_names = sorted(os.listdir(train_dir))
with open('/content/drive/MyDrive/class_names.pkl', 'wb') as f:
    pickle.dump(class_names, f)

# 클래스 레이블 로드
with open('/content/drive/MyDrive/class_names.pkl', 'rb') as f:
    class_names = pickle.load(f)

# 클래스 이름에서 인덱스 얻기
class_to_index = {class_name: index for index, class_name in enumerate(class_names)}

# 데이터 전처리 함수
def preprocess(image, label):
    image = tf.image.resize(image, (224, 224)) / 255.0
    return image, label

# 이미지 로드 및 전처리 함수
def load_and_preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    # 이미지 경로에서 클래스 이름 추출
    class_name = tf.strings.split(image_path, os.sep)[-2]
    label = class_to_index[class_name.numpy().decode('utf-8')]
    return preprocess(image, label)

# 데이터셋 생성 함수
def create_dataset(directory):
    dataset = tf.data.Dataset.list_files(os.path.join(directory, '*/*'))
    def map_func(filepath):
        result = tf.py_function(func=load_and_preprocess_image, inp=[filepath], Tout=[tf.float32, tf.int32])
        result[0].set_shape((224, 224, 3))
        result[1].set_shape(())
        return result
    dataset = dataset.map(map_func)
    return dataset

# 데이터셋 크기 계산
train_dataset_size = len(tf.io.gfile.glob(train_dir + '/*/*'))
validation_dataset_size = len(tf.io.gfile.glob(validation_dir + '/*/*'))

# 로컬 데이터셋 로드 및 배치 처리
batch_size = 32
buffer_size = train_dataset_size  # 셔플 버퍼 크기를 train 데이터셋의 크기로 설정
ds_train = create_dataset(train_dir).shuffle(buffer_size).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
ds_val = create_dataset(validation_dir).shuffle(buffer_size).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)

# 모델 로드 및 커스터마이징
model_url = "https://tfhub.dev/tensorflow/efficientnet/b0/classification/1"
feature_extractor_layer = hub.KerasLayer(model_url, input_shape=(224, 224, 3), trainable=False)

model = tf.keras.Sequential([
    feature_extractor_layer,
    tf.keras.layers.Dense(len(class_names), activation='softmax')  # 데이터셋에 맞는 출력 레이어 (클래스 수에 맞게 조정)
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 모델 훈련
epochs = 5
history = model.fit(ds_train, validation_data=ds_val, epochs=epochs)

# ONNX로 모델 변환
import tf2onnx
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32),)
output_path = "efficientnet_b0.onnx"
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13)
with open(output_path, "wb") as f:
    f.write(model_proto.SerializeToString())

# OpenVINO로 모델 최적화 및 추론
from openvino.runtime import Core

ie = Core()
model_onnx_path = "/content/efficientnet_b0.onnx"
model = ie.read_model(model=model_onnx_path)
compiled_model = ie.compile_model(model=model, device_name="CPU")

input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

# 이미지 전처리 함수
def preprocess_image_openvino(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)  # 배치 차원 추가 (N, H, W, C)
    return img

# OpenVINO 예측 함수
def predict_openvino(image_path):
    img = preprocess_image_openvino(image_path)
    predictions = compiled_model([img])
    predicted_class = np.argmax(predictions[output_layer], axis=-1)
    return class_names[predicted_class[0]]  # 예측된 클래스 이름 반환

# 테스트 이미지 예측
image_path = "/content/drive/MyDrive/dataset/test_image.jpg"  # 여기에 테스트할 이미지 경로를 입력하세요.
predicted_class = predict_openvino(image_path)
print(f"Predicted class: {predicted_class}")

# 모델 최적화를 위해 OpenVINO의 Model Optimizer 사용
!mo --input_model efficientnet_b0.onnx --output_dir /content/drive/MyDrive/efficientnet_model

# 출력 디렉토리의 파일 목록 확인
!ls /content/drive/MyDrive/efficientnet_model
