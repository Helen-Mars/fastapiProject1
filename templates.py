from datetime import datetime
from fastapi.templating import Jinja2Templates


def datetimeformat(value: datetime, fmt='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(fmt)
    return value


# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")
templates.env.filters['datetimeformat'] = datetimeformat
