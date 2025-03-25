from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models.db_setup import db, Subject, Chapter, Quiz, Question, User

def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    subjects = Subject.query.all()
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/dashboard.html', subjects=subjects, users=users)

# Subject CRUD operations
def add_subject():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        
        flash('Subject added successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/subject_form.html')

def edit_subject(subject_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        
        db.session.commit()
        
        flash('Subject updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/subject_form.html', subject=subject)

def delete_subject(subject_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    flash('Subject deleted successfully')
    return redirect(url_for('admin_dashboard'))

# Chapter CRUD operations
def view_chapters(subject_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    return render_template('admin/chapters.html', subject=subject)

def add_chapter(subject_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        
        flash('Chapter added successfully')
        return redirect(url_for('view_chapters', subject_id=subject_id))
    
    subject = Subject.query.get_or_404(subject_id)
    return render_template('admin/chapter_form.html', subject=subject)

# Quiz CRUD operations
def view_quizzes(chapter_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('admin/quizzes.html', chapter=chapter)

def add_quiz(chapter_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        time_duration = request.form['time_duration']
        remarks = request.form['remarks']
        
        new_quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(new_quiz)
        db.session.commit()
        
        flash('Quiz added successfully')
        return redirect(url_for('view_quizzes', chapter_id=chapter_id))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('admin/quiz_form.html', chapter=chapter)

# Question CRUD operations
def view_questions(quiz_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/questions.html', quiz=quiz)

def add_question(quiz_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = int(request.form['correct_option'])
        
        new_question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )
        db.session.add(new_question)
        db.session.commit()
        
        flash('Question added successfully')
        return redirect(url_for('view_questions', quiz_id=quiz_id))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/question_form.html', quiz=quiz)
