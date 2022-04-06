from django.db import models
from rdflib import Graph
import os
import threading



graph = None
# Create your models here.

def load_data():
    global graph
    g = Graph()
    g.parse('./ontology/fo22.owl')
    graph = g


thread = threading.Thread(target=load_data)
thread.start()
