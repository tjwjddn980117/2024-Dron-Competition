1. data_checking_size.py
    내가 가지고있는 image 데이터들이 size가 어떻게 되는지 확인한다. 
    내가 가지고있는 image 데이터들의 size를 알아야 이후 data_crop을 할 때 기준을 잡아야하기 때문이다. 

2. data_crop.py
    내가 가지고 있는 image 데이터들을 각각 중심을 기준으로 crop한다. 

3. data_downsampling.py
    내가 가지고 있는 image 데이터들의 해상도를 낮춘다. 

4. data_re_file.py
    내 데이터셋을 train과 valid로 나눈다. 

0. data_argument.py
    만약 내 데이터가 부족하다면, data_argument.py를 통해 강제로 데이터의 갯수를 키운다. 