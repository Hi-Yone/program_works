'''
刺激パラメータ設定用プログラム
'''
import numpy as np

# =========================================================
# 視覚刺激パラメータ定義
# =========================================================
elem_radius = 0.08                 # ドットサイズ [deg]
dot_density = 14                # ドット密度[%]
surround_side_len = 20               # 無相関パッチの描画範囲 [deg]

disk_radius_arr = [1.0, 2.0, 4.0, 6.0, 8.0] # 刺激の半径 [deg]
disparity_arr = [-0.7, -0.5, -0.3, -0.1, 0.5]   # 刺激の視差リスト[deg]

dot_refreshrate = 10            # DRDSのリフレッシュレート[Hz]
flicker_freq = 2                # フリッカー周波数[Hz]


# =========================================================
# 呈示パラメータ定義
# =========================================================
present_time = 6                         # 刺激呈示時間

fixation_start_time = 0.5                # 固視点呈示開始時刻
fixation_end_time = np.inf               # 固視点呈示終了時刻

text_start_time = fixation_start_time    # 教示呈示開始時刻(固視点呈示と同時)
text_end_time = 1.5                      # 教示呈示終了時刻

stim_start_time = 0.75                    # 教示呈示終了から何秒後に刺激呈示を開始するか(教示の後タイマーはリセット)
stim_end_time = stim_start_time+present_time  # 刺激呈示終了時刻

resp_start_time = stim_end_time+0.3      # 応答開始時刻
resp_end_time = np.inf                   # 応答終了時刻

break_start_time = fixation_start_time+1 # 休憩開始時刻
break_end_time = np.inf                  # 休憩終了時刻

# =========================================================
# 実験パラメータ定義
# =========================================================
break_timing = 15                       # 休憩のタイミング
N_repeat = 30                           # 1パラメータあたりの試行数
stimOder = 'random'                     # 刺激呈示順序
