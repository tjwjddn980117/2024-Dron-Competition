2024 AI 드론 경진대회

 - Classification
 - Real-Time Object Detection

Classification에 대한 코드들:
 - 대회에서 제공한 base code는 'Classification_for_base_Colab'에 있음. 
 - 우리가 짜놓았던 다양한 코드들은 'Classification_for_our_Colab'에 있음.
   - Classification_for_our_Colab의 환경을 vscode같은 환경에서 구동할 경우 'Hackaton_pytorch.bat'/'Hackaton_pytorchLightning.bat'을 실행하거나 'Hackaton_pytorch.txt'에 환경을 설치하면 된다. 
 - 최종적으로 우리가 드론의 Real-Time Object Detection에 성공한 코드는 'AI_Hackaton_real_9.ipynb'과 'AI_Hackaton_real.ipynb'이다. 
  - 위 코드를 vscode같은 환경에서 구동할 경우 'Hackaton_tensorflow.bat'을 실행하거나 'Hackaton_tensorflow.txt'에 환경을 설치하면 된다.
  - AI_Hackaton_real_9.ipynb 코드는 '기존 클래스 8개'+'더미클래스 1개(Zerogroung)'로 9개의 클래스를 학습한다. 
  - AI_hackaton_real.ipynb 코드는 '기존 클래스 8개'로 8개의 클래스를 학습한다. 

Datas
 - 데이터는 3000*2250의 이미지를 사용하였다. 
  - AI_Hackaton_real_9.ipynb의 valid-score는 99.7 나왔다. 
 - data https://drive.google.com/file/d/12tUp9dFygg4sHht-Z0EpYpW7y3pNMc-i/view?usp=sharing
 - 데이터는 기존 클래스 8개('Bonobono', 'Eagle', 'Gmarket', 'Hp', 'Intel', 'Underwood', 'Wonju', 'Yonsei')와, 배경화면을 인식하는 클래스 1개('Zeroground')로 총 9개가 있다.

drone에 대한 코드들:
 - dron_control.py에 63 line을 self.CLASSIFICATION_CONF = 0.9 * 100로 하여 Classification의 민감도를 조정한다.
 - ObjectClassifier.py에 120, 121 line에서 더미 클래스를 추가한 것에 대해서 예외 처리해주는 코드를 추가하였다. 
