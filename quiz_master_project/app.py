from flask import Flask
import os
from models.db_setup import init_db
from controllers import auth, admin, user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Authentication routes
app.route('/')(auth.home)
app.route('/login', methods=['GET', 'POST'])(auth.login)
app.route('/register', methods=['GET', 'POST'])(auth.register)
app.route('/logout')(auth.logout)

# Admin Routes
app.route('/admin/dashboard')(admin.admin_dashboard)
app.route('/admin/subject/new', methods=['GET', 'POST'])(admin.add_subject)
app.route('/admin/subject/<int:subject_id>/edit', methods=['GET', 'POST'])(admin.edit_subject)
app.route('/admin/subject/<int:subject_id>/delete')(admin.delete_subject)
app.route('/admin/subject/<int:subject_id>/chapters')(admin.view_chapters)
app.route('/admin/subject/<int:subject_id>/chapter/new', methods=['GET', 'POST'])(admin.add_chapter)
app.route('/admin/chapter/<int:chapter_id>/quizzes')(admin.view_quizzes)
app.route('/admin/chapter/<int:chapter_id>/quiz/new', methods=['GET', 'POST'])(admin.add_quiz)
app.route('/admin/quiz/<int:quiz_id>/questions')(admin.view_questions)
app.route('/admin/quiz/<int:quiz_id>/question/new', methods=['GET', 'POST'])(admin.add_question)

# User Routes
app.route('/user/dashboard')(user.user_dashboard)
app.route('/user/subject/<int:subject_id>')(user.user_view_subject)
app.route('/user/quiz/<int:quiz_id>')(user.user_view_quiz)
app.route('/user/quiz/<int:quiz_id>/start')(user.start_quiz)
app.route('/user/quiz/<int:quiz_id>/submit', methods=['POST'])(user.submit_quiz)

if __name__ == '__main__':
    app.run(debug=True)
