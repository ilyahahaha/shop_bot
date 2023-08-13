from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.common.database import get_session
from src.models import User

router = Router()


@router.message(Command(commands=["start"]))
async def start_command(message: Message) -> None:
    session = await get_session()

    user = await User.find_by_user_id(session, str(message.from_user.id))

    if user is None:
        user = User(
            user_id=str(message.from_user.id),
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

        await user.save(session)

    await message.answer(f"hello {user.user_id}")
