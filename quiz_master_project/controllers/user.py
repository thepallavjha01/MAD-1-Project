from flask import render_template, request, redirect, url_for, session, flash
from models.db_setup import db, User, Subject, Quiz, Question, Score
from sqlalchemy import func

def user_dashboard():
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get all completed quizzes
    completed_quizzes = Score.query.filter_by(user_id=user_id).all()
    
    subjects = Subject.query.all()
    return render_template('user/dashboard.html', user=user, subjects=subjects, completed_quizzes=completed_quizzes)

def user_view_subject(subject_id):
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    return render_template('user/subject.html', subject=subject)

def user_view_quiz(quiz_id):
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('user/quiz_details.html', quiz=quiz)

def start_quiz(quiz_id):
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    return render_template('user/take_quiz.html', quiz=quiz, questions=questions)

def submit_quiz(quiz_id):
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Calculate score
    total_correct = 0
    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option and int(selected_option) == question.correct_option:
            total_correct += 1
    
    # Save score
    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=total_correct
    )
    db.session.add(new_score)
    db.session.commit()
    
    flash(f'Quiz completed! Your score: {total_correct}/{len(questions)}')
    return redirect(url_for('user_dashboard'))

def quiz_summary():
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get all subjects
    subjects = Subject.query.all()
    
    summary_data = []
    
    for subject in subjects:
        # Count total quizzes for this subject
        total_quizzes = 0
        for chapter in subject.chapters:
            total_quizzes += len(chapter.quizzes)
        
        # Count attempted quizzes for this subject by the user
        attempted_quizzes = db.session.query(func.count(Score.id))\
            .join(Quiz, Score.quiz_id == Quiz.id)\
            .join(Subject, Subject.id == Quiz.chapter.has(Subject.id == subject.id))\
            .filter(Score.user_id == user_id)\
            .scalar()
        
        # Get average score for this subject
        avg_score = db.session.query(func.avg(Score.total_scored))\
            .join(Quiz, Score.quiz_id == Quiz.id)\
            .join(Subject, Subject.id == Quiz.chapter.has(Subject.id == subject.id))\
            .filter(Score.user_id == user_id)\
            .scalar()
        
        if avg_score:
            avg_score = round(avg_score, 2)
        else:
            avg_score = 0
            
        summary_data.append({
            'subject': subject,
            'total_quizzes': total_quizzes,
            'attempted_quizzes': attempted_quizzes,
            'avg_score': avg_score
        })
    
    return render_template('user/quiz_summary.html', user=user, summary_data=summary_data)
