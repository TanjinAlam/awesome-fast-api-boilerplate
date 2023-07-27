from functools import wraps

from core.db import SessionLocal


# class Transactional:
#     def __call__(self, func):
#         @wraps(func)
#         async def _transactional(*args, **kwargs):
#             try:
#                 result = await func(*args, **kwargs)
#                 await session.commit()
#             except Exception as e:
#                 await session.rollback()
#                 raise e

#             return result

#         return _transactional


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            async with SessionLocal() as db:
                try:
                    result = await func(db, *args, **kwargs)
                    await db.commit()
                except Exception as e:
                    await db.rollback()
                    print("ERROR",e)
                    raise e

                return result

        return _transactional