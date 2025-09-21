from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

GROUP_RULES = {
    'DEPUTY': [
        ('core', 'student', ['add', 'change', 'view']),
        ('core', 'classlevel', ['view']),
        ('core', 'term', ['view']),
        ('core', 'academicyear', ['view']),
    ],
    'CASHIER': [
        ('core', 'payment', ['add', 'view']),
        ('core', 'student', ['view']),
        ('core', 'classlevel', ['view']),
        ('core', 'term', ['view']),
        ('core', 'academicyear', ['view']),
    ],
    'HEAD': [
        ('core', 'payment', ['add', 'change', 'view']),
        ('core', 'ledgerentry', ['view']),
        ('core', 'student', ['view']),
        ('core', 'classlevel', ['view']),
        ('core', 'term', ['view']),
        ('core', 'academicyear', ['view']),
    ],
    'DIRECTOR': 'ALL',
}

def _perm_codename(verb: str, model: str) -> str:
    return f"{verb}_{model}"

def ensure_groups_and_perms(sender, **kwargs):
    with transaction.atomic():
        groups = {}
        for name in GROUP_RULES.keys():
            g, _ = Group.objects.get_or_create(name=name)
            groups[name] = g

        core_cts = ContentType.objects.filter(app_label='core')
        all_core_perms = Permission.objects.filter(content_type__in=core_cts)
        groups['DIRECTOR'].permissions.set(all_core_perms)

        for grp, rules in GROUP_RULES.items():
            if grp == 'DIRECTOR' or rules == 'ALL':
                continue
            wanted = []
            for app_label, model, verbs in rules:
                ct = ContentType.objects.get(app_label=app_label, model=model)
                for v in verbs:
                    code = _perm_codename(v, model)
                    try:
                        p = Permission.objects.get(content_type=ct, codename=code)
                        wanted.append(p)
                    except Permission.DoesNotExist:
                        continue
            groups[grp].permissions.set(wanted)
