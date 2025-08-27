# -*- coding: utf-8 -*-
"""
DAG para automação de download de dados de consumo energético da CCEE
usando o Tableau Scraper.

Created on Thu Mar 30 12:03:45 2023

@author: 50338 (CamilaFernandesdev)
"""


import logging
import pandas as pd
from pathlib import Path
from datetime import date, datetime, timedelta

import infra_copel
from infra_copel import SharepointSiteCopel, MongoHistoricoOficial

import airflow
from airflow import DAG
from airflow.decorators import dag
from airflow.decorators import task
from airflow import Variables

# Decorators: dags and task
# funções dentro de funções



# constants and Log
DAG_NAME = 'ccee_consumo_tableau'
logger = logging.getLogger('airflow.task')






@dag(schedule_interval='@montly',
     start_date=datetime(2023, 4, 1),
     catchup=False,
     tags=['consumo_energetico', 'CCEE', 'MongoDB', 'PowerBI', 'SharePoint'],
     )
def ccee_consumo_tableau():
    """doc stringers."""
    @task
    def primeira_tarefa():
        # importe dos modulos como infra_copel
        # importe das classes e funções
        # class Tal().metodo_tal()
        pass
    
    @task
    def tarefa_mongo():
        pass
    
    @task
    def tarefa_sharepoint():
        pass
    
    @task
    def tarefa_powerbi():
        pass
    
    #Definir ordem das tarefas
    primeira_tarefa() >> tarefa_mongo() >> tarefa_powerbi() # e mais qtas forem necessarias
    
    
dag = ccee_consumo_tableau()
    
