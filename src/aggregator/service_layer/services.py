from datetime import timedelta, datetime
from typing import List, Optional, Tuple

from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchemaAdd, UserSchemaAuth, UserSchema, OlympiadSchemaCard, \
    OlympiadSchemaView
from src.aggregator.database import crud
from src.aggregator.service_layer import utils
from src.aggregator.service_layer.utils import logging_wrapper
from src.setup import pwd_context, settings


@logging_wrapper
async def get_olympiad(
        olympiad_id: int,
        auth: UserSchema | bool,
        db_session: async_session,
) -> OlympiadSchemaView | None:
    """
    Service function to get olympiad by its id
    Function get from database olympiad by id and transfers it to Pydantic DTO model
    Then if request were from authenticated user function gets additional data from it
    Then function accumulates all information in OlympiadSchemaView
    formatting in parallel some data with the help of utils

    Args:
        olympiad_id: olympiad id to get information
        auth: UserSchema or False, from middleware
        db_session: session for database, from middleware

    Returns: OlympiadSchemaView - pydantic model with formatted data for frontend

    """
    olympiad = await crud.get_olympiad_by_id(session=db_session,
                                             olympiad_id=olympiad_id)

    if olympiad is None:
        return None

    olympiad = olympiad.to_dto_model()

    logger.info('Got olympiad')

    is_favorite, is_notified, is_participant = False, False, False

    if olympiad is None:
        return None

    if auth is not False:
        if olympiad.id in auth.participates:
            is_participant = True
        if olympiad.id in auth.favorites:
            is_favorite = True
        if olympiad.id in auth.notifications:
            is_notified = True

    return OlympiadSchemaView(
        id=olympiad.id,
        title=olympiad.title,
        level=olympiad.level,
        dates=await utils.jsonify_dates(olympiad),
        date=await utils.get_nearest_date_str(olympiad),
        description=olympiad.description,
        subjects=olympiad.subjects,
        classes=await utils.humanize_classes(olympiad),
        is_favorite=is_favorite,
        is_notified=is_notified,
        is_participant=is_participant
    )


@logging_wrapper
async def get_olympiads(
        auth: UserSchema | bool,
        db_session: async_session,
) -> List[OlympiadSchemaCard]:
    """
    Get a list of all available olympiads.

    Args:
        auth: Authenticated user's info, or False if not authenticated.
        db_session: Asynchronous database session.

    Returns:
        List[OlympiadSchemaCard]: List of olympiads in card format.
    """
    olympiads = await crud.get_all_olympiads(session=db_session)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=olympiads,
                                                                  auth=auth)

    logger.info('Got olympiad cards')
    return card_olympiads


