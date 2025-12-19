# backend/ops/utils/dt.py
from django.utils import timezone
from django.utils.formats import date_format



def format_dt_jst(dt) -> str:
    # JST で統一フォーマット
    with timezone.override("Asia/Tokyo"):
        return date_format(timezone.localtime(dt), "Y-n-j H:i")
