from flask import render_template, redirect, url_for, flash, Markup, request, jsonify
from app import app, db, socketio
from app.models import User, Course, user_course, Group, user_group, Labs, Student_lab, Session
from app.forms import LoginForm, CreateUserForm, CreateStudentForm, EmptyForm, CreateCourseForm, AddStudentForm, AddStudentFileForm, AddToGroupForm, CreateGroupForm, RemoveFromCourseForm,StudentAnswer,StudentLab, NewSessionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.helpers.permission_levels import admin_required, instructor_required
from app.helpers.permission_levels import login_req
from app.helpers.process_csv import read_csv
import json
from collections import namedtuple
from flask_socketio import emit, join_room
from datetime import datetime, timedelta
import jwt
from functools import wraps

@app.route('/')
@login_required
def index():
    return render_template('base.html')

@app.route('/test/<int:session_id>')
def test(session_id):
    greeting = 'Rendering from Flask'
    return render_template('test.html', greeting=greeting, session_id=session_id)

@app.route('/login', methods=['POST'])
def login():
    data = {}
    '''if current_user.is_authenticated:
        logout_url = url_for('logout')
        data['alerts'] = (f'Already logged in as {current_user.name}. Try <a href="{logout_url}">logout</a> to log out.')
        #return redirect(url_for('index'))'''
    #form = LoginForm()*/
    if request.method == "POST":
        print("we got a post!")
        post_data = request.get_json()
        user = User.authenticate(**post_data)
        print(user)
        #user = User.query.filter_by(email=post_data.get("email")).first()
        if user is None:
            data['alerts'] = f'{post_data.get("email")} was not found in the database. Try again!'
            return jsonify(data), 401
            #return redirect(url_for('login'))
        else:
            token = jwt.encode({
                'sub': user.email,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=120)},
                app.config['SECRET_KEY']
            )
            print(token)
            data['alerts'] = f'{post_data.get("email")}, You are now logged in!'
            data['token'] = token
            return jsonify(data)
        #return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/userlist/<int:user_id>',methods=['PUT','DELETE'])
def user(user_id):
    data={'status': 'success'}
    print("Reached server")
    if request.method == 'PUT':
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            post_data = request.get_json()
            user.name = post_data["name"]
            user.role = post_data["role"]
            db.session.add(user)
            db.session.commit()
            data['message'] = 'User updated!'
            response_object = {'status': 'success'}
    if request.method == 'DELETE':
        print("Has delete method")
        user = User.query.filter_by(id=user_id).first()
        print(user)
        db.session.delete(user)
        db.session.commit()
        data['message'] = 'User deleted!'
        response_object = {'status': 'success'}
    return jsonify(data)

@app.route('/userlist')
@login_req('admin')
def user_list(current_user):
    users = User.query.all()
    json_users = [user.serialize() for user in users]
    return jsonify(json_users) 


@app.route('/createuser', methods=["POST"])
@login_req('admin')
def createuser(current_user):
    data= request.get_json()
    email_exists = User.query.filter_by(email=data.get("email")).first()
    if email_exists:
        return{"status":"exists"}
    if data.get("name").strip() == "":
        return {"status":"noname"}
    if data.get("password").strip() == "":
        return {"status":"nopassword"}
    if data.get("email").strip() == "":
        return {"status":"noemail"}
    if data.get("role").strip() == "":
        return {"status":"norole"}
    
    new_user= User(data.get("name"),data.get("email"),data.get("role"), data.get("password"))
    db.session.add(new_user)
    db.session.commit()
    return{"status":"successful"}

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            flash('Student not found.')
            return redirect(url_for('index'))
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.name} has been deleted!')
    return redirect(url_for('index'))

@app.route('/getuserid')
@login_req()
def get_user_id(current_user):
    return {'role': current_user.role}

@app.route('/getcourse/instructor/<course_name>/<semester>/<int:section>')
@login_req('instructor')
def course_getter(current_user, course_name, semester, section):
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section).first()
    if course is None: 
        return {'status': 'failure'}
    if current_user.role == 'instructor' and current_user.id != course.instructor_id:
        return {'status': 'failure'}
    students = User.query.join(user_course).filter(user_course.c.course_id == course.id).order_by(User.name).all()
    instructor = User.query.get(course.course_instructor)
    json_users = [user.serialize() for user in students]
    sessions = Session.query.filter_by(course_id=course.id)
    json_sessions = [session.serialize() for session in sessions]
    labs = Labs.query.all()
    json_labs = [lab.serialize() for lab in labs]
    return {'status': 'success', 'name': course.course_name, 'instructor': instructor.name, 
            'members': json_users, 'sessions': json_sessions, 'labs': json_labs}

