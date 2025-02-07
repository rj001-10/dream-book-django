# Generated by Django 5.1.2 on 2024-10-20 08:42

import django.core.validators
import django.db.models.deletion
import dream.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dream', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=dream.models.unique_image_path, validators=[django.core.validators.validate_image_file_extension]),
        ),
        migrations.CreateModel(
            name='DreamLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(blank=True, default=False, null=True)),
                ('is_dislike', models.BooleanField(blank=True, default=False, null=True)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dreamlikes', to='dream.dream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
