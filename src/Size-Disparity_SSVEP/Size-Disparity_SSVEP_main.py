'''
大きさ-奥行きのSSVEP計測実験
'''
# ===================================
# ライブラリインポート
# ===================================
from psychopy import core, monitors, visual, data, gui
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np
import os
import datetime

# stimフォルダのクラスをインポート
from stim import StimGenerator as stgen
from stim import StimCalculations as stcalc
from stim import StimParameters as stprm
from stim import EnvironmentSettings as Envset
from stim import StimTexts as sttxt


# ===================================
# 実験情報
# ===================================
# 実験情報の保存
expInfo = {'participant' : ""}

# 被験者の情報入力GUI
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=None)
if dlg.OK == False:                                                             # GUIウインドウがキャンセルされたら実験をしない
    core.quit()

# 実験結果保存用のフォルダ作成
parcitipant_name = expInfo['participant']
if not os.path.isdir(f"{parcitipant_name}/"):
    os.mkdir(f"{parcitipant_name}/")

# 保存先のファイルパスを設定
filename = f"{parcitipant_name}/{parcitipant_name}.csv"

# 実験中のログファイル保存用のフォルダ作成
if not os.path.isdir("./log"):
    os.mkdir("./log")


# ===================================
# 実験用クラス呼び出し
# ===================================
# モニタの設定
moni = monitors.Monitor("")
moni.newCalib(
    calibName="test",                                                          # キャリブレーションの名前
    width=Envset.MONITOR_WIDTH_CM,                                             # モニタの横幅
    distance=Envset.DISTANCE_CM                                                # 視距離
)
moni.setSizePix(Envset.MONITOR_SIZE_PIX)                                       # モニタサイズ[pixel]

# 画面管理クラス
win = visual.Window(
    size = Envset.MONITOR_SIZE_PIX,                                             # モニタサイズ
    colorSpace = Envset.COLOR_SPACE,                                            # 色空間
    color = Envset.gray,                                                        # 背景色
    fullscr = True,                                                             # フルスクリーン化
    monitor = moni,                                                             # モニタ情報を設定
    screen = Envset.screen_num,                                                 # スクリーンを選択 (モニタが複数ある場合に，どのモニタに表示するか)
    allowStencil = True                                                         # Aperture刺激の呈示に用いる (OpenGL)
)

# キーボード入力クラス
keyboard_start = keyboard.Keyboard()                                            # 実験開始用
keyboard_default = keyboard.Keyboard()                                          # 実験中断用
keyboard_resp = keyboard.Keyboard()                                             # 被験者の応答の取得用
keyboard_break = keyboard.Keyboard()                                             # 休憩用
clock = core.Clock()                                                            # 時間管理クラス

# 計算処理のクラス
stim_calc = stcalc.StimCalculation(framerate=Envset.MONITOR_FRAMERATE, 
                                    moniSize_pix=Envset.MONITOR_SIZE_PIX, 
                                    moniSize_cm=Envset.MONITOR_WIDTH_CM, 
                                    eyeOffset_cm=Envset.DISTANCE_CM)

# 固視点の位置を計算
fpPos = np.array([stim_calc.cm2deg(Envset.EYEPOS_IN_MONITOR),0])                       # ハプロスコープを使った時、視線がモニタ上のどこに対応するか. 固視点の位置．
# 刺激作成クラス
stim_gene = stgen.StimGenerator(win, 
                                 units=Envset.units,
                                 fpPos=fpPos,
                                 colorSpace=Envset.COLOR_SPACE)

# テキスト(教示)を描画するクラス
stim_texts = sttxt.StimTexts(win, fpPos)


