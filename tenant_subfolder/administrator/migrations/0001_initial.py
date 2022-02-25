# Generated by Django 4.0 on 2022-01-18 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('is_company', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_branch_user', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_super_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_name', models.CharField(max_length=30)),
                ('ar_name', models.CharField(max_length=30)),
                ('en_place', models.CharField(max_length=30)),
                ('ar_place', models.CharField(max_length=30)),
                ('en_district', models.CharField(max_length=30)),
                ('ar_district', models.CharField(max_length=30)),
                ('cr_no', models.CharField(max_length=15)),
                ('vat_no', models.CharField(max_length=15)),
                ('lan_no', models.CharField(max_length=15)),
                ('logo', models.ImageField(null=True, upload_to='media/')),
                ('status', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'db_table': 'branches',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_name', models.CharField(max_length=30)),
                ('ar_name', models.CharField(max_length=30)),
                ('en_place', models.CharField(max_length=30)),
                ('ar_place', models.CharField(max_length=30)),
                ('en_district', models.CharField(max_length=30)),
                ('ar_district', models.CharField(max_length=30)),
                ('cr_no', models.CharField(max_length=15)),
                ('vat_no', models.CharField(max_length=15)),
                ('lan_no', models.CharField(max_length=15)),
                ('logo', models.ImageField(null=True, upload_to='media/')),
                ('status', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('branch_count', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='administrator.user')),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('iqama_no', models.CharField(max_length=15, null=True)),
                ('branches', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.branches')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_id', to='administrator.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_id', to='administrator.user')),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='BranchManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('iqama_no', models.CharField(max_length=15, unique=True)),
                ('branches', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches_id', to='administrator.branches')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch_manager_id', to='administrator.user')),
            ],
            options={
                'db_table': 'branch_manager',
            },
        ),
        migrations.AddField(
            model_name='branches',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.company'),
        ),
    ]