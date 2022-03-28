from django.shortcuts import render
import folium
import numpy as np

# Create your views here.
def index(req):
    map = folium.Map([48.88, 2.33])
    for i in range(30):
        posx = np.random.normal(48.9, 0.06)
        posy = np.random.normal(2.3, 0.06)
        folium.Marker([posx, posy], popup="<b>Here</b>").add_to(map)
    context = {'map':map._repr_html_()}
    return render(req, 'common/index.html', context)