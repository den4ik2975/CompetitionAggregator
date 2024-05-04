from src.aggregator.database.models import User

user = User(id=1, telegram_id=4242, name='Denis', favorites=[])
userShema = user.to_dto_model()
print(type(userShema.model_dump()))
