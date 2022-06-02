import mysql.connector
import socket

hostname = socket.gethostname()


conexion1 = mysql.connector.connect(
    host="localhost", user="root", passwd="MultasPro2018", database="c1dataMultas"
)
cursor1 = conexion1.cursor()
cursor1.execute(
    "SELECT multas.multa_id_camara, camaras.cam_cod, multas.multa_id_lote, COUNT(*) FROM multas INNER JOIN camaras ON multas.multa_id_camara=camaras.id_camara WHERE multas.multa_id_lote=0 AND SUBSTRING(multas.multa_fecha,1,8) BETWEEN 20000101 AND 20261231 GROUP BY multas.multa_id_camara, camaras.cam_cod, multas.multa_id_lote;"
)
for tabla in cursor1:
    print(hostname, tabla[1], tabla[3])
conexion1.close()

# SELECT multas.multa_id_camara, camaras.cam_cod, multas.multa_id_lote, COUNT(*) FROM multas INNER JOIN camaras ON multas.multa_id_camara=camaras.id_camara WHERE multas.multa_id_lote=0 AND SUBSTRING(multas.multa_fecha,1,8) BETWEEN 20000101 AND 20261231 GROUP BY multas.multa_id_camara, camaras.cam_cod, multas.multa_id_lote;
