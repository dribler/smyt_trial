from main.utils import create_model_class
from yaml import load
from django.conf import settings


with open(settings.DB_STRUCTURE[__package__], 'r') as f:
    scheme = load(f.read())


for table_name, table_metadata in scheme.iteritems():
    locals().update({table_name.title(): create_model_class(table_name, table_metadata)})

