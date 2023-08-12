from argparse import ArgumentParser
from enum import StrEnum
from pathlib import Path

from alembic import command
from alembic.config import Config

from src.common.bootstrapper import bootstrap
from src.common.settings import Settings

settings = Settings()

alembic_cfg = Config(Path(settings.base_dir).parent / "alembic.ini")


class Commands(StrEnum):
    CREATE_ADMIN = "create_admin"
    DELETE_ADMIN = "delete_admin"
    START = "start"
    MAKE_MIGRATIONS = "make_migrations"
    MIGRATE = "migrate"


def register_commands(parser: ArgumentParser) -> None:
    """
    Инициализация команд.
    :param parser: Парсер аргументов
    :return: None
    """

    commands = parser.add_subparsers(
        title="Управление администраторами", dest="commands", required=True
    )

    # Создание администратора
    create_admin_command = commands.add_parser(
        Commands.CREATE_ADMIN,
        help="Создать администратора с заданным именем и паролем.",
    )
    create_admin_command.add_argument(
        "--username", required=True, help="Имя пользователя"
    )
    create_admin_command.add_argument("--password", required=True, help="Пароль")

    # Удаление администратора
    delete_admin_command = commands.add_parser(
        Commands.DELETE_ADMIN, help="Удалить администратора с заданным именем."
    )
    delete_admin_command.add_argument(
        "--username", required=True, help="Имя пользователя"
    )

    commands.add_parser(Commands.START, help="Запустить бота.")
    commands.add_parser(
        Commands.MAKE_MIGRATIONS, help="Сгенерировать миграции для базы данных."
    )
    commands.add_parser(Commands.MIGRATE, help="Внести изменения в базу данных.")


def command_line(args_list: list[str]) -> None:
    """
    Точка входа для CLI интерфейса бота.
    :param args_list: Список аргументов передаваемых в парсер
    :return: None
    """

    parser = ArgumentParser(
        prog="Shop Bot CLI", description="Интерфейс управление ботом-магазином."
    )
    register_commands(parser)

    args = parser.parse_args(args_list)

    # Обработчик команд администратора
    match args.commands:
        case Commands.CREATE_ADMIN:
            return print(settings.base_dir)
        case Commands.DELETE_ADMIN:
            return print("delete")
        case Commands.START:
            bootstrap()
        case Commands.MAKE_MIGRATIONS:
            command.revision(alembic_cfg, autogenerate=True)
        case Commands.MIGRATE:
            command.upgrade(alembic_cfg, "head")
