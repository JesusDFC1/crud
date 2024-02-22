from flask import Flask
from flask_cors import CORS
from flask import jsonify,request
import pymysql
from cryptography.fernet import Fernet

app=Flask(__name__)
## Nos permite acceder desde una api externa
CORS(app)
## Funcion para conectarnos a La base de datos de mysql
def conectar (vhost,vuser,vpass,vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn
# Ruta para consulta general del baul de contraseñas
@app.route("/")
def consulta_general():
    try:
        conn=conectar('localhost','root','','gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul """)
        datos=cur.fetchall()
        data=[]       
        for row in datos:
            dato={'id_baul':row[0],'Plataforma':row[1],'usuario':row[2],'clave':row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul':data,'mensaje':'Baul de contrasenas'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})
@app.route("/consulta_individual/<codigo>",methods=['GET'])
def consulta_individual(codigo):
    try:
        conn=conectar('localhost','root','','gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul where id_baul='{0}' """.format(codigo))
        datos=cur.fetchone()
        cur.close()
        conn.close()
        if datos!=None:
           dato={'id_baul':datos[0],'Plataforma':datos[1],'usuario':datos[2],'clave':datos[3]}
           return jsonify({'baul':dato,'mensaje':'Registro encontrado'})
        else:
            return jsonify({'mensaje':'Registro no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@app.route("/registro/",methods=['POST'])
def registro():
    try:
        conn=conectar('localhost','root','','gestor_contrasena')
        cur = conn.cursor()
        x=cur.execute(""" insert into baul (plataforma,usuario,clave) values \
            ('{0}','{1}','{2}')""".format(request.json['plataforma'],\
                request.json['usuario'],request.json['clave']))
        conn.commit() ## Para confirmar La inserción de La información
        cur.close()
        conn.close()
        return jsonify({'mensaje':'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Erro'})

@app.route("/eliminar/<codigo>",methods=['DELETE'])
def eliminar(codigo):
    try:
        conn=conectar('localhost','root','','gestor_contrasena')
        cur = conn.cursor()
        x=cur.execute(""" delete from baul where id_baul={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Erro'})

@app.route("/actualizar/<int:codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        query = """UPDATE baul SET plataforma=%s, usuario=%s, clave=%s WHERE id_baul=%s"""
        data = (request.json['plataforma'], request.json['usuario'], request.json['clave'], codigo)
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

if __name__ == "__main__":
    app.run(debug=True)