from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, fields, validate, validates_schema

ma = Marshmallow()


class ExerciseSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, load_default=None)


class WorkoutExerciseSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=1))

    @validates_schema
    def require_a_measure(self, data, **kwargs):
        has_reps_and_sets = data.get('reps') is not None and data.get('sets') is not None
        if not has_reps_and_sets and data.get('duration_seconds') is None:
            raise ValidationError('Provide reps and sets, or duration_seconds.')


class WorkoutExerciseWithExerciseSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutExerciseWithWorkoutSchema(WorkoutExerciseSchema):
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseWithExerciseSchema, many=True, dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseWithWorkoutSchema, many=True, dump_only=True
    )