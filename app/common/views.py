from concurrent.futures import thread
from multiprocessing import context
from ntpath import join
from django.shortcuts import render
import threading
import folium
import numpy as np
import pandas as pd
from . import models, query as q
from .models import thread


def index(req):

    # Map displaying
    map = folium.Map([48.297, 4.07], zoom_start=6)
    loc = pd.DataFrame([
            [x[0].split('/')[-1], float(x[1].value), float(x[2].value), x[3].value] for x in q.query9()
        ], columns=['uai', 'x', 'y', 'name']
    )
    for uai, ser in loc.iterrows():
        posx, posy, uai, name = ser.x, ser.y, ser.uai, ser['name']
        folium.Marker([posx, posy], popup=f"<b>{name}</b><p>UAI Code : {uai}</p>").add_to(map)
    context = {'map':map._repr_html_()}
    
    # For ministry and Academy data
    acad = '\n'.join([f'<li>{x[0].value}</li>' for x in q.query1()])
    minis = '\n'.join([f'<li>{x[0].value}</li>' for x in q.query3()])
    context['ministry'] = f'<ul>{minis}</ul>'
    context['academy'] = f'<ul>{acad}</ul>'
     

    return render(req, 'common/index.html', context)


def get_school(req, entry=None):
    context = dict()
    
    col = ['name', 'school', 'tel', 'siret', 'type', 'category','atitude', 'longitude', 'address', 'city', 'region', 'academy', 'ministry']
    
    schools_info = pd.DataFrame([
        [str(y.value) if hasattr(y, 'value') else y.split('/')[-1] for y in x] 
        for x in q.query5()
    ], columns=col)
    schools_info.siret = schools_info.siret.map(lambda x: int(eval(x)))
    schools_info['type'] = schools_info['type'].map(lambda x: x.split('#')[-1])
    context['schools'] = schools_info.iterrows()
    return render(req, 'common/school.html', context=context)


def get_person(req, type='student'):
    context = dict()
    context['person'] = pd.DataFrame([range(5), range(5)]).to_html(index=False, classes='pers-df')
    return render(req, 'common/person.html', context=context)
