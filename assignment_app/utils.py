
from .models import Logs



def log_user_action(user, action):
    from datetime import datetime
    date=datetime.now().strftime("%Y-%m-%d %H:%M")
    Logs.objects.create(USER=user, logtext=action,timestamp=date)
    