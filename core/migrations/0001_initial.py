# Generated by Django 3.0.8 on 2020-07-06 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('PROCESSING', 'Processing')], default='PROCESSING', max_length=10)),
                ('result', models.CharField(choices=[('APPROVED', 'Approved'), ('REFUSED', 'Refused')], max_length=10)),
                ('refused_policy', models.CharField(choices=[('APPROVED', 'Approved'), ('REFUSED', 'Refused')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=6)),
                ('terms', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('cpf', models.CharField(max_length=11)),
                ('birthdate', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=4, max_digits=6)),
                ('terms', models.PositiveSmallIntegerField()),
                ('income', models.DecimalField(decimal_places=6, max_digits=8)),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit', to='core.Credit')),
            ],
        ),
    ]