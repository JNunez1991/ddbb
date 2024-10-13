#%% Conecto a la BBDD
import mysql.connector as mc

conn = mc.connect(
    host='localhost',
    user='root',
    passwd='SQL_dev_1991@',
    database="ddbb_test")

cursor = conn.cursor()
p = cursor.execute # ejecuta una query
sp = cursor.callproc # ejecuta una stored procedure
#%%


#%% Creacion de nueva BBDD
# cursor.execute("SHOW DATABASES")
# for d in cursor:
#     print(d)
# cursor.execute("CREATE DATABASE ddbb_test")
#%%


############################################# CREACION DE USUARIOS y PERMISOS
#%% Obtengo todos los usuarios creados
query_users = """
    SELECT User, Host
    FROM mysql.user
"""
p(query_users)
users = cursor.fetchall()
users = list(set(x[0] for x in users))
print(users)
#%%


#%% Elimino usuario
user = 'janunez'
if user in users:
    query_drop_user = f"""
        DROP USER '{user}'@'localhost'
    """
    p(query_drop_user)
    conn.commit()
else:
    print("Usuario no existe")
#%%


#%% Creacion de usuarios
user, passw = "admin", "admin"
if user not in users:
    create_user = f"""
        CREATE USER '{user}'@'localhost' IDENTIFIED BY '{passw}';
        """
    try:
        p(create_user)
        conn.commit()
        print(f"Usuario '{user}' creado exitosamente.")
    except mc.Error as err:
        print(f"Error al crear el usuario: {err}")
else:
    print("Usario ya existente")
#%%


#%% Asignacion de privilegios por usuario
user = 'admin'
if user in users:
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON ddbb_test.* TO '{user}'@'localhost';"
    try:
        p(grant_privileges_query)
        conn.commit()
        print(f"Permisos otorgados a '{user}' en la base de datos 'ddbb_test'.")
    except mc.Error as err:
        print(f"Error al asignar privilegios: {err}")

    try:
        p("FLUSH PRIVILEGES;")
        conn.commit()
        print("Privilegios actualizados correctamente.")
    except mc.Error as err:
        print(f"Error al aplicar los privilegios: {err}")
#%%


############################################# MANEJO DE TABLAS
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


#%% Borrar tabla
# drop_table= "DROP TABLE IF EXISTS t_clientes;"
# p(drop_table)
# conn.commit()
#%%



############################################# INGRESO DE DATOS
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



############################################# STORED PROCEDURES
#%% Obtengo todas las Stored Procedures
show_procedures = """
    SELECT specific_name
    FROM information_schema.ROUTINES
    WHERE ROUTINE_TYPE = 'PROCEDURE' AND ROUTINE_SCHEMA = 'ddbb_test';
"""

# Ejecutar la consulta
p(show_procedures)
procedures = cursor.fetchall()
procedures = [x for subx in procedures for x in subx]
#%%


#%% Creacion de Stored Procedures para ingreso de datos
proc = 'InsertCliente'
if not proc in procedures:
    insert_client = f"""
        CREATE PROCEDURE {proc} (
            IN p_nombre VARCHAR(100),
            IN p_telefono VARCHAR(20),
            IN p_mail VARCHAR(100)
        )
        BEGIN
            INSERT INTO t_clientes (nombre, telefono, mail)
            VALUES (p_nombre, p_telefono, p_mail);
        END
    """
    p(insert_client)

proc = 'InsertFuncionario'
if not proc in procedures:
    insert_funcionario = f"""
        CREATE PROCEDURE {proc} (
            IN p_nombre VARCHAR(100),
            IN p_direccion VARCHAR(20),
            IN p_Fnacim date
        )
        BEGIN
            INSERT INTO t_funcionarios (nombre, direccion, Fnacim)
            VALUES (p_nombre, p_direccion, p_Fnacim);
        END
    """
    p(insert_funcionario)


proc = 'DeleteCliente'
if not proc in procedures:
    delete_cliente = f"""
        CREATE PROCEDURE {proc} (
            IN p_idCliente INT
        )
        BEGIN
            DELETE FROM t_clientes WHERE id_cliente = p_idCliente;
        END
    """
    p(delete_cliente)


proc = 'DeleteFuncionario'
if not proc in procedures:
    delete_funcionario = f"""
        CREATE PROCEDURE {proc} (
            IN p_idFuncionario INT
        )
        BEGIN
            DELETE FROM t_funcionarios WHERE id_funcionario = p_idFuncionario;
        END
    """
    p(delete_funcionario)

conn.commit()
#%%


#%% Insertar valores mediante Stored Procedure
# nombre = "Emilia Nuñez"
# telefono = "097-097097"
# mail = "mariaemilia@example.com"
# sp('InsertCliente', [nombre, telefono, mail])

# nombre = "Andres Ojeda"
# direccion = "Mercedes 985"
# fnacim = "1980-07-24"
# sp('InsertFuncionario', [nombre, direccion, fnacim])

# conn.commit()
#%%


#%% Eliminar valores mediante Stored Procedure
id_cliente = 1003
sp('DeleteCliente', [id_cliente])

id_funcionario = 103
sp('DeleteFuncionario', [id_funcionario])

conn.commit()
#%%


#%% Elimino Stored Procedure
# drop_procedure = "DROP PROCEDURE IF EXISTS InsertFuncionario;"
# cursor.execute(drop_procedure)
# conn.commit()
#%%


############################################# DESCONECTO
#%% Cierro conexion
conn.close()
#%%