# ===================================
# 刺激パラメータの計算
# ===================================
time=np.linspace(0, stprm.present_time, int(Envset.MONITOR_FRAMERATE*stprm.present_time)) # 呈示時間分のフレームを用意
dot_refresh_timing = stim_calc.dotRefresh_timing(stprm.dot_refreshrate, len(time))        # DRDSをリフレッシュするタイミングの配列
flicker_timing = stim_calc.flicker_timing(stprm.flicker_freq, time)                       # フリッカー刺激のタイミングの配列(1:テスト視差, -1:ゼロ視差)
Nstim=len(time)


# ===================================
# 刺激作成
# ===================================
# 固視点
fp_L, fp_R = stim_gene.fixation_point(fillColor=Envset.white)

# フリッカー周波数確認用の刺激
flickerCheck_stim = visual.Circle(win, units='deg', pos=(-22,12), radius=0.5, fillColor=Envset.black, colorSpace=Envset.COLOR_SPACE)
fillColor = {-1:Envset.white, 1:Envset.black}

# 教示テキスト
text_resp_L = stim_texts.text_resp_L()
text_resp_R = stim_texts.text_resp_R()
text_start_withButton_L = stim_texts.text_start_withButton_L()
text_start_withButton_R = stim_texts.text_start_withButton_R()
text_start_withoutButton_L = stim_texts.text_start_withoutButton_L()
text_start_withoutButton_R = stim_texts.text_start_withoutButton_R()
text_continue_L = stim_texts.text_continue_L()
text_continue_R = stim_texts.text_continue_R()


# ===================================
# 実験条件の設定
# ===================================
frame_tolerance=0.01                                                    # sec, フレームの許容誤差
times = {
    'fixation' : [stprm.fixation_start_time, stprm.fixation_end_time],  # 固視点の呈示時間
    'text' : [stprm.text_start_time, stprm.text_end_time],              # 教示の呈示時間
    'stim' : [stprm.stim_start_time, stprm.stim_end_time],              # 刺激の呈示時間
    'resp' : [stprm.resp_start_time, stprm.resp_end_time],              # 応答時間
    'break' : [stprm.break_start_time, stprm.break_end_time]            # 休憩時間
}

# trial毎に変える条件
conditions = data.createFactorialTrialList({
    'disparity' : stprm.disparity_arr,
    'disk_radius' : stprm.disk_radius_arr,
})

# 実験条件の管理
trials = data.TrialHandler(
    conditions,                                                         # trial毎に変える条件
    nReps = stprm.N_repeat,                                             # １条件を何回繰り返すか
    method = stprm.stimOder                                             # ランダマイズの方法                                                                                    # ランダマイズの方法
)

# 総試行回数
Trial_N = len(stprm.disparity_arr) * len(stprm.disk_radius_arr)* stprm.N_repeat

print("======実験パラメータ======")
print(f"両眼視差 : {stprm.disparity_arr}")
print(f"刺激半径 : {stprm.disk_radius_arr}")
print(f"トライアル回数 : {Trial_N}回")


# =========================================================
# 実験のコンポーネント定義
# =========================================================
# スタート画面のコンポーネント
trialComponents_start = [text_start_withButton_L, text_start_withButton_R, 
                         text_start_withoutButton_L, text_start_withoutButton_R, 
                         text_continue_L, text_continue_R, keyboard_start]


