To run the POC model:
First time executing:
1 - Install conda package manager

2 - Create a virtual env with command:
conda create -n "virtual_env_name"

3 - Install dependecies with pip

If not the first time executing:

4 - Enter the virtual env:
conda activate "virtual_env_name"

In our case:
We have to go to the project directory and run:

conda activate tsr

5 - Install requirements:
pip install -r requirements.txt

6 - run the python script:
python poc_get_sign.py

TO TRAIN THE MODEL:
python model_train.py
