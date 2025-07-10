from celery import Celery
from models.database import init_db

init_db()
celery_app = Celery(
    "cyberdashboard",
    broker="redis://localhost:6379/0",  # 👈 Redis como broker
    backend="redis://localhost:6379/0"  # 👈 Redis como backend de resultados
)
import routes.tasks
def init_celery(app):
    celery_app.conf.update(app.config)  # Coge la config de Flask
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    celery_app.autodiscover_tasks(['routes'])
