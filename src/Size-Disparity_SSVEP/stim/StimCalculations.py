'''
変換処理などの関数をまとめたプログラム
'''
import numpy as np
from scipy.signal import square

class StimCalculation:
    def __init__(
            self,
            framerate,
            moniSize_pix,
            moniSize_cm,
            eyeOffset_cm):
        
        self.framerate = int(framerate)                     # フレームレート（Hz）
        self.moniSize_pix = moniSize_pix                    # モニターの解像度（ピクセル単位）
        self.moniSize_cm = moniSize_cm                      # モニターのサイズ（cm単位）
        self.ratio_cm2pix = moniSize_pix[0] / moniSize_cm   # cm から ピクセルへの変換比率

        self.eyeOffset_cm = eyeOffset_cm                    # 目のオフセット（cm単位）
    
    # 角度（度）をラジアンに変換し、対応する距離（cm）を計算
    def deg2rad(self, d_deg):
        d_rad = np.radians(d_deg)
        d_cm = np.tan(d_rad/2) * 2 * self.eyeOffset_cm
        return d_cm
    
    # 角度（度）をピクセルに変換
    def deg2pix(self, d_deg):
        d_cm = self.deg2rad(d_deg)
        d_pix = self.ratio_cm2pix * d_cm
        return int(round(d_pix))

    # ピクセルを角度（度）に変換
    def pix2deg(self, d_pix):
        d_cm = d_pix / self.ratio_cm2pix
        d_deg = np.degrees(d_cm)
        return d_deg
    
    # 距離（cm）を角度（度）に変換
    def cm2deg(self, d_cm):
        d_rad = 2 * np.arctan(d_cm / (2 * self.eyeOffset_cm))
        d_deg = np.degrees(d_rad)
        return d_deg
    
    # 角度（分）を角度（度）に変換
    def arcmin2deg(self, arcmin):
        return arcmin / 60
    
    # 指定したリフレッシュレートでドットを更新するタイミングを計算
    def dotRefresh_timing(self, refresh_rate, time):
        return [1 if ii % (self.framerate / refresh_rate) == 0 else 0 for ii in range(time)]
    
    # 指定したフリッカー周波数で点滅するタイミングを計算
    def flicker_timing(self, flicker_freq, time):
        return square(2 * np.pi * flicker_freq * time)
    
    # 指定したディスクの半径、要素の半径、ドット密度に基づいてドット数を計算
    def calc_diskNdots(self, disk_radius, elem_radius, dot_density):
        disk_area = np.pi * disk_radius ** 2                            # ディスクの面積
        elem_area = np.pi * elem_radius ** 2                            # 要素の面積
        diskNdots = int(disk_area * (dot_density / 100) / elem_area)    # 必要なドット数
        return diskNdots

    # 周囲の領域におけるドット数を計算
    def clac_surroundNdots(self, surround_side_len, elem_radius, dot_density):
        elem_area = np.pi * elem_radius ** 2                            # 要素の面積
        surroundNdots = int((surround_side_len ** 2 * (dot_density / 100) / elem_area))  # 周囲領域のドット数
        if surroundNdots % 2 != 0:                                      # 偶数に調整
            surroundNdots += 1
        return surroundNdots
