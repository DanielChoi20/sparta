from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분  reviews -> orders
@app.route('/orderform', methods=['POST'])
def write_order():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']
    
    order = {
       'name': name_receive,
       'address': address_receive,
       'phone': phone_receive
    }
    # reviews에 review 저장하기
    db.orderform.insert_one(order)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': 'Order confirmed.'})

@app.route('/orderform', methods=['GET'])
def read_orders():
    orders = list(db.orderform.find({},{'_id':0}))
    return jsonify({'result': 'success', 'orderList': orders})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)