@app.route('/removefromcourse/<course_name>/<semester>/<int:section>', methods=['POST'])
@login_req('instructor')
def remove_from_course(current_user, course_name, semester, section):
    student_name = request.get_json().get('student_name')
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section).first()
    user = User.query.filter_by(name=student_name).first()
    if user is None or course is None:
        return {'status': 'failure'}
    db.session.execute(user_course.delete().where(user_course.c.user_id == user.id, user_course.c.course_id == course.id))
    db.session.commit()
    return {'status': 'success'}

@app.route('/addsession/<course_name>/<semester>/<int:section>', methods=['POST'])
@login_req('instructor')
def add_session_to_course(current_user, course_name, semester, section):
    session_name = request.get_json().get('name')
    lab_name = request.get_json().get('lab')
    lab = Labs.query.filter_by(title=lab_name).first()
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section).first()
    if lab is None or course is None:
        return {'status': 'failure'}
    sessionExists = Session.query.filter_by(course_id=course.id, name=session_name).first()
    if sessionExists is not None:
        return {'status': 'failure'}
    session = Session(lab_id=lab.lab_id, course_id=course.id, name = session_name)
    db.session.add(session)
    db.session.commit()
    return {'status': 'success'}

@app.route('/addfromfile/<course_name>/<semester>/<int:section>', methods=['POST'])
@login_req('instructor')
def add_from_file(current_user, course_name, semester, section):
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section).first()
    f = request.files['csv']
    try: 
        users = read_csv(f)
        course.users.extend(users)
        db.session.add(course)
        db.session.commit()
    except Exception as e: 
        print(e)
        return {'status': 'failure'}
    return {'status': 'success'}

@app.route('/addfromname/<course_name>/<semester>/<int:section>', methods=['POST'])
@login_req('instructor')
def add_from_name(current_user, course_name, semester, section):
    new_student_name = request.get_json().get('student_name')
    user = User.query.filter_by(name=new_student_name).first()
    if user is None:
        return {'status': 'failure'}
    course = Course.query.filter_by(course_name=course_name).first()
    if course is None: 
        return {'status': 'failure'}
    course.users.extend([user])
    db.session.add(course)
    db.session.commit()
    return {'status': 'success'}

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course(course_id):
    current_user = User.query.get(1)
    course = Course.query.filter_by(id=course_id).first_or_404()
    instructor = User.query.get(course.course_instructor)
    students = User.query.join(user_course).filter(user_course.c.course_id == course_id).order_by(User.name).all()
    delete_form = EmptyForm() if current_user.role == 'admin' else None
    add_student_form = AddStudentForm() if current_user.role == 'admin' or current_user.role == 'instructor' else None
    add_file_form = AddStudentFileForm() if current_user.role == 'admin' or current_user.id == instructor.id else None
    student_removals = [(str(student.id), student.name) for student in students]
    remove_form = RemoveFromCourseForm(students=student_removals) if current_user.role == 'admin' or current_user.id == instructor.id else None
    labs = Labs.query.all()
    lab_choices = [(str(lab.lab_id), lab.title) for lab in labs]
    session_add_form = NewSessionForm(labs=lab_choices) if current_user.role == 'admin' or current_user.id == instructor.id else None
    sessions = Session.query.filter_by(course_id=course_id)

    if add_student_form and add_student_form.validate_on_submit() and add_student_form.submitstudent.data:
        user = User.query.filter_by(name=add_student_form.name.data).first()
        if user is None:
            create_user_url = url_for('create_user')
            flash(Markup(f'User not found! Try <a href="{create_user_url}">create user</a>'))
            return redirect(url_for('course', course_id=course_id))
        course.users.extend([user])
        db.session.add(course)
        db.session.commit()
        flash('User added to class!')
        redirect(url_for('course', course_id=course_id))

    if add_file_form and add_file_form.validate_on_submit() and add_file_form.submitfile.data:
        csv_file = request.files['file']
        users = read_csv(csv_file)
        course.users.extend(users)
        db.session.add(course)
        db.session.commit()
        flash('All students from file have been created and added to class')
        return redirect(url_for('course', course_id=course_id))

    if remove_form and remove_form.validate_on_submit() and remove_form.submit_remove.data:
        user = User.query.get_or_404(remove_form.students.data)
        db.session.execute(user_course.delete().where(user_course.c.user_id == user.id, user_course.c.course_id == course.id))
        db.session.commit()
        flash(f'{user.name} has been removed from the course.')
        return redirect(url_for('course', course_id=course_id))

    if session_add_form and session_add_form.validate_on_submit() and session_add_form.submit_new_session.data:
        sesh = Session.query.filter_by(course_id=course_id, name=session_add_form.name.data).first()
        if sesh is not None:
            flash('Session with given name already exists!')
            return redirect(url_for('course', course_id=course_id))
        lab = Labs.query.get_or_404(session_add_form.lab.data)
        sesh = Session(course_id=course_id, lab_id=lab.lab_id, name=session_add_form.name.data)
        db.session.add(sesh)
        db.session.commit()
        flash('New session added')
        return redirect(url_for('course', course_id=course_id))

    return render_template('course.html', course=course, delete_form=delete_form, instructor=instructor, remove_form=remove_form,
                             students=students, add_student_form=add_student_form, add_file_form=add_file_form, sessions=sessions, session_add_form=session_add_form)

