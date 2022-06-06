from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = ' postgres://nzirkofqgcflfy:51f8633797185637ca2919422ac08a1a6b7e283644e9ca8fc9e6263dd04b598e@ec2-52-206-182-219.compute-1.amazonaws.com:5432/d96at25t3pc96f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app=app)

class record_data(db.Model):
    srno = db.Column(db.Integer, primary_key = True)
    main_category = db.Column(db.String(100), nullable=False)
    sub_category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False) 


@app.route('/',methods=['GET','POST'])
def homepage():
    if request.method == 'GET':
        show_data = record_data.query.all()
        print(show_data)
        m_category = db.session.query(record_data.main_category).distinct()
        s_category = db.session.query(record_data.sub_category).distinct()
        main = m_category.all()
        print(main)
        return render_template('index.html', show_data=show_data, m_category=main, s_category=s_category)
    else:        
        main_category = request.form['mainCategory']
        sub_category = request.form['subCategory']
        description = request.form['desc']
    
        ins_data = record_data(main_category = main_category, sub_category = sub_category, description = description)
        if(main_category!='' and sub_category!='' and description!=''):
            db.session.add(ins_data)
            db.session. commit()
        show_data = record_data.query.all()
        m_category = db.session.query(record_data.main_category).distinct()
        s_category = db.session.query(record_data.sub_category).distinct()
        return render_template('/index.html', show_data=show_data, m_category=m_category, s_category=s_category)

@app.route('/update/<int:srno>', methods=['GET','POST'])
def update(srno):
    if request.method == 'POST':
        main_category = request.form['mainCategory']
        sub_category = request.form['subCategory']
        description = request.form['desc']
        update_data = record_data.query.filter_by(srno=srno).first()
        update_data.main_category = main_category
        update_data.sub_category = sub_category
        update_data.description = description
        db.session.add(update_data)
        db.session.commit()
        return redirect('/')
    else:
        retreive = record_data.query.filter_by(srno=srno).first()
        return render_template('update.html', data=retreive)

@app.route('/delete/<int:srno>')
def delete(srno):
    del_record = record_data.query.filter_by(srno=srno).first()
    db.session.delete(del_record)
    db.session.commit()
    return redirect('/')

@app.route('/search')
def search():
    return 'Search'


    #a = 'Welcome to Homepage'
    



if __name__ == '__main__':
    app.run(debug=True)