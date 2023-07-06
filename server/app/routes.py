from flask import render_template, redirect, url_for, flash, Markup, request, jsonify
from app import app, db, socketio
from app.models import User, Course, user_course, Group, user_group, Labs, Student_lab, Session
from app.forms import LoginForm, CreateUserForm, CreateStudentForm, EmptyForm, CreateCourseForm, AddStudentForm, AddStudentFileForm, AddToGroupForm, CreateGroupForm, RemoveFromCourseForm,StudentAnswer,StudentLab, NewSessionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.helpers.permission_levels import admin_required, instructor_required
from app.helpers.process_csv import read_csv
import json
from collections import namedtuple
from flask_socketio import emit, join_room
from datetime import datetime

@app.route('/')
@login_required
def index():
    return render_template('base.html')

@app.route('/test/<int:session_id>')
def test(session_id):
    greeting = 'Rendering from Flask'
    return render_template('test.html', greeting=greeting, session_id=session_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_url = url_for('logout')
        flash(Markup(
            f'Already logged in as {current_user.name}. Try <a href="{logout_url}">logout</a> to log out.'))
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(f'{form.email.data} was not found in the database. Try again!')
            return redirect(url_for('login'))
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<int:user_id>')
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = EmptyForm() if current_user.role == 'admin' else None
    return render_template('user.html', user=user, form=form)

@app.route('/user_list')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_user():
    form = CreateUserForm() if current_user.role == 'admin' else CreateStudentForm()
    if form.validate_on_submit():
        email_exists = User.query.filter_by(email=form.email.data).first()
        if email_exists:
            flash('Email already in use!')
            return redirect(url_for('create_user'))
        new_user = User(name=form.name.data, email=form.email.data, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User created!')
        return redirect(url_for('create_user'))
    return render_template('create_user.html', form=form)

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

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def course(course_id):
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
@login_required
@instructor_required
def course_list():
    courses = Course.query.all()
    return render_template('course_list.html', courses=courses)

@app.route('/create_course', methods=['GET', 'POST'])
@login_required
@instructor_required
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
@login_required
def session(course_id, session_id):
    course = Course.query.get_or_404(course_id)
    session = Session.query.get_or_404(session_id)
    groups = Group.query.filter_by(session_id=session_id).order_by(Group.group_name).all()
    users = User.query.join(user_course).filter(user_course.c.course_id == course_id).order_by(User.name).all()
    user_choices = [(str(user.id), user.name) for user in users]
    group_choices = [(str(group.id), group.group_name) for group in groups]
    add_to_group_form = AddToGroupForm(possible_students=user_choices, groups=group_choices
                        ) if current_user.role == 'admin' or current_user.id == course.course_instructor else None
    new_group_form = CreateGroupForm() if current_user.role == 'admin' or current_user.id == course.course_instructor else None

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

@app.route('/my_courses')
@login_required
def my_courses():
    user = current_user
    courses_taught = Course.query.filter_by(course_instructor=user.id).order_by(Course.course_name
                            ).all() if user.role == 'admin' or user.role == 'instructor' else None
    courses_in = Course.query.join(user_course).filter(user_course.c.user_id == user.id).order_by(Course.course_name).all()
    return render_template('my_courses.html', courses_taught=courses_taught, courses_in=courses_in, user=user)

@app.route('/labs/fetch/<int:session_id>')
def lab_fetcher(session_id):
    dict = []
    groups = Group.query.filter_by(session_id=session_id)
    for group in groups:
        student_names = []
        students = User.query.join(user_group).filter(user_group.c.group_id == group.id).all()
        for student in students:
            student_names.append(student.name)
        dict.append({'name': group.group_name, 'members': student_names, 'group_id': group.id})
    #response = jsonify(dict)
    return dict

@app.route("/<course_name>/<semester>/<int:section_num>/<int:lab_num>/<int:group_num>",methods=['GET', 'POST'])
def student_view(course_name,lab_num,group_num,semester,section_num):

    #lab=Labs.query.filter_by (lab_num=lab_num).first_or_404()
    course=Course.query.filter_by(course_name=course_name,semester=semester,section_num=section_num).first_or_404().id
    
    # the file is beung read through a string (change to read from file)
    f="""[
    {
        "order_num": 0,
        "title": "What are the names of all the files in the repository you just cloned?",
        "type": "Question",
        "checkpoint": false
    },
    {
        "order_num": 1,
        "title": "What symbols are used to indicate that the REPL is ready for you to enter a statement?",
        "type": "Question",
        "checkpoint": false
    },
    {
        "order_num": 2,
        "title": "Draw a square",
        "type": "Exercise",
        "checkpoint": false
    },
    {
        "order_num": 3,
        "title": "What code did you write? Copy and paste that code for the answer to this question. Include only the Python code, not the “>>>” that indicates that you are in the REPL.",
        "type": "Question",
        "checkpoint": true
    },
    {
        "order_num": 4,
        "title": "What is the third oldest line of code in your Python REPL history? If the arrow keys arent working for you, put “Arrow Keys Dont Work :(” for your answer.",
        "type": "Question",
        "checkpoint": false
    }
    ]"""
    raw_results = json.loads(f)
    response_object = {"status":"success","questions": raw_results}
    if request.method == 'POST':
        post_data = request.get_json()
        now = datetime.now()
        print(post_data.get("id"))
        student_lab=Student_lab( question_num= int(post_data.get("id")), group_name=group_num, submit_time=now,saved_answer=post_data.get("answer"),course_id=course)
        db.session.add(student_lab) 
        db.session.commit()
        response_object['message'] = 'Question saved!'
        print( "commit succesfull")

    return jsonify (response_object)





@socketio.on('connect')
def connect_test():
    print("connected, I think")

@socketio.on('command_send')
def send_command(group_id, command):
    session_id = Group.query.get(group_id).session_id
    print(str(group_id))
    emit('command', (group_id, command), to=str(session_id))

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

