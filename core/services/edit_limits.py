from datetime import datetime, time
from zoneinfo import ZoneInfo

def can_head_edit(today_edit_count: int, actor_is_head: bool, now=None):
    if not actor_is_head:
        return False, 'Only Head can edit (Director bypass not covered here).'
    now = now or datetime.now(ZoneInfo('Africa/Nairobi'))
    cutoff = datetime.combine(now.date(), time(23,59), tzinfo=ZoneInfo('Africa/Nairobi'))
    if now > cutoff:
        return False, 'Edit window closed after 23:59 Africa/Nairobi.'
    if today_edit_count >= 3:
        return False, 'Daily edit limit reached (3).'
    return True, 'OK'
