import asyncio
import json
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.config import settings
from api.database import async_session
from api.exercises.models import Exercise, ExercisePhoto

data_path = Path(__file__).parent.joinpath("data.json")


with open(data_path, "r", encoding="UTF-8") as f:
    data = json.load(f)


async def create_exercise(
        async_session: AsyncSession,
        name: str,
        muscle: str,
        additional_muscle: str,
        exercise_type: str,
        equipment: str,
        difficulty: str
) -> Exercise:
    new_exercise = Exercise(
        name=name,
        muscle=muscle,
        additional_muscle=additional_muscle,
        type=exercise_type,
        equipment=equipment,
        difficulty=difficulty
    )
    async_session.add(new_exercise)
    await async_session.commit()
    await async_session.refresh(new_exercise)
    return new_exercise


async def create_exercise_photo(
        async_session: AsyncSession,
        exercise_id: UUID,
        path: str
) -> ExercisePhoto:
    new_exercise_photo = ExercisePhoto(
        exercise_id=exercise_id,
        path=path
    )
    async_session.add(new_exercise_photo)
    await async_session.commit()
    await async_session.refresh(new_exercise_photo)
    return new_exercise_photo


async def main(data_dict):
    c = 1
    async with async_session() as session:
        print('entrypoint function')
        for exercise in data_dict:
            print(f"{c}/588")
            name = exercise.get("name")
            muscle = exercise.get("muscle")
            additional_muscle = exercise.get("additionalMuscle")
            exercise_type = exercise.get("type")
            equipment = exercise.get("equipment")
            difficulty = exercise.get("difficulty")
            photos = exercise.get("photos")

            exercise = await create_exercise(
                session, name, muscle, additional_muscle, exercise_type, equipment, difficulty
            )

            c += 1
            for photo in photos:
                photo_name = photo.split("/")[-1]
                exercise_photo = await create_exercise_photo(
                    session, exercise.id, settings.S3_MEDIA_PATH + "exercises/" + photo_name
                )


asyncio.run(main(data))
