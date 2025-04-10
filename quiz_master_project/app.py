from flask import Flask
from models.db_setup import init_db
from controllers.auth import home, login, register, logout
from controllers.admin import (
    admin_dashboard, add_subject, edit_subject, delete_subject,
    view_chapters, add_chapter, edit_chapter, delete_chapter,
    view_quizzes, add_quiz, view_questions, add_question, delete_question,
    admin_summary
)
# Import all functions from the user controller
from controllers.user import (
    user_dashboard, user_view_subject, user_view_quiz, 
    start_quiz, submit_quiz, quiz_summary
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Auth routes
app.route('/')(home)
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/register', methods=['GET', 'POST'])(register)
app.route('/logout')(logout)

# Admin routes
app.route('/admin/dashboard')(admin_dashboard)
app.route('/admin/subject/add', methods=['GET', 'POST'])(add_subject)
app.route('/admin/subject/edit/<int:subject_id>', methods=['GET', 'POST'])(edit_subject)
app.route('/admin/subject/delete/<int:subject_id>')(delete_subject)
app.route('/admin/subject/<int:subject_id>/chapters')(view_chapters)
app.route('/admin/subject/<int:subject_id>/chapter/add', methods=['GET', 'POST'])(add_chapter)
app.route('/admin/chapter/edit/<int:chapter_id>', methods=['GET', 'POST'])(edit_chapter)
app.route('/admin/chapter/delete/<int:chapter_id>')(delete_chapter)
app.route('/admin/chapter/<int:chapter_id>/quizzes')(view_quizzes)
app.route('/admin/chapter/<int:chapter_id>/quiz/add', methods=['GET', 'POST'])(add_quiz)
app.route('/admin/quiz/<int:quiz_id>/questions')(view_questions)
app.route('/admin/quiz/<int:quiz_id>/question/add', methods=['GET', 'POST'])(add_question)
app.route('/admin/question/delete/<int:question_id>')(delete_question)
app.route('/admin/summary')(admin_summary)

# User routes
app.route('/user/dashboard')(user_dashboard)
app.route('/user/subject/<int:subject_id>')(user_view_subject)
app.route('/user/quiz/<int:quiz_id>')(user_view_quiz)
app.route('/user/quiz/<int:quiz_id>/take')(start_quiz)
app.route('/user/quiz/<int:quiz_id>/submit', methods=['POST'])(submit_quiz)
app.add_url_rule('/user/summary', 'quiz_summary', quiz_summary)

if __name__ == '__main__':
    app.run(debug=True)
