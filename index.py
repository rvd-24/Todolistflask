from flask import Flask,render_template,request,jsonify,redirect
from flask_mongoengine import MongoEngine
from decouple import config
import datetime

app=Flask(__name__)
password=config("password")
db_name="API"

DB_URI="mongodb+srv://admin:{}@flaskcon.3su2lne.mongodb.net/{}?retryWrites=true&w=majority".format(password,db_name)

db=MongoEngine()
db.connect(db=db_name,username="admin",password=config("password"),host=DB_URI)

class TaskList(db.Document):
    task_id=db.IntField()
    name=db.StringField()
    created_at=db.DateTimeField(default=datetime.datetime.now)

    def to_json(self):
        return{
            "task_id":self.task_id,
            "name":self.name,
            "created_at":self.created_at
        }


@app.route('/',methods=['GET','POST'])
def task_api():
    cnt=0
    if request.method=="GET":
        tasks=[]
        for task in TaskList.objects:
            tasks.append(task.to_json())
        return render_template('index.html',tasks=tasks)
    elif request.method=="POST":
        content=request.form['content']
        task_id=request.form['taskid']
        task=TaskList(task_id=task_id,name=content,created_at=datetime.datetime.now)
        task.save()
        return redirect('/')
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task_obj=TaskList.objects(task_id=task_id).first()
    task_obj.delete()
    return redirect('/')

@app.route('/update/<int:task_id>',methods=['POST','GET'])
def update(task_id):
    if request.method=='POST':
        content=request.form['content']
        task_obj=TaskList.objects(task_id=task_id).first()
        task_obj.update(name=content)
        return redirect('/')
    else:
        task_obj=TaskList.objects(task_id=task_id).first()
        return render_template('update.html',task=task_obj)

# if __name__=="__main__":
#     app.run(debug=True)