@app.route('/course_list')
@login_req('admin')
def course_list(current_user):
    print('alright')
    courses = Course.query.all()
    json_users = [course.serialize() for course in courses]
    print(json_users)
    return jsonify(json_users)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        instructor = User.query.filter_by(name=form.instructor_name.data).first()
        if instructor is None:
            flash('Instructor not found!')
            return redirect(url_for('create_course'))
        if instructor.role != 'admin' and instructor.role != 'instructor':
            flash('Instructor must have admin/instructor permissions!')
            return redirect(url_for('create_course'))
        new_course = Course(course_name=form.name.data, course_instructor=instructor.id)
        db.session.add(new_course)
        db.session.commit()
        flash('Course created!')
        return redirect(url_for('create_course'))
    return render_template('create_course.html', form=form)

@app.route('/newcourse/submit', methods=['POST'])
def newCourse():
    data = request.get_json()
    course_search = Course.query.filter_by(course_name=data.get('name'), semester=data.get('semester'), section_num=data.get('section')).first()
    if course_search is not None:
        return {'status': 'exists'}
    instructor_search = User.query.filter_by(name=data.get('instructor')).first()
    if instructor_search is None:
        return {'status': 'noprof'}
    if data.get('name').strip() == '':
        return {'status': 'noname'}
    if data.get('semester').strip() == '':
        return {'status': 'nosem'}
    if int(data.get('section')) < 1:
        return {'status': 'nosec'}
    newCourse = Course(course_name=data.get('name'), semester=data.get('semester'), section_num=data.get('section'), course_instructor=instructor_search.id)
    db.session.add(newCourse)
    db.session.commit()
    return {'status': 'success'}

@app.route('/newcourse/getinstructors')
def get_instructors():
    admins = User.query.filter_by(role='admin').all()
    instructors = User.query.filter_by(role='instructor').all()
    returners = admins + instructors
    json_returners = [instructor.serialize() for instructor in returners]
    return json_returners

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
@admin_required
def delete_course(course_id):
    form = EmptyForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id=course_id).first()
        if course is None:
            flash('Course not found.')
            return redirect(url_for('index'))
        db.session.delete(course)
        db.session.commit()
        flash(f'Course {course.course_name} has been deleted!')
    return redirect(url_for('index'))

@app.route('/course/<int:course_id>/<int:session_id>', methods=['GET', 'POST'])
def session(course_id, session_id):
    course = Course.query.get_or_404(course_id)
    session = Session.query.get_or_404(session_id)
    groups = Group.query.filter_by(session_id=session_id).order_by(Group.group_name).all()
    users = User.query.join(user_course).filter(user_course.c.course_id == course_id).order_by(User.name).all()
    user_choices = [(str(user.id), user.name) for user in users]
    group_choices = [(str(group.id), group.group_name) for group in groups]
    add_to_group_form = AddToGroupForm(possible_students=user_choices, groups=group_choices)
    new_group_form = CreateGroupForm()

    if add_to_group_form and add_to_group_form.validate_on_submit() and add_to_group_form.submit_add_to_group.data:
        group_add = Group.query.get_or_404(add_to_group_form.group.data)
        user_add = User.query.get_or_404(add_to_group_form.student_to_add.data)
        group_add.users.append(user_add)
        db.session.add(group_add)
        db.session.commit()
        flash(f'Added {user_add.name} to group {group_add.group_name}')
        return redirect(url_for('session', course_id=course_id, session_id=session_id))
    
    if new_group_form and new_group_form.validate_on_submit() and new_group_form.submit_create_group:
        new_group = Group(group_name=new_group_form.name.data, course_id=course_id, session_id=session_id)
        db.session.add(new_group)
        db.session.commit()
        flash(f'Created new group "{new_group.group_name}"')
        return redirect(url_for('session', course_id=course_id, session_id=session_id))
    
    return render_template('groups.html', course=course, session=session, groups=groups, add_to_group_form=add_to_group_form, new_group_form=new_group_form)

