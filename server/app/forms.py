from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField, FileField, TextAreaField,FormField, FieldList, Form
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign on')

#Used for instructors creating a user
class CreateStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    possible_roles = [('student', 'Student'), ('assistant', 'Lab Assistant')]
    role = SelectField('Role', choices=possible_roles)
    submit = SubmitField('Create user')

#Used for admins creating a user
class CreateUserForm(CreateStudentForm):
    possible_roles = [('student', 'Student'), ('assistant', 'Lab Assistant'), ('instructor', 'Instructor'), ('admin', 'Admin')]
    role = SelectField('Role', choices=possible_roles)

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class CreateCourseForm(FlaskForm):
    name = StringField('Course name', validators=[DataRequired()])
    instructor_name = StringField('Instructor name', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class AddStudentForm(FlaskForm):
    name = StringField('Add student by name')
    submitstudent = SubmitField('Add Student')

class AddStudentFileForm(FlaskForm):
    file = FileField('Add student from CSV file', validators=[DataRequired()])
    submitfile = SubmitField('Add students fom file')

class AddToGroupForm(FlaskForm):
    group = SelectField('Group', validators=[DataRequired()], coerce=int)
    student_to_add = SelectField('Add student', validators=[DataRequired()], coerce=int)
    submit_add_to_group = SubmitField('Add student to group')

    def __init__(self, groups, possible_students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group.choices = groups
        self.student_to_add.choices = possible_students

class CreateGroupForm(FlaskForm):
    name = StringField('Name of new group', validators=[DataRequired()])
    submit_create_group = SubmitField('Create new group')

class RemoveFromCourseForm(FlaskForm):
    students = SelectField('Remove', validators=[DataRequired()], coerce=int)
    submit_remove = SubmitField('Remove student from course')

    def __init__(self, students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.students.choices = students

class StudentAnswer(FlaskForm):
    students=TextAreaField ("Answer",validators=[DataRequired()])
    submit = SubmitField('Submit')

class StudentLab(FlaskForm):
    list_of_answers=FieldList(FormField(StudentAnswer),min_entries=1, max_entries=100)

    def populate_answers(self,question):
        self.list_of_answers.append(StudentAnswer(students=question))

class NewSessionForm(FlaskForm):
    name = StringField('Name of new session', validators=[DataRequired()])
    lab = SelectField('Lab', validators=[DataRequired()])
    submit_new_session = SubmitField('Create new session')

    def __init__(self, labs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lab.choices = labs