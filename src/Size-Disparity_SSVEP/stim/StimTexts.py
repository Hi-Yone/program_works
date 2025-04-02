'''
実験中の教示設定用プログラム
'''
from psychopy import visual
from stim import EnvironmentSettings as Envset

class StimTexts:
    def __init__(self, win, fpPos):
        self.win=win
        self.fpPos=fpPos

    # テキスト(教示)を描画するクラス
    def text_resp_L(self):
        return visual.TextStim(
            self.win,
            text = "Press       SPACE", # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = -self.fpPos                             # 呈示位置
        )

    def text_resp_R(self):
        return visual.TextStim(
            self.win,
            text = "Press       SPACE", # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = self.fpPos                              # 呈示位置
        )

    def text_start_withButton_L(self):
        return visual.TextStim(
            self.win,
            text = "Experiment session! \n Press 'Middle button' to START",          # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = -self.fpPos+(0, 1.5)                    # 呈示位置
        )

    def text_start_withButton_R(self):
        return visual.TextStim(
            self.win,
            text = "Experiment session! \n Press 'Middle button' to START",          # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = self.fpPos+(0, 1.5)                    # 呈示位置
        )

    def text_start_withoutButton_L(self):
        return visual.TextStim(
            self.win,
            text = "Experiment session!",          # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = -self.fpPos+(0, 1.5)                    # 呈示位置
        )

    def text_start_withoutButton_R(self):
        return visual.TextStim(
            self.win,
            text = "Experiment session!",          # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = self.fpPos+(0, 1.5)                    # 呈示位置
        )

    def text_continue_L(self):
        return visual.TextStim(
            self.win,
            text = " ",                                     # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = -self.fpPos+(0,-1.5)                    # 呈示位置
        )

    def text_continue_R(self):
        return visual.TextStim(
            self.win,
            text = " ",                                     # 描画する文字
            height = 1,                                     # 文字の大きさ
            color = Envset.white,                           # 文字の色
            units = 'deg',                                  # 単位
            colorSpace = Envset.COLOR_SPACE,                # 色空間
            pos = self.fpPos+(0,-1.5)                     # 呈示位置
        )