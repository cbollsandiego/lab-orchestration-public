from flask import request, jsonify
from app import app, db, socketio
from app.models import User, Course, user_course, Group, user_group, Labs, Student_lab, Session
from app.helpers.permission_levels import login_req
from app.helpers.process_csv import read_csv
import json
from flask_socketio import emit, join_room
from datetime import datetime, timedelta
import jwt

@app.route('/login', methods=['POST'])
def login():
    '''
    The login function for the application. 
    The user email and password must be sent from the frontend in a single object with 'username' and 'pass'
    This will return a JWT token to the frontend, which then is sent in all requests that require a login.
    '''
    data = {}
    if request.method == "POST":
        post_data = request.get_json()
        user = User.authenticate(**post_data)
        if user is None:
            data['alerts'] = f'{post_data.get("email")} was not found in the database. Try again!'
            return jsonify(data), 401
        else:
            token = jwt.encode({
                'sub': user.email,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=120)},
                app.config['SECRET_KEY']
            )
            data['alerts'] = f'{post_data.get("email")}, You are now logged in!'
            data['token'] = token
            return jsonify(data)

@app.route('/userlist/<int:user_id>',methods=['PUT','DELETE'])
def user(user_id):
    '''
    This route is used by the user list page, to update or delete users.
    The request must include an object with 'name' and 'role' data if it is a put request
    params:
        -user_id: id of user being deleted/edited (int)
    '''
    data={'status': 'success'}
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
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        data['message'] = 'User deleted!'
        response_object = {'status': 'success'}
    return jsonify(data)

@app.route('/userlist')
@login_req('admin')
def user_list(current_user):
    '''
    This returns all of the users in the database and is used by the User List page in the frontend.
    '''
    users = User.query.all()
    json_users = [user.serialize() for user in users]
    return jsonify(json_users) 


@app.route('/createuser', methods=["POST"])
@login_req('admin')
def createuser(current_user):
    '''
    This is used to add a new user to the database. Validaiton of all inputs is done in this function
    The request must come with info for the user 'email', 'name', 'password', and 'role'
    '''
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

@app.route('/getuserid')
@login_req()
def get_user_id(current_user):
    '''
    This returns the role of the logged in user.
    Must have an authentication key sent with the request, as the current_user is retreieved from this.
    '''
    return {'role': current_user.role}

