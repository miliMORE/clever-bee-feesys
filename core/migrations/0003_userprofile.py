from django.db import migrations, models
import uuid
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_import_ref_idx_core_import_referen_583286_idx_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('role', models.CharField(max_length=12, choices=[('DIRECTOR','Director'),('HEAD','Head Teacher'),('DEPUTY','Deputy Head'),('CASHIER','Cashier')], null=True, blank=True)),
                ('user', models.OneToOneField(on_delete=models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
