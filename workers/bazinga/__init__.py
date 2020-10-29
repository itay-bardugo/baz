import sys, os, django

sys.path.append(os.environ.get("DJANGO-ROOT-FOLDER"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baz.settings')
django.setup()
