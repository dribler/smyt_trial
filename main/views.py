import json
import datetime

from django.http.response import HttpResponse
from django.db.models import Model
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.forms import ModelForm as BaseModelForm

from main.utils import FIELD_TYPES
from main.models import *

app_models = dict()
for var_name, var in dict(locals()).iteritems():
    if isinstance(var, type) and issubclass(var, Model) and var is not Model:
        app_models[var_name] = var

field_type_names = dict()
for k, v in FIELD_TYPES.iteritems():
    field_type_names[v] = k


def home(request):
    model_list = list()
    for model_name, model in app_models.iteritems():
        model_list.append({'url': "/model/{}/".format(model_name),
                           'verbose_name': model._meta.verbose_name})

    return render(request, 'home.html', {"models": model_list})


def model(request, model_name):
    if model_name not in app_models:
        return HttpResponseNotFound("?!")
    else:
        model_class = app_models[model_name]

    if request.method == 'GET':
        json_data = {"objects": list(),
                     "fields": [{'name': f.name,
                                 'title': f.verbose_name,
                                 'type': field_type_names.get(f.__class__),
                                 'read_only': False if field_type_names.get(f.__class__) else True}
                                for f in model_class._meta.fields],
                     "title": model_class._meta.verbose_name}

        for obj in model_class.objects.all():
            obj_data = dict()
            for field in model_class._meta.fields:
                val = getattr(obj, field.name)
                if isinstance(val, datetime.date):
                    val = val.isoformat()

                obj_data.update({field.name: val})
            json_data['objects'].append(obj_data)
        return HttpResponse(json.dumps(json_data))
    elif request.method == 'POST':
        model_class = app_models[model_name]

        class ModelForm(BaseModelForm):
            class Meta:
                model = model_class
                field = [f.name for f in model_class._meta.fields]

        m_instance = None
        if request.POST.get('id'):
            try:
                m_instance = model_class.objects.get(pk=request.POST['id'])
            except Exception:
                pass

        form = ModelForm(request.POST, instance=m_instance)
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest('post data is not valid')

        return HttpResponse('Success')
