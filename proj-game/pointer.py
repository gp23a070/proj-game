import cv2
import numpy as np
import pyautogui

# カメラ設定
cap = cv2.VideoCapture(1)  # 必要に応じてデバイスIDを変更

# EMA係数（α）
alpha = 1.2  # 数値を小さくして滑らかさを増加

# 初期位置
predicted_x, predicted_y = None, None

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # フリップ（必要に応じてコメントアウト）
    # frame = cv2.flip(frame, 1)
    
    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # ノイズを低減するためにGaussian Blurを適用
    gray = cv2.GaussianBlur(gray, (1, 1), 0)
    
    # グレースケール画像の最大輝度位置を検出
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
    
    threshold = 200  # 輝度のしきい値（必要に応じて調整）
    if max_val > threshold:
        # 予測位置の初期化
        if predicted_x is None or predicted_y is None:
            predicted_x, predicted_y = max_loc
        
        # EMAによる位置予測
        previous_x, previous_y = predicted_x, predicted_y
        predicted_x = alpha * max_loc[0] + (1 - alpha) * predicted_x
        predicted_y = alpha * max_loc[1] + (1 - alpha) * predicted_y
        
        # 移動距離の制限（オプション）
        max_move = 50  # 最大移動ピクセル数
        delta_x = predicted_x - previous_x
        delta_y = predicted_y - previous_y
        distance = np.sqrt(delta_x**2 + delta_y**2)
        if distance > max_move:
            ratio = max_move / distance
            predicted_x = previous_x + delta_x * ratio
            predicted_y = previous_y + delta_y * ratio
        
        # スクリーン座標に変換
        screen_width, screen_height = pyautogui.size()
        mouse_x = int(predicted_x * screen_width / frame.shape[1])
        mouse_y = int(predicted_y * screen_height / frame.shape[0])
        
        # マウスを移動
        pyautogui.moveTo(mouse_x, mouse_y)
        
        # 最大輝度位置に円を描画
        cv2.circle(frame, (int(predicted_x), int(predicted_y)), 10, (0, 255, 0), 2)
    
    # 結果のフレームを表示
    cv2.imshow('Brightest Spot Detection with Prediction', frame)
    
    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()