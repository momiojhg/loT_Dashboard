from flask import Flask, render_template, request, redirect, jsonify
import os
import price_prediction
import real_time_price_display
import time

app = Flask(__name__)

# 全局变量存储价格数据
price_data = {
    'stock_name': '',
    'current_price': 0,
    'future_price': 0,
    'update_time': ''
}

# API接口：获取实时价格数据
@app.route('/api/price_data')
def get_price_data():
    try:
        spider = real_time_price_display.GoldFuturesSpider()
        model = price_prediction.FuturesModel()
        
        name, current_price = spider.get_data()
        future_price = model.train_and_predict()
        
        price_data = {
            'stock_name': name,
            'current_price': current_price,
            'future_price': future_price,
            'update_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(price_data)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'update_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)