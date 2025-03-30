from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models.db_setup import db, Subject, Chapter, Quiz, Question, User, Score
from sqlalchemy import func

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

def edit_chapter(chapter_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        
        db.session.commit()
        
        flash('Chapter updated successfully')
        return redirect(url_for('view_chapters', subject_id=chapter.subject_id))
    
    return render_template('admin/chapter_form.html', chapter=chapter, subject=chapter.subject)

def delete_chapter(chapter_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    
    db.session.delete(chapter)
    db.session.commit()
    
    flash('Chapter deleted successfully')
    return redirect(url_for('view_chapters', subject_id=subject_id))

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

def delete_question(question_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    
    db.session.delete(question)
    db.session.commit()
    
    flash('Question deleted successfully')
    return redirect(url_for('view_questions', quiz_id=quiz_id))

def admin_summary():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    # Get all subjects
    subjects = Subject.query.all()
    summary_data = []
    
    for subject in subjects:
        subject_data = {
            'subject': subject,
            'top_scorers': [],
            'total_attempts': 0,
            'user_attempts': {}
        }
        
        # Get all quizzes for this subject through chapters
        quiz_ids = []
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                quiz_ids.append(quiz.id)
        
        if not quiz_ids:
            summary_data.append(subject_data)
            continue
        
        # Get top scorers for this subject
        top_scores = db.session.query(
            User.id,
            User.username,
            User.full_name,
            func.sum(Score.total_scored).label('total_score'),
            func.count(Score.id).label('attempts')
        ).join(Score).filter(
            Score.quiz_id.in_(quiz_ids)
        ).group_by(User.id).order_by(func.sum(Score.total_scored).desc()).limit(5).all()
        
        subject_data['top_scorers'] = top_scores
        
        # Get user attempt counts
        attempts = db.session.query(
            User.id,
            User.username,
            User.full_name,
            func.count(Score.id).label('attempts')
        ).join(Score).filter(
            Score.quiz_id.in_(quiz_ids)
        ).group_by(User.id).order_by(func.count(Score.id).desc()).all()
        
        for user_attempt in attempts:
            subject_data['user_attempts'][user_attempt.id] = {
                'username': user_attempt.username,
                'full_name': user_attempt.full_name,
                'attempts': user_attempt.attempts
            }
            subject_data['total_attempts'] += user_attempt.attempts
        
        summary_data.append(subject_data)
    
    return render_template('admin/summary.html', summary_data=summary_data)
