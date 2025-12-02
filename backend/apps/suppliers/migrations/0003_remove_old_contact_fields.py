from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0002_suppliercontact_contactaccess'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='contact_phone',
        ),
    ]