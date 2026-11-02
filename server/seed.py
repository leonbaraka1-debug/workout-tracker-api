#!/usr/bin/env python3
from datetime import date, timedelta

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing tables...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    pushup = Exercise(name='Push-up', category='strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='strength', equipment_needed=False)
    plank = Exercise(name='Plank', category='core', equipment_needed=False)
    curl = Exercise(name='Dumbbell Curl', category='strength', equipment_needed=True)
    rope = Exercise(name='Jump Rope', category='cardio', equipment_needed=True)
    db.session.add_all([pushup, squat, plank, curl, rope])
    db.session.commit()

    print('Seeding workouts...')
    today = date.today()
    upper = Workout(date=today, duration_minutes=45, notes='Upper body focus')
    legs = Workout(date=today - timedelta(days=2), duration_minutes=60, notes='Leg day')
    cardio = Workout(date=today - timedelta(days=4), duration_minutes=30, notes=None)
    db.session.add_all([upper, legs, cardio])
    db.session.commit()

    print('Linking exercises to workouts...')
    db.session.add_all([
        WorkoutExercise(workout=upper, exercise=pushup, reps=15, sets=3),
        WorkoutExercise(workout=upper, exercise=curl, reps=12, sets=3),
        WorkoutExercise(workout=upper, exercise=plank, duration_seconds=60),
        WorkoutExercise(workout=legs, exercise=squat, reps=20, sets=4),
        WorkoutExercise(workout=legs, exercise=plank, duration_seconds=90),
        WorkoutExercise(workout=cardio, exercise=rope, duration_seconds=600),
    ])
    db.session.commit()
    print('Done seeding.')