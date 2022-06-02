import os
import re
import socket

servidor = socket.gethostname()

camaras = []
for root, dirs, files in os.walk("/var/www/clients/client1/web1/web/data/SinDetectar"):
    if re.search(r'\d\d\d\d', root.split("/")[-1]):
        camara = root.split("/")[-1]
                
        junio = 0
        julio = 0
        agosto = 0
        septiembre = 0
        octubre = 0
        noviembre = 0
        diciembre = 0
        enero = 0
        otros = 0
        
        for file in files:
            if file.endswith(".jpg"):
                
                if re.search(r'_I-', file):
                    
                    if file[6:12] == "202106":
                        junio += 1
                    if file[6:12] == "202107":
                        julio += 1
                    elif file[6:12] == "202108":
                        agosto += 1
                    elif file[6:12] == "202109":
                        septiembre += 1
                    elif file[6:12] == "202110":
                        octubre += 1
                    elif file[6:12] == "202111":
                        noviembre += 1
                    elif file[6:12] == "202112":
                        diciembre += 1
                    elif file[6:12] == "202201":
                        enero += 1
                    else: 
                        otros += 1
        # if junio < 99:
        #     junio = 0
        # if julio < 99:
        #     julio = 0
        # if agosto < 99:
        #     agosto = 0
        # if septiembre < 99:
        #     septiembre = 0
        # if octubre < 99:
        #     octubre = 0
        # if noviembre < 99:
            # noviembre = 0
        # if diciembre < 99:
        #     diciembre = 0
        # if enero < 99:
        #     enero = 0
        # if otros < 99:
            # otros = 0
                 
        if not agosto == septiembre == octubre == noviembre == diciembre == enero == otros == 0:
            videos = 0                    
            for root, dirs, files in os.walk('/procesos/SinProcesar/'+camara):
                for file in files:
                    if file.endswith(".mp4"):
                        videos += 1
                        
                
            print(servidor, camara, junio, julio, agosto, septiembre, octubre, noviembre, diciembre, enero, otros, videos)