@app.route('/getcourse/student/<course_name>/<semester>/<int:section>')
@login_req()
def course_getter_student(current_user, course_name, semester, section):
    '''
    This is used to get the information needed to render the Course page for students. It will return only information that
    is accessible to students, there is a seperate route for instructors to get all the information about a course.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section).first()
    if course is None: 
        return {'status': 'failure'}
    students = User.query.join(user_course).filter(user_course.c.course_id == course.id).order_by(User.name).all()
    if current_user not in students:
        return {'status': 'failure'}
    instructor = User.query.get(course.course_instructor)
    sessions = Session.query.filter_by(course_id=course.id)
    groups = []
    for session in sessions:
        g = Group.query.filter_by(session_id=session.id).first()
        if g is not None:
            groups.append({'session': session.name, 'group': g.group_name})
    return {'status': 'success', 'name': course.course_name, 'instructor': instructor.name, 
            'groups': groups}

@app.route('/getcourse/instructor/<course_name>/<semester>/<int:section>')
@login_req('instructor')
def course_getter(current_user, course_name, semester, section):
    '''
    This is the route used for an instructor to get all of the informaiton about a course. Unlike the student course view, this
    route will return more information about the course only visible to instrcutors, such as sessions and labs.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
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
    '''
    This is the route used to remove a student from a course. It is accessed from the instructor course page.
    The request must include a student_name element with the name of the student being removed.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
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
    '''
    This is used to add a new lab session to a specified course. It is accessed from the Instructor course page.
    The session must have a name and a lab passed in the request to properly be created
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
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
    '''
    This route is used in the Instructor course page to add a batch of students from a .csv file to the course.
    The .csv file must have the first value of each line be the student last name, the second value as the first name, and the 
    third value as their USD username(not including '@sandiego.edu'). This is the same format as generated in a course list
    by Blackboard.
    The file must be labeled as 'csv' and sent in the request
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
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
    '''
    This is used to add a student to a course from a given name. It is accessed from the Instructor course page.
    The request must include the student's name as student_name
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
    '''
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

@app.route('/course_list')
@login_req('admin')
def course_list(current_user):
    '''
    This is used to get all the information about all the courses in the database for the Course List page.
    '''
    courses = Course.query.all()
    json_courses = [course.serialize() for course in courses]
    return jsonify(json_courses)

@app.route('/newcourse/submit', methods=['POST'])
def newCourse():
    '''
    This is used to create a new course in the database. It is accessed from the Course Create page.
    All data about the course must be included in the request: name(str), semester(str), section(int), instructor(str)(instructor's name)
    '''
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
    '''
    This returns all instructor and admin users in the database.
    It is used by the Course Create page to provide the user a list of possible instructors for the course they are creating.
    '''
    admins = User.query.filter_by(role='admin').all()
    instructors = User.query.filter_by(role='instructor').all()
    returners = admins + instructors
    json_returners = [instructor.serialize() for instructor in returners]
    return json_returners

@app.route('/mycourses')
@login_req()
def my_courses(current_user):
    '''
    This route is used by instructors and students to get all of the information about the courses that they are registered in,
    or the courses that they are listed as the instructor for. It is used for the My Courses page
    '''
    courses_taught = Course.query.filter_by(course_instructor=current_user.id).order_by(Course.course_name).all()
    courses_in = Course.query.join(user_course).filter(user_course.c.user_id == current_user.id).order_by(Course.course_name).all()
    courses = courses_taught + courses_in
    json_courses = [course.serialize() for course in courses]
    return json_courses

@app.route('/labs/fetch/<course_name>/<semester>/<int:section_num>/<session>')
def lab_fetcher(course_name,semester,section_num,session):
    '''
    This is used to get all of the information about a lab session for the instructor of a course.
    All information about all groups of the lab session is returned. This is used in the Live view of a lab session for an instructor
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
        -session: session name (str)
    '''
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
    '''
    This is used to get all the information for a student about a lab.
    It retrieves all information about the lab questions and their saved respones, and returns it all.
    This is used in the Student Live lab view page.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section_num: section number (int)
        -session_name: session name (str)
        -group_num: group number (str)
    '''
    course=Course.query.filter_by(course_name=course_name,semester=semester,section_num=section_num).first_or_404().id
    session=Session.query.filter_by(course_id=course,name= session_name).first_or_404()
    lab_id=session.lab_id
    session_id=session.id
    lab=Labs.query.filter_by (lab_id=lab_id).first_or_404()
    f=lab.questions
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

@app.route("/<course_name>/<semester>/<int:section_num>/<session_name>/getgroups", methods=['GET'])
@login_req('instructor')
def get_groups(course_name, semester, section_num, session_name):
    '''
    This is used to get all the groups that are associated with a certain lab session.
    This is called from the Create Groups page, and sends all the groups that are in the database along with students that are 
    registered in the class, but not assigned to a group.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
        -session_name: session name (str)
    '''
    course_id = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section_num).first_or_404().id
    session = Session.query.filter_by(course_id=course_id,name=session_name).first_or_404()
    groups = Group.query.filter_by(session_id=session.id).all()
    all_student_names = [{'name': user.name, 'id': user.id} for user in User.query.join(user_course).filter(user_course.c.course_id==course_id).order_by(User.name).all()]
    dict = []
    for group in groups:
        student_names = []
        students = User.query.join(user_group).filter(user_group.c.group_id==group.id).all()
        for student in students:
            if {'name': student.name, 'id': student.id} in all_student_names: all_student_names.remove({'name': student.name, 'id': student.id})
            student_names.append({'name': student.name, 'id': student.id})
        dict.append({"name": group.group_name, "members": student_names})
    sessions = Session.query.filter(Session.course_id==course_id, Session.name!=session.name).all()
    json_sessions = [s.serialize() for s in sessions]
    return {"groups":dict, "old_sessions":json_sessions, "not_in_group": all_student_names}

@app.route("/<course_name>/<semester>/<int:section_num>/<session_name>/postgroups", methods=['POST'])
@login_req('instructor')
def post_groups(course_name, semester,section_num,session_name):
    '''
    This is used to save the groups that have been made in the Create Groups page.
    When the instructor presses 'save groups', all the groups and users in each group are sent to this route, where they are all
    created and saved in the database.
    params:
        -course_name: course name (str)
        -semester: semester (str)
        -section: section number (int)
        -session_name: session name (str)
    '''
    data = request.get_json()
    course = Course.query.filter_by(course_name=course_name, semester=semester, section_num=section_num).first()
    session = Session.query.filter_by(course_id=course.id,name=session_name).first()
    lab = Labs.query.get(session.lab_id)
    try:
        db.session.query(Group).filter(Group.session_id==session.id).delete()
        db.session.commit()
        for group in data.get('groups'): 
            newGroup = Group(group_name=group.get('name'), course_id=course.id, session_id=session.id, max_progress=lab.num_questions)
            db.session.add(newGroup)
            print(group.get('members'))
            for member in group.get('members'):
                user = User.query.filter_by(name=member.get('name')).first()
                newGroup.users.append(user)
                db.session.add(newGroup)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'status': 'failure'}
    return {'status': 'success'}

@app.route('/newlab/submit', methods=['POST'])
def newLab():
    '''
    This creates a new Lab and adds it to the database. It is used by the Create Lab page to submit the info put in there
    into the database.
    '''
    data = request.get_json()
    l = Labs.query.filter_by(title=data.get('title')).first()
    if l is not None or data.get('title') is None or data.get('questions') is None:
        return {'status': 'name exists'}
    lab = Labs(title=data.get('title'), questions=json.dumps(data.get('questions')), num_questions=int(data.get('num_questions')))
    try:
        db.session.add(lab)
        db.session.commit()
        
    except Exception as e: 
        return {'status': 'failure'}
    return {'status': 'success'}

@socketio.on('enter_room')
def enter_room(room_name):
    '''
    This is used for a user to join a room, which is used for sending and receiving signals via socket.io
    '''
    join_room(str(room_name))

@socketio.on('command_send')
def send_command(group_id, command):
    '''
    This is used to emit a signal that a group has raised their hand or reached a checkpoint.
    The signal is typically sent from the student live lab view and recieved in the instructor live lab view.
    '''
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
    emit('command', (group_id, command), to=str(session_id))