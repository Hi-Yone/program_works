# 1. Size-Disparity SSVEP
大きさ-奥行きのSSVEP（定常状態視覚誘発電位）計測実験のPythonプログラム。

# 2. Stereo-VGG16 size discrimination
深層学習モデルに大きさ識別を学習させ、擬似心理物理実験を適用するPythonプログラム。

## プロジェクト構成
📂 src  
 ┣ 📂 Size-Disparity_SSVEP/       # 脳波計測実験のプログラムフォルダ  
 ┃ ┣ 📜 Size-Disparity_SSVEP_main.py  # 実験のメインスクリプト  
 ┃ ┣ 📜 StimGenerator.py              # 視覚刺激の生成  
 ┃ ┣ 📜 StimCalculations.py           # 刺激の計算  
 ┃ ┣ 📜 StimParameters.py             # 刺激のパラメータ管理  
 ┃ ┣ 📜 StimTexts.py                  # 刺激に関するテキストデータ  
 ┃ ┣ 📜 EnvironmentSettings.py         # 実験環境の設定  
 ┃ ┗ 📜 calculate_geometrical_size.ipynb # 幾何学的計算のノートブック  
 ┣ 📂 Stereo-VGG16 size discrimination/  
 &ensp;&ensp;&ensp;┣ 📜 vgg16_stereo_size-discrimination_sndl_stereo_gabor.ipynb  # 深層学習によるサイズ識別のプログラム  
