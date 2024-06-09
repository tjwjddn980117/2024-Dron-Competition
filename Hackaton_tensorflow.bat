rem you should change the root with your own environment path root.
rem and you could change the ENV_NAME with your one vitual environment.
set root=C:\Users\Seo\anaconda3
set ENV_NAME=Dron_tensorflow

if not exist "%root%" (
    echo check the root please: %root%
    pause
    exit
)

call %root%\Scripts\activate.bat %root%

echo make the virtual environment '%ENV_NAME%'
call conda create -y -n %ENV_NAME% python=3.10

echo enter the virtual environment.
call conda activate %ENV_NAME%

echo start downloading environment for %ENV_NAME%.
call conda install -y conda-forge::pandas conda-forge::tqdm conda-forge::matplotlib conda-forge::seaborn conda-forge::scikit-plot anaconda::scikit-learn
call pip install wandb
call pip install keras-models
call pip install keras-utils
call pip install Keras-Applications
call pip install tensorflow-2.13.0
call pip install numpy
call pip install opencv-python
call pip install pydot
call pip install plotly
call pip install graphviz

call conda deactivate

echo complete. 