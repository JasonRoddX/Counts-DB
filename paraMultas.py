import paramiko
import time
import pandas as pd
from sqlalchemy import create_engine

hoy = time.strftime("%Y%m%d")

df = pd.DataFrame(columns=['SERVIDOR', 'CAMARA','MULTAS'])

if __name__ == '__main__':
    
    for i in range(5, 8):
        
        if i not in [3,34,36]:
            
                try:
                    
                    HOSTNAME = f'multas{i}.servidor.lan'
                    
                    print(f'Ingresando al servidor {HOSTNAME}')
                    
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    
                    client.connect(HOSTNAME, username='administrador', password='MultasPro2018')
                    
                    stdin, stdout, stderr = client.exec_command('python3 /home/administrador/Server/scripts/multas-lotes.py')
                    
                
                    for line in stdout:
                        line = line.strip('\n').split(' ')
                        
                        df.loc[len(df)] = line
                        
                    # if not stdout:
                    #     df.loc[len(df)] = [HOSTNAME.split('.'),'-','-']
                        
                    for line in stderr:
                        print('error:',line)
                    time.sleep(1)
                                        
                except Exception as e:
                    print(e)
                    print('Error en el servidor:', HOSTNAME)
                    
                finally:
                    client.close()

df.to_excel(f'resultados_excel/multas-lote-{hoy}.xlsx', index=False)

#engine = create_engine('postgresql://postgres:admin@localhost:5432/sap_db')

#df[['SERVIDOR', 'CAMARA','MULTAS']].to_sql('conteos_conteo', engine, if_exists='append', index=False)