from concurrent.futures import thread
from multiprocessing import context
from ntpath import join
from django.shortcuts import render
import threading
import unidecode
import folium
import numpy as np
import pandas as pd
from . import models, query as q






def school_query():
    global school_query_res
    school_query_res = q.query5()
    

school_query_res = None
thread = threading.Thread(target=school_query)
thread.start()




def index(req):

    # Map displaying
    map = folium.Map([48.297, 4.07], zoom_start=6)
    loc = pd.DataFrame([
            [x[0].split('/')[-1], float(x[1].value), float(x[2].value), x[3].value] for x in q.query9()
        ], columns=['uai', 'x', 'y', 'name']
    )
    for uai, ser in loc.iterrows():
        posx, posy, uai, name = ser.x, ser.y, ser.uai, ser['name']
        folium.Marker(
            [posx, posy], 
            popup=f"<b>{name}</b><p>UAI Code : {uai}</p>",
            tooltip='Click here'
        ).add_to(map)
    context = {'map':map._repr_html_()}
    
    # For ministry and Academy data
    acad = '\n'.join([f'<li>{x[0].value}</li>' for x in q.query1()])
    minis = '\n'.join([f'<li>{x[0].value}</li>' for x in q.query3()])
    context['ministry'] = f'<ul>{minis}</ul>'
    context['academy'] = f'<ul>{acad}</ul>'
     
    return render(req, 'common/index.html', context)





def get_school(req):
    context = dict()
    
    thread.join()
    

    col = ['name', 'school', 'tel', 'siret', 'type', 'category','atitude', 'longitude', 'address', 'city', 'region', 'academy', 'ministry']
    
    schools_info = pd.DataFrame([
        [str(y.value) if hasattr(y, 'value') else y.split('/')[-1] for y in x] 
        for x in school_query_res
    ], columns=col)
    schools_info.siret = schools_info.siret.map(lambda x: int(eval(x)))
    schools_info['type'] = schools_info['type'].map(lambda x: x.split('#')[-1])


    if not req.POST:
        context['schools'] = schools_info.iterrows()

    else:
        entry = req.POST.get('s-bar').lower()
        entry = unidecode.unidecode(entry)
        matched_school = set()

        for col in schools_info:
            try:
                # remove accents
                c = schools_info[col].astype(str).str.normalize('NFKD').\
                        str.encode('ascii', errors='ignore').str.decode('utf-8')
                matching = c.str.contains(entry)
                matched_school.update(matching[matching].index.values)
            except:
                pass

        matched_school = list(matched_school)
        context['schools'] = schools_info.iloc[matched_school].iterrows()
        
        if not matched_school:
            context['no_results'] = True
        
    return render(req, 'common/school.html', context=context)






def get_person(req, type='student'):
    context = dict()
    res = q.query10() if type=='student' else q.query11()
    
    student_info = pd.DataFrame([
        [str(y) if hasattr(y, 'value') or y is None else y.split('#')[-1] for y in x] 
        for x in res
    ])
    student_info.columns = ['individual', 'type', 'firstName', 
                'lastName', 'age', 'email', 'nationality', 
                'tel', 'address', 'city']

    context['person'] = student_info.to_html(index=False, classes='pers-df')
    return render(req, 'common/person.html', context=context)




