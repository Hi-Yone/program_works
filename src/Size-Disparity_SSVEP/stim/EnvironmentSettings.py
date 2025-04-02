'''
実験環境の設定をまとめたプログラム
'''
from psychopy import core, monitors, visual, data, gui
import numpy as np

from stim import StimGenerator as stim_gene

screen_num = 0                                                                  # モニタ番号

# 座標単位の定義
units = 'deg'

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0., 0., 0.]
white = [1., 1., 1.]
gray = [0.5, 0.5, 0.5]

# モニタの定義
# MONITOR_SIZE_PIX = [1440, 900]                                                # モニタサイズ(x, y) [pixel] (MacOS)
MONITOR_SIZE_PIX = [1920, 1080]                                                 # モニタサイズ(x, y) [pixel] (Windows)
MONITOR_WIDTH_CM = 53                                                           # モニタの横幅
MONITOR_FRAMERATE = 120                                                         # モニタのフレームレート[Hz]

# ハプロスコープの定義
eye_mirror1_dist = 4                                                            # [cm]
mirror1_mirror2_dist = 11                                                       # [cm]
mirror2_display_dist = 52                                                       # [cm]

# 視距離に関する定義
DISTANCE_CM = eye_mirror1_dist+mirror1_mirror2_dist+mirror2_display_dist        # 視距離 [cm]
BOD = 6.3                                                                       # 人間の両眼の間隔 [cm] (BOD : binocular distance)
EYEPOS_IN_MONITOR = BOD/2 + mirror1_mirror2_dist - np.arctan(BOD/2/DISTANCE_CM) # モニタ上での目の位置 [cm]