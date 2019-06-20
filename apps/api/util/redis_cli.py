import redis

exec_file_redis = redis.Redis(db=2)
celery_redis = redis.Redis(db=3)