from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return 'This is hello world!'

@app.route('/mypage')
def mypage():
   return render_template('index.html')

## API 역할을 하는 부분
@app.route('/register', methods=['POST'])
def register():
   babys_id_receive = request.form['babys_id_give']          # 클라이언트로부터 url을 받는 부분
   mothers_name_receive = request.form['mothers_name_give']  # 클라이언트로부터 comment를 받는 부분
   babys_name_receive = request.form['babys_name_give']
   password_receive = request.form['password_give']

   doc = {'babys_id':babys_id_receive,'mothers_name':mothers_name_receive,'babys_name':babys_name_receive, 'password':password_receive} # 받은 걸 딕셔너리로 만들고,

   db.users.insert_one(doc)

   return jsonify({'result':'success'})

@app.route('/login', methods=['POST'])
def login():
   babys_id_receive = request.form['babys_id_give']          # 클라이언트로부터 url을 받는 부분
   password_receive = request.form['password_give']

   result = db.users.find_one({'babys_id':babys_id_receive,'password':password_receive})
   print(result)

   return jsonify({'result':'success'})


@app.route('/post', methods=['POST'])
def post():
   title_receive = request.form['title_give']          # 클라이언트로부터 url을 받는 부분
   comment_receive = request.form['comment_give']

   article = {'title':title_receive,'comment':comment_receive} # 받은 걸 딕셔너리로 만들고,
   db.articles.insert_one(article)

   return jsonify({'result':'success'})


@app.route('/board', methods=['GET'])
def board():
   posts = db.articles.find({}, {'_id': 0})
   return jsonify({'result':'success', 'articles':list(posts)})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)