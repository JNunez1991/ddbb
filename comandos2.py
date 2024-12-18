#%% Conecto a la BBDD
import mysql.connector as mc

conn = mc.connect(
    host='localhost',
    user='root',
    passwd='SQL_dev_1991@',
    database="ddbb_test")

cursor = conn.cursor()
p = cursor.execute
#%%


#%% Creacion de nueva BBDD 
# cursor.execute("SHOW DATABASES")
# for d in cursor:
#     print(d)
# cursor.execute("CREATE DATABASE ddbb_test")
#%%


#%% Borrar tabla
# drop_table= "DROP TABLE IF EXISTS t_clientes;"
# p(drop_table)
# conn.commit()
#%%


#%% Creacion de tablas
create_t_clientes = """
    CREATE TABLE IF NOT EXISTS t_clientes (
        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        telefono VARCHAR(20),
        mail VARCHAR(100)
    ) AUTO_INCREMENT=1001;
    """
p(create_t_clientes)


create_t_funcionarios = """
    CREATE TABLE IF NOT EXISTS t_funcionarios (
        id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(20),
        Fnacim date
    ) AUTO_INCREMENT=101;
    """
p(create_t_funcionarios)


conn.commit()
#%%


#%% Insertar valores
insert_query1 = """
    INSERT INTO t_clientes (nombre, telefono, mail)
    VALUES (%s, %s, %s);
    """
valores = ("Juan Pérez", "099-099099", "juan@example.com")
p(insert_query1, valores)


insert_query2 = """
    INSERT INTO t_funcionarios (nombre, direccion, Fnacim)
    VALUES (%s, %s, %s);
    """
valores = ("Maria Azucena", "Colonia 987", "1990-04-21")
p(insert_query2, valores)

conn.commit()
#%%


#%% Borrar valores de tabla
delete_query = """
    DELETE FROM t_clientes WHERE id_cliente = %s;
"""
del_idx = (1001,)

p(delete_query, del_idx)
conn.commit()
#%%