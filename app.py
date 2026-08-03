import os
import time  # 処理時間計測用
import urllib.request
import cv2
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}

DENOISE_LEVELS = {
    'none': 0,
    'low': 3,
    'medium': 7,
    'high': 10,
    'max': 15,
}

DENOISE_LABELS = {
    'none': 'なし',
    'low': '低',
    'medium': '中',
    'high': '高',
    'max': '最高',
}


def get_model_path(scale):
    model_filename = f"ESPCN_x{scale}.pb"
    if not os.path.exists(model_filename):
        print(f"モデルファイル（{model_filename}）をダウンロード中...")
        url = f"https://raw.githubusercontent.com/fannymonori/TF-ESPCN/master/export/ESPCN_x{scale}.pb"
        urllib.request.urlretrieve(url, model_filename)
        print("ダウンロード完了！")
    return model_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --- 処理時間の計測スタート ---
        start_time = time.time()

        file = request.files.get('image')
        scale_str = request.form.get('scale', '2')
        denoise_key = request.form.get('denoise', 'none')

        if not file or file.filename == '':
            return render_template(
                'index.html', error='画像ファイルを選択してください。'
            )

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return render_template(
                'index.html',
                error='対応していないファイル形式です。（.jpg, .png などの画像を選択してください）',
            )

        try:
            scale = int(scale_str)
            model_path = get_model_path(scale)
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            sr.readModel(model_path)
            sr.setModel("espcn", scale)

            upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(upload_path)

            img = cv2.imread(upload_path)

            if img is None:
                return render_template(
                    'index.html',
                    error='画像を正しく読み込めませんでした。別の画像をお試しください。',
                )

            orig_h, orig_w = img.shape[:2]

            # ノイズ除去処理
            denoise_strength = DENOISE_LEVELS.get(denoise_key, 0)
            if denoise_strength > 0:
                img = cv2.fastNlMeansDenoisingColored(
                    img,
                    None,
                    denoise_strength,
                    denoise_strength,
                    7,
                    21,
                )

            # 高画質化の実行
            result_img = sr.upsample(img)
            res_h, res_w = result_img.shape[:2]

            result_filename = f"result_x{scale}_{denoise_key}_" + file.filename
            result_path = os.path.join(RESULT_FOLDER, result_filename)
            cv2.imwrite(result_path, result_img)

            # ---  処理時間の計算（小数第2位で四捨五入） ---
            elapsed_time = round(time.time() - start_time, 2)

            return render_template(
                'index.html',
                original_img=upload_path,
                result_img=result_path,
                orig_size=f"{orig_w} x {orig_h}",
                res_size=f"{res_w} x {res_h}",
                scale=scale,
                denoise_label=DENOISE_LABELS.get(denoise_key, 'なし'),
                elapsed_time=elapsed_time,  # 画面に時間を渡す
            )

        except Exception as e:
            print(f"エラー発生: {e}")
            return render_template(
                'index.html',
                error='処理中にエラーが発生しました。時間を置いて再度お試しください。',
            )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)