from flask import Flask, request, jsonify, render_template
from apify_client import ApifyClient

app = Flask(__name__)

# Replace with your Apify API token
API_TOKEN = "apify_api_U8cKVZNAGyIx1voOeRQc6rXPUMYykL314LA8"
client = ApifyClient(API_TOKEN)

@app.route('/')
def home():
    # Render the HTML form for input
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    # รับข้อมูลจากฟอร์ม
    twitter_handles = request.form.getlist('twitterHandles')

    # ตรวจสอบว่ามีการป้อน Twitter handles
    if not twitter_handles:
        return jsonify({"error": "กรุณาระบุ Twitter handles อย่างน้อยหนึ่งชื่อ"}), 400

    # Prepare Actor input
    run_input = {
        "twitterHandles": twitter_handles,
        "maxItems": 10,  # กำหนดจำนวนโพสต์สูงสุดที่ต้องการดึง
        "tweetLanguage": "en",  # ตัวกรองภาษา
    }

    try:
        # เรียกใช้ Actor และรอให้เสร็จสิ้น
        run = client.actor("61RPP7dywgiy0JPD0").call(run_input=run_input)

        # ดึงผลลัพธ์จาก Dataset
        results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        # หากไม่พบผลลัพธ์
        if not results:
            return jsonify({"message": "ไม่พบผลลัพธ์"}), 404

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