@app.route('/groups/<int:course_id>/<int:group_id>/remove/<int:user_id>', methods=['POST'])
@login_required
@instructor_required
def remove_from_group(course_id, group_id, user_id):
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)
    db.session.execute(user_group.delete().where(user_group.c.user_id == user.id, user_group.c.group_id == group.id))
    db.session.commit()
    flash(f'{user.name} has been removed from group {group.group_name}')
    return redirect(url_for('groups', course_id=course_id))

@app.route('/delete_group/<int:group_id>', methods=['POST'])
@login_required
@instructor_required
def delete_group(group_id):
    form = EmptyForm()
    if form.validate_on_submit():
        group = Group.query.get(group_id)
        if group is None:
            flash('Group not found')
            return redirect(url_for('index'))
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted.')
        return redirect(url_for('course', course_id=group.course_id))
    return redirect(url_for('index'))

@app.route('/mycourses')
@login_req()
def my_courses(current_user):
    courses_taught = Course.query.filter_by(course_instructor=current_user.id).order_by(Course.course_name).all()
    courses_in = Course.query.join(user_course).filter(user_course.c.user_id == current_user.id).order_by(Course.course_name).all()
    courses = courses_taught + courses_in
    json_courses = [course.serialize() for course in courses]
    return json_courses

@app.route('/labs/fetch/<course_name>/<semester>/<int:section_num>/<session>')
def lab_fetcher(course_name,semester,section_num,session):
    dict = []
    session_id=Session.query.filter_by(name=session).first().id
    groups = Group.query.filter_by(session_id=session_id)
    for group in groups:
        student_names = []
        students = User.query.join(user_group).filter(user_group.c.group_id == group.id).all()
        for student in students:
            student_names.append(student.name)
        dict.append({'name': group.group_name, 'members': student_names, 'group_id': group.id, 'handRaised': group.hand_raised, 'atCheckpoint': group.at_checkpoint, 'progress': group.progress, 'maxProgress': group.max_progress})
    return dict

@app.route("/<course_name>/<semester>/<int:section_num>/<session_name>/<group_num>",methods=['GET', 'POST'])
def student_view(course_name,session_name,group_num,semester,section_num):
    
   
    course=Course.query.filter_by(course_name=course_name,semester=semester,section_num=section_num).first_or_404().id
    session=Session.query.filter_by(course_id=course,name= session_name).first_or_404()
    lab_id=session.lab_id
    session_id=session.id
    lab=Labs.query.filter_by (lab_id=lab_id).first_or_404()
    # the file is beung read through a string (change to read from file)
    f=lab.questions
    """[
   
    
       
        
 "order_num": 1,
        "title": "What are the names of all the files in the repository you just cloned?",
        "type": "Question",
        "checkpoint": false
    },
    {
        "order_num": 2,
        "title": "What symbols are used to indicate that the REPL is ready for you to enter a statement?",
        "type": "Question",
        "checkpoint": false
    },
    {
        "order_num": 3,
        "title": "Draw a square",
        "type": "Exercise",
        "checkpoint": false
    },
    {
        "order_num": 4,
        "title": "What code did you write? Copy and paste that code for the answer to this question. Include only the Python code, not the “>>>” that indicates that you are in the REPL.",
        "type": "Question",
        "checkpoint": true
    },
    {
        "order_num": 5,
        "title": "What is the third oldest line of code in your Python REPL history? If the arrow keys arent working for you, put “Arrow Keys Dont Work :(” for your answer.",
        "type": "Question",
        "checkpoint": false
    }
    ]"""
    

    raw_results = json.loads(f)
    
    response_object = {"status":"success",
                       "questions": raw_results,
                       "progress":0,
                       "total_questions": (len(raw_results)), 
                       "answers":{}}
    if request.method == 'POST':
        post_data = request.get_json()
        now = datetime.now()
        
        student_lab=Student_lab(
            question_num= int(post_data.get("id")), 
            group_name=group_num, 
            submit_time=now,
            saved_answer=post_data.get("answer")[str(post_data.get("id"))],
            session_id=session_id)
        
        db.session.add(student_lab) 
        db.session.commit()
       
        group = Group.query.filter_by(group_name=group_num,session_id=session_id).first()
        if int(post_data.get("id")) > int(group.progress):
            group.progress = int(post_data.get("id"))
            db.session.add(group)
            db.session.commit()
            session_id = group.session_id
            socketio.emit('progress_update', (group_num, int(post_data.get("id"))), to=str(session_id))
    
    progress=Group.query.filter_by(group_name=group_num,session_id=session_id).first().progress
    response_object['progress']=progress

    answers=Student_lab.query.filter_by (group_name=group_num, session_id=session_id).all()
    for answer in answers:
        if response_object['answers'].get(answer.question_num)==None:
            response_object ['answers'][answer.question_num]={"answer":answer.saved_answer,"time": answer.submit_time}
        else:
            if answer.submit_time > response_object["answers"][answer.question_num]["time"]:
               response_object ['answers'][answer.question_num]={"answer":answer.saved_answer,"time": answer.submit_time}
    for i in range(1, len(raw_results)+1):
        if response_object["answers"].get(i)==None:
            response_object["answers"][i]= ""
        else:
            response_object["answers"][i]=response_object["answers"][i]["answer"]
    print(response_object["answers"])
    return jsonify(response_object)