@logging_wrapper
async def get_user_by_id(
        user_id: int,
        db_session: async_session,
) -> UserSchema | None:
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db_session (async_session): The asynchronous database session.

    Returns:
        UserSchema | None: The user's information as a UserSchema object, or None if the user is not found.
    """
    user = await crud.get_user_by_id(session=db_session,
                                     user_id=user_id)

    logger.info('Got user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_new_user(
        user: UserSchemaAdd,
        db_session: async_session,
) -> UserSchema | None:
    """
    Add a new user to the database. Function also hashes password for more security.

    Args:
        user (UserSchemaAdd): The user information to be added.
        db_session (async_session): The asynchronous database session.

    Returns:
        UserSchema | None: The added user's information as a UserSchema object, or None if the user could not be added.
    """
    hashed_password = pwd_context.hash(user.password)
    user = await crud.add_user(session=db_session,
                               username=user.username,
                               mail=user.mail,
                               password=hashed_password)

    logger.info('Added new user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def auth_user(
        user_login: UserSchemaAuth,
        db_session: async_session,
) -> Optional[Tuple[UserSchema | None, str | None]]:
    """
    Authenticate a user and generate an access token.

    Args:
        user_login (UserSchemaAuth): An object containing the user's login credentials (either email or username, and password).
        db_session (async_session): The asynchronous database session.

    Returns:
        Optional[Tuple[UserSchema | None, str | None]]: A tuple containing the authenticated user's information as a UserSchema object and the generated access token as a string, or (None, None) if authentication fails.

    This function attempts to authenticate the user based on the provided login credentials.
    It first checks if the user exists in the database by looking for a matching email or username.
    If a user is found, the function verifies the provided password using the `pwd_context.verify` method.

    If the password is correct, the function generates an access token with an expiration
    time based on the configured `access_token_expire_minutes` setting. The access token is created using the
    `utils.create_access_token` function.

    If the user is successfully authenticated, the function returns a tuple containing the user's information as a
    UserSchema object and the generated access token as a string. If authentication fails
    (either due to the user not being found or an incorrect password), the function returns (None, None).

    The function also logs messages indicating whether the authentication was successful or failed.
    """
    logger.info('Try user auth')
    user = await crud.get_user_by_email(session=db_session,
                                        mail=user_login.login)
    if user is None:
        user = await crud.get_user_by_username(session=db_session,
                                               username=user_login.login)
    if user is None:
        return None, None

    if pwd_context.verify(user_login.password, user.hashed_password):
        access_token_expires = timedelta(minutes=settings.encryption.access_token_expire_minutes)
        access_token = await utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info('User auth success')
        return user.to_dto_model(), access_token

    logger.info('User auth failed')
    return None, None


@logging_wrapper
async def is_authenticated(
        request: Request,
        db_session: async_session,
) -> UserSchema | bool:
    """
    Checks if the user is authenticated based on the access token in the request cookies.

    Args:
        request (Request): The incoming HTTP request object.
        db_session (async_session): The asynchronous database session.

    Returns:
        UserSchema | bool: Returns the UserSchema object if the user is authenticated, False otherwise.
    """
    logger.info('Auth check')

    access_token = request.cookies.get('access_token')

    if not access_token:
        return False

    access_token = access_token.replace('Bearer ', '')

    username = await utils.decode_access_token(access_token)
    user = await crud.get_user_by_username(session=db_session, username=username)

    if user is None:
        logger.info('Auth check failed')
        return False

    return user.to_dto_model()


@logging_wrapper
async def add_user_favorite(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    """
    Adds an olympiad to the user's favorites.

    Args:
        user_id (int): The ID of the user.
        olympiad_id (int): The ID of the olympiad to be added as a favorite.
        db_session (async_session): The asynchronous database session.

    Returns:
        UserSchema | None: Returns the updated UserSchema object if successful, None otherwise.
    """
    user = await crud.update_user_favorites(session=db_session,
                                            user_id=user_id,
                                            olympiad_id=olympiad_id)

    logger.info('Added user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def delete_user_favorite(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    """
    Removes an olympiad from the user's favorites.

    Args:
        user_id (int): The ID of the user.
        olympiad_id (int): The ID of the olympiad to be removed from favorites.
        db_session (async_session): The asynchronous database session.

    Returns:
        UserSchema | None: Returns the updated UserSchema object if successful, None otherwise.
    """
    user = await crud.delete_user_favorite(session=db_session,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_user_participate(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    """
    Adds an olympiad to the user's list of participated olympiads.

    Args:
        user_id (int): The ID of the user.
        olympiad_id (int): The ID of the olympiad to be added.
        db_session (async_session): The database session object.

    Returns:
        UserSchema | None: The updated user object with the olympiad added to the participated list,
        or None if the operation fails.

    """
    user = await crud.update_user_participate(session=db_session,
                                              user_id=user_id,
                                              olympiad_id=olympiad_id)

    logger.info('Added user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def delete_user_participate(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    """
    Removes an olympiad from the user's list of participated olympiads.

    Args:
        user_id (int): The ID of the user.
        olympiad_id (int): The ID of the olympiad to be removed.
        db_session (async_session): The database session object.

    Returns:
        UserSchema | None: The updated user object with the olympiad removed from the participated list,
        or None if the operation fails.
    """
    user = await crud.delete_user_favorite(session=db_session,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_notifications(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | bool:
    """
    Schedules notifications for a given user and olympiad.

    This function adds notifications for the user with the specified `user_id` for the olympiad
    with the specified `olympiad_id`. It calculates the dates for notifications based on the
    olympiad's dates and the user's preferences (the number of days before the olympiad to send
    a notification, specified by `user.n`). The notifications are then added to the database.

    Args:
        user_id (int): The ID of the user for whom to schedule notifications.
        olympiad_id (int): The ID of the olympiad for which to schedule notifications.
        db_session (async_session): The database session to use for querying and updating data.

    Returns:
        UserSchema | bool: If successful, returns the updated UserSchema object. Otherwise, returns False.
    """
    logger.info('Started scheduling notifications')

    user = await crud.update_user_notification(session=db_session,
                                               user_id=user_id,
                                               olympiad_id=olympiad_id)

    olympiad = await crud.get_olympiad_by_id(session=db_session,
                                             olympiad_id=olympiad_id)

    if user is None or olympiad is None:
        return False

    now: datetime = datetime.now()
    date_now = datetime(now.year, now.month, now.day)
    delta = timedelta(days=user.n)

    for stage, olympiad_str_list in olympiad.dates.values():
        olympiad_str_date = olympiad_str_list[0]
        olympiad_date = datetime.strptime(olympiad_str_date, '%Y-%m-%d')
        text = (f'Напоминание об олимпиаде: {olympiad.title}\''
                f'Этап {stage} начинается {olympiad_str_date}')

        if date_now <= olympiad_date <= date_now + delta:
            await crud.add_notification(session=db_session,
                                        user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        text=text,
                                        date=date_now)

        elif date_now + delta <= olympiad_date:
            await crud.add_notification(session=db_session,
                                        user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        text=text,
                                        date=olympiad_date - delta)

    logger.info('Schedule success')
    return user.to_dto_model()



@logging_wrapper
async def delete_notifications(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | bool:
    """
    Deletes all notifications related to a specific olympiad for a user.

    Args:
        user_id (int): The ID of the user.
        olympiad_id (int): The ID of the olympiad for which notifications should be deleted.
        db_session (async_session): The database session object.

    Returns:
        UserSchema | bool: True if the notifications were successfully deleted, False otherwise.

    """
    result = await crud.delete_notifications_by_user_and_olympiad_id(session=db_session,
                                                                     user_id=user_id,
                                                                     olympiad_id=olympiad_id)

    if result is None:
        return False
    return True


@logging_wrapper
async def search_olympiads(
        search_string: str,
        auth: UserSchema | bool,
        db_session: async_session,
) -> List[OlympiadSchemaCard]:
    """
    Search for Olympiads based on the provided search string.

    This function searches for Olympiads in the database using the given search string.
    It retrieves the matching Olympiads, converts them to the OlympiadSchemaCard format,
    and returns a list of OlympiadSchemaCard objects.

    Args:
        search_string (str): The search string to be used for filtering Olympiads.
        auth (UserSchema | bool): The authenticated user's information or False if not authenticated.
        db_session (async_session): The asynchronous database session.

    Returns:
        List[OlympiadSchemaCard]: A list of OlympiadSchemaCard objects representing the matching Olympiads.
    """
    logger.info(f'Started searching olympiads with query: {search_string}')

    results = await crud.search_for_olympiads(session=db_session,
                                              search_string=search_string)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=results,
                                                                  auth=auth)

    return card_olympiads


@logging_wrapper
async def get_user_choices(
        user_id: int,
        auth: UserSchema | bool,
        key: str,
        db_session: async_session
) -> List[OlympiadSchemaCard]:
    """
    Retrieve a list of Olympiads based on the user's choices.

    This function retrieves a list of Olympiads based on the user's choices specified by the provided key.
    It fetches the user's information from the database, retrieves the Olympiad IDs associated with the given key,
    and converts the corresponding Olympiads to the OlympiadSchemaCard.

    Args:
        user_id (int): The ID of the user.
        auth (UserSchema | bool): The authenticated user's information or False if not authenticated.
        key (str): The key representing the user's choice (e.g., 'favorites', 'participates', 'notifications').
        db_session (async_session): The asynchronous database session.

    Returns:
        List[OlympiadSchemaCard]: A list of OlympiadSchemaCard objects representing the user's chosen Olympiads.
    """
    logger.info(f'Getting choices: {key}')
    user = await crud.get_user_by_id(session=db_session, user_id=user_id)

    olympiads = []
    for olympiad_id in getattr(user, key):
        olympiad = await crud.get_olympiad_by_id(session=db_session, olympiad_id=olympiad_id)
        olympiads.append(olympiad)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=olympiads, auth=auth)

    return card_olympiads


@logging_wrapper
async def filter_olympiads(
        auth: UserSchema | bool,
        subjects: List[str] | None,
        grades: List[int] | None,
        db_session: async_session
) -> List[OlympiadSchemaCard]:
    """
    Filter olympiads based on subjects and grades.
    It retrieves the matching Olympiads, converts them to the OlympiadSchemaCard format,
    and returns a list of OlympiadSchemaCard objects.

    Args:
        auth (UserSchema | bool): The authenticated user or False if not authenticated.
        subjects (List[str] | None): A list of subject strings to filter by, or None for no subject filtering.
        grades (List[int] | None): A list of grade integers to filter by, or None for no grade filtering.
        db_session (async_session): The database session to use for querying.

    Returns:
        List[OlympiadSchemaCard]: A list of OlympiadSchemaCard objects representing the filtered olympiads.
    """
    logger.info('Started filtered olympiads')

    results = await crud.filter_olympiads(subjects=subjects,
                                          grades=grades,
                                          session=db_session)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=results,
                                                                  auth=auth)

    return card_olympiads


@logging_wrapper
async def sort_olympiads(
        sort_clause: str,
        olympiads: List[OlympiadSchemaCard]
) -> List[OlympiadSchemaCard]:
    """
    Sort the list of olympiads based on the specified sort clause.

    Args:
        sort_clause (str): The sort clause to use for sorting. Can be either 'name' or 'date'.
        olympiads (List[OlympiadSchemaCard]): The list of olympiads to be sorted.

    Returns:
        List[OlympiadSchemaCard]: The sorted list of olympiads.
    """
    logger.info('Started sorting')

    if sort_clause == 'name':
        olympiads.sort(key=lambda x: x.title)

    elif sort_clause == 'date':
        to_sort = []
        to_back = []

        for olympiad in olympiads:
            if isinstance(olympiad.date, datetime):
                to_sort.append(olympiad)
            else:
                to_back.append(olympiad)
        to_sort.sort(key=lambda x: x.date)

        olympiads = to_sort + to_back

    return olympiads


@logging_wrapper
async def change_n(
        user_id: int,
        n: int,
        db_session: async_session
) -> UserSchema:
    """
    Change the value of 'n' for a given user.

    Args:
        user_id (int): The ID of the user whose 'n' value needs to be changed.
        n (int): The new value of 'n' for the user.
        db_session (async_session): The database session to use for updating the user.

    Returns:
        UserSchema: The updated UserSchema object representing the user.
    """
    user = await crud.update_user_n(session=db_session,
                                    user_id=user_id,
                                    n=n)

    return user.to_dto_model()