# ===================================
# 実験開始
# ===================================
trial_cnt = 0   # 現在のトライアル回数
for trial in trials:
    # 本トライアルの刺激パラメータ
    disparity = trial['disparity']
    disk_radius = trial['disk_radius']
    print('===================================')
    print(f"trial:{trial_cnt}, 両眼視差:{disparity} [arcmin], 刺激半径:{disk_radius} [deg]")

    # ===================================
    # 実験刺激作成
    # ===================================
    # ドット数を計算
    diskNdots = stim_calc.calc_diskNdots(disk_radius, stprm.elem_radius, stprm.dot_density)
    surroundNdots = stim_calc.clac_surroundNdots(stprm.surround_side_len, stprm.elem_radius, stprm.dot_density)

    # 呈示する相関刺激の作成(左右眼の相関刺激を一つのクラスでまとめて作る)
    diskStim = visual.ElementArrayStim(win, units=Envset.units, nElements=int(diskNdots*2), sizes=stprm.elem_radius*2, colorSpace=Envset.COLOR_SPACE)
    
    # 背景の無相関刺激作成(左右眼の無相関刺激を一つのクラスでまとめて作る)
    surroundStim = visual.ElementArrayStim(win, units=Envset.units, nElements=int(surroundNdots*2), sizes=stprm.elem_radius*2, colorSpace=Envset.COLOR_SPACE)

    # ドットの座標格納用のリスト初期化
    disk_dotPos_arr=[None]*Nstim
    surround_dotPos_arr=[None]*Nstim
    # ドットの色格納用のリスト初期化
    disk_dotColor_arr=[None]*Nstim
    surround_dotColor_arr=[None]*Nstim
    
    # 刺激・背景・0視差ドットの座標値,色をNoneで初期化
    LeyeDisk_dotPos=None; ReyeDisk_dotPos=None  # パッチ刺激のドット座標値配列

    for ii in range(Nstim):
        # DRDSのリフレッシュタイミングが1の時，刺激を作成
        if dot_refresh_timing[ii] == 1:
            # ============
            # テスト視差のドット
            # ============
            if flicker_timing[ii]==1:
                # 相関ドットの座標リストを作成
                corr_dotPos = stim_gene.circlePatch(diskNdots, disk_radius)
                LeyeDisk_dotPos = np.copy(corr_dotPos) - (disparity/2, 0) -fpPos
                ReyeDisk_dotPos = np.copy(corr_dotPos) + (disparity/2, 0) +fpPos

                # 左右眼の相関ドットの座標リストを結合
                disk_dotPos_arr[ii] = np.concatenate([LeyeDisk_dotPos, ReyeDisk_dotPos], axis=0)

                # 今回計算したドット座標の結果をコピーしておく
                LeyeDisk_dotPos=np.copy(LeyeDisk_dotPos); ReyeDisk_dotPos=np.copy(ReyeDisk_dotPos)
            
            # ============
            # ゼロ視差のドット
            # ============
            else:
                # 相関ドットの座標リストを作成
                corr_dotPos = stim_gene.circlePatch(diskNdots, disk_radius)
                LeyeDisk_dotPos = np.copy(corr_dotPos)-fpPos
                ReyeDisk_dotPos = np.copy(corr_dotPos)+fpPos

                # 左右眼の相関ドットの座標リストを結合
                disk_dotPos_arr[ii] = np.concatenate([LeyeDisk_dotPos, ReyeDisk_dotPos], axis=0)

                # 今回計算したドット座標の結果をコピーしておく
                LeyeDisk_dotPos=np.copy(LeyeDisk_dotPos); ReyeDisk_dotPos=np.copy(ReyeDisk_dotPos)
            
            # 相関ドットの色を設定
            LeyeDisk_dotColor = np.array([Envset.white if ii%2 else Envset.black for ii in range(diskNdots)])
            ReyeDisk_dotColor = np.array([Envset.white if ii%2 else Envset.black for ii in range(diskNdots)])
            # 相関ドットの色のリストを結合
            disk_dotColor_arr[ii] = np.concatenate([LeyeDisk_dotColor, ReyeDisk_dotColor], axis=0)
            
            # ============
            # 背景の無相関ドット
            # ============
            # 無相関ドットの座標リストを作成
            LeyeSurround_dotPos = np.random.uniform(-stprm.surround_side_len/2, stprm.surround_side_len/2, (surroundNdots, 2)) -fpPos
            ReyeSurround_dotPos = np.random.uniform(-stprm.surround_side_len/2, stprm.surround_side_len/2, (surroundNdots, 2)) +fpPos
            
            # 左右眼の背景の無相関ドットの座標リストを結合
            surround_dotPos_arr[ii] = np.concatenate([LeyeSurround_dotPos, ReyeSurround_dotPos], axis=0)

            # パッチの範囲内はグレーにする(sqrt((x-a)^2 + (y-b)^2)なので，disparityの正負は反対になる)
            LeyeDisk_area = (np.sqrt(np.sum((LeyeSurround_dotPos +fpPos + (disparity/2,0))**2, axis=1)) <= disk_radius)
            ReyeDisk_area = (np.sqrt(np.sum((ReyeSurround_dotPos -fpPos - (disparity/2,0))**2, axis=1)) <= disk_radius)

            # 無相関ドットの色を設定
            LeyeSurroundColor = np.array([Envset.white if ii%2 else Envset.black for ii in range(len(LeyeDisk_area))])
            ReyeSurroundColor = np.array([Envset.white if ii%2 else Envset.black for ii in range(len(ReyeDisk_area))])
            LeyeSurroundColor[LeyeDisk_area] = Envset.gray
            ReyeSurroundColor[ReyeDisk_area] = Envset.gray

            # 左右眼の無相関ドットの色のリストを結合
            surround_dotColor_arr[ii] = np.concatenate([LeyeSurroundColor, ReyeSurroundColor], axis=0)

            # 今回計算したドット座標・色の結果をコピーしておく
            LeyeSurround_dotPos=np.copy(LeyeSurround_dotPos); ReyeSurround_dotPos=np.copy(ReyeSurround_dotPos)
            LeyeSurroundColor=np.copy(LeyeSurroundColor); ReyeSurroundColor=np.copy(ReyeSurroundColor)
            
        # DRDSのリフレッシュタイミングが0なら，同じ刺激を使用
        else:
            # 相関ドットの座標リストを結合
            disk_dotPos_arr[ii] = np.concatenate([LeyeDisk_dotPos, ReyeDisk_dotPos], axis=0)
            # 相関ドットの色のリストを結合
            disk_dotColor_arr[ii] = np.concatenate([LeyeDisk_dotColor, ReyeDisk_dotColor], axis=0)

            # コピーした背景の無相関ドットの座標リストを結合
            surround_dotPos_arr[ii] = np.concatenate([LeyeSurround_dotPos, ReyeSurround_dotPos], axis=0)
            # コピーした背景の無相関ドットの色のリストを結合
            surround_dotColor_arr[ii] = np.concatenate([LeyeSurroundColor, ReyeSurroundColor], axis=0)
                
    # 刺激呈示のtrialに使うコンポーネントを定義
    trialComponents_present = [fp_L, fp_R, 
                               diskStim, 
                               surroundStim,
                               text_resp_L, text_resp_R, keyboard_resp,
                               flickerCheck_stim]
    

    # ======================================================================
    # スタート画面
    # ======================================================================
    # 休憩のトライアルの時はキーボードでスタート
    if trial_cnt%stprm.break_timing==0:
        # コンポーネントの状態を初期化
        startRoutine = True                                                                                         # trial中はTrue
        keyboard_default.keys = None                                                                                # キーボード応答を初期化
        keyboard_start.keys = None                                                                                  # キーボード応答を初期化

        # 各コンポーネントのステータスをリセット
        for thisComponent_start in trialComponents_start:
            if hasattr(thisComponent_start, 'status'):
                thisComponent_start.status = NOT_STARTED                                                            # ステータスのリセット
        
        # タイマーリセット
        time_first_frame = win.getFutureFlipTime(clock="now")                                                       # 次の画面フリップまでにかかる時間
        clock.reset(-time_first_frame)                                                                              # 次に画面フリップしたときに時間が0になるように設定

        # ====== トライアル開始 ======
        while startRoutine:
            t_flip = win.getFutureFlipTime(clock=clock)                                                             # 次にflipが行われる時刻(trial内)

            # テキストの開始時間を過ぎるとき
            if text_start_withButton_L.status == NOT_STARTED and t_flip >= times['text'][0] - frame_tolerance:
                text_start_withButton_L.setAutoDraw(True)                                                           # text_start_withButton_Lの描画開始
                text_start_withButton_R.setAutoDraw(True)                                                           # text_start_withButton_Rの描画開始

                text_continue_L.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt, trial=trial_cnt+1)            # 描画する文字を設定
                text_continue_R.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt, trial=trial_cnt+1)            # 描画する文字を設定
                text_continue_L.setAutoDraw(True)                                                                   # text_continue_Lの描画
                text_continue_R.setAutoDraw(True)                                                                   # text_continue_Rの描画
                fp_L.setAutoDraw(True)                                                                              # fp_Lの描画
                fp_R.setAutoDraw(True)                                                                              # fp_Rの描画

            waitOnFlip = False

            # キーボード入力の開始時間を過ぎるとき
            if keyboard_start.status == NOT_STARTED and t_flip >= times['text'][0] - frame_tolerance:
                keyboard_start.status = STARTED                                                                     # keyboard_startのキーを受け付けるようにする
                waitOnFlip = True

                win.callOnFlip(keyboard_start.clock.reset)                                                          # 次のフリップで時間をリセット
                win.callOnFlip(keyboard_start.clearEvents, eventType='keyboard')                                    # 次のフリップでキーボードのイベントをリセット
                
            # キーボード入力が既に始まった
            if keyboard_start.status == STARTED and not waitOnFlip:
                # キーボード入力を取得 (keyList中のキーしか取得できない)
                all_key_resp_start = keyboard_start.getKeys(keyList=['space'], waitRelease=False)

                # もし何かしら入力されたら
                if len(all_key_resp_start):
                    keyboard_start.keys = all_key_resp_start[-1].name                                               # 押されたキーの名前を取得
                    startRoutine = False                                                                            # trialの継続をFalseにする
                
            # エスケープが押されたら実験終了
            if keyboard_default.getKeys(keyList=["escape"]):
                core.quit()
                    
            if not startRoutine:
                # 今のtrialを終了
                # whileループを抜ける
                break
            else:
                # trialを継続
                # 画面をフリップさせて次フレームへ
                win.flip()

        # テキストの描画を辞める        
        text_start_withButton_L.setAutoDraw(False)
        text_start_withButton_R.setAutoDraw(False)
        text_continue_L.setAutoDraw(False)
        text_continue_R.setAutoDraw(False)

    else:
        # コンポーネントの状態を初期化
        startRoutine = True                                                                                         # trial中はTrue

        # 各コンポーネントのステータスをリセット
        for thisComponent_start in trialComponents_start:
            if hasattr(thisComponent_start, 'status'):
                thisComponent_start.status = NOT_STARTED                                                            # ステータスのリセット
        
        # タイマーリセット
        time_first_frame = win.getFutureFlipTime(clock="now")                                                       # 次の画面フリップまでにかかる時間
        clock.reset(-time_first_frame)                                                                              # 次に画面フリップしたときに時間が0になるように設定

        # ====== トライアル開始 ======
        while startRoutine:
            t_flip = win.getFutureFlipTime(clock=clock)                                                             # 次にflipが行われる時刻(trial内)

            # テキストの開始時間を過ぎるとき
            if text_start_withoutButton_L.status == NOT_STARTED and t_flip >= times['text'][0] - frame_tolerance:
                text_start_withoutButton_L.setAutoDraw(True)                                                        # text_start_withoutButton_Lの描画開始
                text_start_withoutButton_R.setAutoDraw(True)                                                        # text_start_withoutButton_Rの描画開始
        
                text_continue_L.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt, trial=trial_cnt+1)            # 描画する文字を設定
                text_continue_R.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt, trial=trial_cnt+1)            # 描画する文字を設定
                text_continue_L.setAutoDraw(True)                                                                   # text_continue_Lの描画
                text_continue_R.setAutoDraw(True)                                                                   # text_continue_Rの描画
                fp_L.setAutoDraw(True)                                                                              # fp_Lの描画
                fp_R.setAutoDraw(True)                                                                              # fp_Rの描画

            waitOnFlip = False

            if t_flip >= times['text'][1] - frame_tolerance:
                startRoutine = False                                                                                # trialの継続をFalseにする
                
            # エスケープが押されたら実験終了
            if keyboard_default.getKeys(keyList=["escape"]):
                core.quit()
                    
            if startRoutine:
                # trial継続
                win.flip()
            else:
                # trial終了
                break

        # テキストの描画を辞める        
        text_start_withoutButton_L.setAutoDraw(False)
        text_start_withoutButton_R.setAutoDraw(False)
        text_continue_L.setAutoDraw(False)
        text_continue_R.setAutoDraw(False)


    # ======================================================================
    # 刺激呈示画面
    # ======================================================================
    # コンポーネントの状態を初期化
    presentRoutine = True                                                                       # trial中はTrue
    all_key_resp = None                                                                         # キーボード応答を初期化
    keyboard_default.keys = None                                                                # キーボード応答を初期化
    keyboard_resp.keys = None                                                                   # キーボード応答を初期化

    # 各コンポーネントのステータスをリセット
    for thisComponent_present in trialComponents_present:
        if hasattr(thisComponent_present, 'status'):
            thisComponent_present.status = NOT_STARTED
    
    # タイマーリセット
    time_first_frame = win.getFutureFlipTime(clock="now")                                       # 次の画面フリップまでにかかる時間
    clock.reset(-time_first_frame)                                                              # 次に画面フリップしたときに時間が0になるように設定
    
    i_frame = -1                                                                                # 刺激呈示中のフレーム番号
    i_pos=0                                                                                     # 刺激のインデックス
    # ====== トライアル開始 ======
    while presentRoutine:
        i_frame += 1                                                                            # 現在のフレーム
        t_flip = win.getFutureFlipTime(clock=clock)                                             # 次にflipが行われる時刻(trial内)

        # Dynamic random dot stereogramの呈示
        if (diskStim.status==NOT_STARTED) and (t_flip >= times['stim'][0]):
            diskStim.status = STARTED                                                           # 相関刺激の呈示開始
            surroundStim.status = STARTED                                                       # 無相関刺激の呈示開始

            flickerCheck_stim.status = STARTED                                                  # フリッカー周波数確認用刺激の呈示開始
        
            diskStim.frameNStart = i_frame                                                      # 呈示開始時のフレームを保存
            surroundStim.frameNStart = i_frame

            diskStim.setXYs(disk_dotPos_arr[i_pos])                                             # 刺激の座標を設定
            diskStim.colors=disk_dotColor_arr[i_pos]                                            # 背景ドットの色を設定
            diskStim.draw(win)                                                                  # 刺激を描画

            surroundStim.setXYs(surround_dotPos_arr[i_pos])                                     # 背景ドットの座標を設定
            surroundStim.colors=surround_dotColor_arr[i_pos]                                    # 背景ドットの色を設定
            
            surroundStim.draw(win)
        
        # 刺激が呈示されているとき
        if diskStim.status == STARTED:
            if i_pos>=Nstim:    # 用意している刺激枚数を超えたら、インデックスを初期化
                i_pos=0
            diskStim.setXYs(disk_dotPos_arr[i_pos])                                             # 刺激の座標を設定
            diskStim.colors=disk_dotColor_arr[i_pos]                                            # 背景ドットの色を設定
            diskStim.draw(win)                                                                  # 刺激を描画

            surroundStim.setXYs(surround_dotPos_arr[i_pos])                                     # 背景ドットの座標を設定
            surroundStim.colors=surround_dotColor_arr[i_pos]                                    # 背景ドットの色を設定
            surroundStim.draw(win)                                                              # 刺激を描画
            
            flickerCheck_stim.fillColor=fillColor[flicker_timing[i_pos]]                        # 呈示周波数確認用刺激の色を設定
            flickerCheck_stim.draw(win)                                                         # 呈示周波数確認用刺激を描画
            i_pos += 1

            # 次のフリップで呈示終了時刻を過ぎるとき
            if (t_flip >= times['stim'][1]-frame_tolerance):
                print(i_pos, '/', Nstim)
                diskStim.status = FINISHED                                                      # 相関刺激の呈示終了
                surroundStim.status = FINISHED                                                  # 無相関刺激の呈示終了

                flickerCheck_stim.status = FINISHED                                             # 呈示周波数確認用刺激の呈示終了

                win.saveFrameIntervals(fileName=f"./log/frameIntervals_trial{trial_cnt}.log", clear=True)
                win.flip()

        # fixation pointの呈示
        if (fp_L.status==NOT_STARTED) and (t_flip >= times['fixation'][0]-frame_tolerance):
            fp_L.status = STARTED                                                               # 呈示開始
            fp_R.status = STARTED                                                               # 呈示開始 

            fp_L.frameNStart = i_frame                                                          # 呈示開始時のフレームを保存

            fp_L.draw(win)                                                                      # setAutoDrawがないので、毎回drawする
            fp_R.draw(win)                                                                      # setAutoDrawがないので、毎回drawする

        # 刺激が呈示されているとき
        if fp_L.status == STARTED:
            fp_L.draw(win)                                                                      # 固視点を描画
            fp_R.draw(win)                                                                      # 固視点を描画
        

    # ======================================================================
    # 応答画面
    # ======================================================================
        # 入力開始していない かつ 次のフリップで開始時刻を過ぎるとき
        if (keyboard_resp.status==NOT_STARTED) and (t_flip >= times['resp'][0]-frame_tolerance):
            keyboard_resp.status = STARTED                                                      # キーボードの状態を開始にする
            waitOnFlip = True

            win.callOnFlip(keyboard_resp.clearEvents, eventType='keyboard')                     # 次のフリップでキーボードのイベントをリセット
          
        # キーボード入力が既に始まった かつ フリップを待った後
        if (keyboard_resp.status==STARTED) and not waitOnFlip:
            # 何も入力されていないときは空のリストが返る
            all_key_resp = keyboard_resp.getKeys(keyList=['space'], waitRelease=False)          # キーボード入力を取得 (keyList中のキーのみ取得)
            text_resp_L.setAutoDraw(True)                                                       # text_resp_Lの描画
            text_resp_R.setAutoDraw(True)                                                       # text_resp_Rの描画

            # もし何かしら入力されたら
            if all_key_resp:
                keyboard_resp.keys = all_key_resp[-1].name                                      # 押されたキーの名前を取得
                print('応答 : ', keyboard_resp.keys)
                text_resp_L.setAutoDraw(False)                                                  # テキストの描画を辞める
                text_resp_R.setAutoDraw(False)                                                  # テキストの描画を辞める
                presentRoutine = False
                win.flip(clearBuffer=True)                                                      # ウィンドウを手動で更新して即座に次のトライアルに移る
        
        waitOnFlip = False
        
        # キー入力が何もなかったら、Noneにする
        if keyboard_resp.keys in ['', [], None]:
            keyboard_resp.keys = None
        
        # エスケープが押されたら実験終了
        if keyboard_default.getKeys(keyList=["escape"]):
            core.quit()
                
        if presentRoutine:
            # trial継続
            win.flip()
        else:
            # trial終了
            break
            
    trial_cnt+=1
    
    # 入力されたキーをデータに追加
    trials.addData('key', keyboard_resp.keys)                                                   

trials.saveAsWideText(fileName=filename)                                                        # 実験条件とレスポンスのデータをCSVファイルに保存

core.quit()                                                                                     # 実験終了