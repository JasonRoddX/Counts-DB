#!/usr/bin/env python
from operator import index
import paramiko
import time
import warnings
warnings.simplefilter(action='ignore', category = FutureWarning)
import pandas
import time
import subprocess
import psycopg2
from sqlalchemy import create_engine
from torch import cosine_similarity

while(True):
    
 hoy = time.strftime("%Y/%m/%d%H:%M:%S")
 finished = time.strftime("%Y/%m/%d %H:%M")
 df = pandas.DataFrame(columns=["SERVIDOR","CAMARA",'JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE','ENERO','FEBRERO','MARZO','ABRIL','OTROS','VIDEOS'])
 if __name__ == '__main__':
  for i in range(1, 38):    
    if i not in [2,3,9,10,14,17,34,36]:
            try:               
                HOSTNAME = f'multas{i}.servidor.lan'                
                print(f'Ingresando al servidor {HOSTNAME}')                
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())                
                client.connect(HOSTNAME, username='administrador', password='MultasPro2018')                
                stdin, stdout, stderr = client.exec_command('python3 /home/administrador/Server/scripts/contar.py')                
                for line in stdout:
                    print(line.strip('\n').split(' '))
                    to_append = line.strip('\n').split(' ')
                    a_series = pandas.Series(to_append, index = df.columns)
                    df = df.append(a_series, ignore_index=True)
                for line in stderr:
                    print('error:',line)
                time.sleep(1)
                servidor = line.strip('\n').split(' ')[0]       
            except Exception as e:
                print(e)
                print('Error en el servidor:', HOSTNAME)                
            finally:
                client.close()

 df.set_index(['SERVIDOR','CAMARA'], inplace=True)

 for i in range(1, 38):    
    if i not in [2,3,9,10,14,17,34,36]:
            try:                
                HOSTNAME = f'multas{i}.servidor.lan'                
                print(f'Buscando infracciones del servidor {HOSTNAME}')                
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())                
                client.connect(HOSTNAME, username='administrador', password='MultasPro2018')                
                stdin, stdout, stderr = client.exec_command('python3 /home/administrador/Server/scripts/multas-lotes.py')                
                for line in stdout:
                    line = line.strip('\n').split(' ')
                    df.loc[(line[0],line[1]),'MULTAS'] = line[2]
                for line in stderr:
                    print('error:',line)
                time.sleep(1)                
            except Exception as e:
                print(e)
                print('Error en el servidor:', HOSTNAME)                
            finally:
                client.close()

 df.reset_index(inplace=True)
 df = df.sort_values(by=['SERVIDOR','CAMARA'], inplace=False)
 df.fillna(0, inplace=True)
 df[['OTROS',
 'VIDEOS',
 'MARZO',
 'ABRIL',
 'MULTAS']]= df[['OTROS',
                    'VIDEOS',
                    'MARZO',
                    'ABRIL',
                    'MULTAS']].astype(int)
 #df.to_excel(f'registro/{hoy}-conteo.xlsx', index=False)
 df.index.names = ['id']
 df.sort_values(by=['MARZO'], ascending=[False], inplace=True)
 engine = create_engine('postgresql://postgres:admin@localhost:5432/sap_db')
 df[['SERVIDOR','CAMARA','MARZO','ABRIL','OTROS','VIDEOS','MULTAS']].to_sql('conteos_conteo', engine, if_exists='replace')
 
 print('Proceso terminado', finished)
