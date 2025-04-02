'''
刺激作成用の関数をまとめたプログラム
'''
from psychopy import visual
import numpy as np

class StimGenerator:
    def __init__(
            self,
            win,
            units,
            fpPos,
            colorSpace):
        self.win = win                  # PsychoPyのウィンドウオブジェクト
        self.units = units              # 単位設定（例: 'deg', 'cm', 'pix'）
        self.fpPos = fpPos              # 固視点の位置
        self.colorSpace = colorSpace    # 色空間の設定
        
    # 固視点（左目・右目用）を作成する関数
    def fixation_point(self, fillColor):
        fp_L = visual.ShapeStim(        # 左目に呈示する固視点の設定
            self.win,
            units=self.units,
            vertices=((-0.2, 0.05), (-0.2, -0.05), (-0.05, -0.05), (-0.05, -0.2), 
                      (0.05, -0.2), (0.05, 0.2), (-0.05, 0.2), (-0.05, 0.05)),
            fillColor=fillColor,
            colorSpace=self.colorSpace,
            lineColor=None,
            pos=-self.fpPos
        )

        fp_R = visual.ShapeStim(        # 右目に呈示する固視点の設定
            self.win,
            units=self.units,
            vertices=((0.2, 0.05), (0.2, -0.05), (0.05, -0.05), (0.05, -0.2), 
                      (-0.05, -0.2), (-0.05, 0.2), (0.05, 0.2), (0.05, 0.05)),
            fillColor=fillColor,
            colorSpace=self.colorSpace,
            lineColor=None,
            pos=self.fpPos
        )
        return fp_L, fp_R

    # 円形領域内にランダムにドットを配置する関数
    def circlePatch(self, Ndots, circle_radius):
        theta = np.random.uniform(0, 2 * np.pi, Ndots)  # 0から2πまでのランダムな角度
        rr = np.sqrt(np.random.uniform(0, circle_radius**2, Ndots))  # 半径方向のランダムな距離
        x = rr * np.cos(theta)          # x座標
        y = rr * np.sin(theta)          # y座標
        xy = np.column_stack((x, y))    # (x, y) のペアを作成
        return xy