@socketio.on('connect')
def connect_test():
    print("connected, I think")

@socketio.on('command_send')
def send_command(group_id, command):
    group = Group.query.get(group_id)
    session_id = group.session_id
    if command == "handup":
        group.hand_raised = True
    elif command == "handdown":
        group.hand_raised = False
    elif command == "checkon":
        group.at_checkpoint = True
    elif command == "checkoff":
        group.at_checkpoint = False
    db.session.add(group)
    db.session.commit()
    print(str(group_id))
    emit('command', (group_id, command), to=str(session_id))

@app.route("/<course_name>/<semester>/<int:section_num>/<session_name>/getgroups",methods=['GET'])
def get_groups(course_name, semester,section_num,session_name):
    course_id=Course.query.filter_by(course_name=course_name,semester=semester,section_num=section_num).first_or_404().id
    session=Session.query.filter_by(course_id=course_id,name=session_name).first_or_404()
    groups=Group.query.filter_by(session_id=session.id).all()
    dict=[]
    for group in groups:
        student_names=[]
        students=User.query.join(user_group).filter(user_group.c.group_id==group.id).all()
        for student in students:
            student_names.append(student.name)
        dict.append({"name":group.group_name,"members":student_names})
    sessions=Session.query.filter(Session.course_id== course_id, Session.name!= session.name).all()
    json_sessions=[s.serialize() for s in sessions]
    return {"groups":dict, "old_sessions":json_sessions}




@socketio.on('ping')
def get_ping():
    emit('flask_ping', broadcast=True)

@socketio.on('enter_room')
def enter_room(room_name):
    join_room(str(room_name))

@app.route('/pingtest/<int:group_id>')
def pingtest(group_id):
    session_id = Group.query.get(group_id).session_id
    return render_template('emit_test.html', group_id=group_id, session_id=session_id)

@app.route('/newlab/submit', methods=['POST'])
def newLab():
    data = request.get_json()
    l = Labs.query.filter_by(title=data.get('title')).first() 
    if l is not None or data.get('title') is None or data.get('questions') is None:
        print("name_exists")
        return {'status': 'name exists'}
    lab = Labs(title=data.get('title'), questions=json.dumps(data.get('questions')), num_questions=int(data.get('num_questions')))
    try:
        db.session.add(lab)
        db.session.commit()
        
    except Exception as e: 
        return {'status': 'failure'}
    return {'status': 'success'}

@app.route('/newlab/delete/<lab_name>', methods=['DELETE'])
def deleteLab(lab_name):
    data={'status': 'success'}
    if request.method == 'DELETE':
        print("Lab has deleted")
        lab = Labs.query.filter_by(title=lab_name).first()
        print(lab)
        db.session.delete(lab)
        db.session.commit()
        data['message'] = 'Lab deleted!'
    return jsonify(data)
    
