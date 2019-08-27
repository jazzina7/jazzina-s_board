from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jazzina

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('login.html')

@app.route('/register')
def page_register():
   return render_template('register.html')

@app.route('/posting')
def page_posting():
   return render_template('posting.html')

@app.route('/board')
def page_board():
   return render_template('board.html')




## API 역할을 하는 부분
@app.route('/reg', methods=['POST']) # 회원가입하는 페이지
def register():
   babys_id_receive = request.form['babys_id_give']
   mothers_name_receive = request.form['mothers_name_give']
   babys_name_receive = request.form['babys_name_give']
   password_receive = request.form['password_give']

   doc = {'babys_id':babys_id_receive,'mothers_name':mothers_name_receive,'babys_name':babys_name_receive, 'password':password_receive} # 받은 걸 딕셔너리로 만들고,

   db.users.insert_one(doc)

   return jsonify({'result':'success'})

@app.route('/login', methods=['POST']) # 로그인하는 페이지
def login():
   babys_id_receive = request.form['babys_id_give']
   password_receive = request.form['password_give']

   result = db.users.find_one({'babys_id':babys_id_receive,'password':password_receive})
   print(result)

   if result is not None:
      return jsonify({'result':'success'})
   else:
      return jsonify({'result':'fail'})


@app.route('/post', methods=['POST']) # 글 써서 올리는 페이지
def post():
   babys_id_receive = request.form['babys_id_give']
   password_receive = request.form['password_give']
   title_receive = request.form['title_give']
   content_receive = request.form['content_give']


   result = db.users.find_one({'babys_id': babys_id_receive, 'password': password_receive})
   postings = {'babys_id':babys_id_receive, 'title':title_receive, 'content':content_receive}

   if result is not None:
      db.lists.insert_one(postings)
      return jsonify({'result':'success'})
   else:
      return jsonify({'result':'fail'})


@app.route('/board', methods=['POST'])
def board():
   babys_id_receive = request.form['babys_id_give']
   password_receive = request.form['password_give']

   result = db.users.find_one({'babys_id': babys_id_receive, 'password': password_receive})

   if result is not None:
      posts = db.lists.find({'babys_id': babys_id_receive}, {'_id': 0})
      return jsonify({'result':'success', 'articles':list(posts)})
   else:
      return jsonify({'result':'fail'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)