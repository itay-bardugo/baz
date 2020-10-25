import sys, os, django

sys.path.append(os.environ.get("DJANGO-ROOT-FOLDER"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')
django.setup()
