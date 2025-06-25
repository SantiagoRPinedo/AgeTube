import functools
from flask import(
    Blueprint,flash, g, render_template, request, url_for, session,Response,jsonify,redirect
)
from werkzeug.security import check_password_hash,generate_password_hash
from . import db
import yagmail
import random


def validac(p,c):
    if (p == c):
        return True
    else:
        return False

def validaEdad (det,ed):
    ed = int(ed)
    det = int(det)
    if (det >= 18 and ed >= 18):
            return True
    elif(det < 18 and ed < 18):
            return True
    else:
        return False

def legalidad(edad):
     if (edad >= 18):
          return 1 # en caso de que ya sea legal
     else:
          return  0

bp = Blueprint('index',__name__,url_prefix='/')

@bp.route('/',methods = ['GET', 'POST'])
def index():
    base , c = db.get_db()
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        cons = "select * from asso.usuario where correo = %s" 
        c.execute(cons, (correo,))
        
        usuario = c.fetchone()        

        if usuario:
            legal = usuario['legal']
            if check_password_hash(usuario['cont'],password):
                session['usr'] = usuario['nombre'] + usuario['apellidos']
                session['legal'] = legal
                session['correo'] = usuario['correo']
                session['username'] = usuario['username']
                print (session['legal'] )
                print(session['correo'])
                return redirect("/muro")
            else:
                no = 'NO'
                flash(no)
                print('No')
                pass
        else:
            pass 
    
    return render_template("index.html")

@bp.route('/salir', methods=['GET','POST'])
def salir():
    session.clear()
    print("la session se a cerrado")
    return redirect("/")

@bp.route('/registro',methods = ['GET', 'POST'])
def registro():
    base , c = db.get_db()

    global nombre
    global apellido 
    global correo 
    global password
    global legal
    global dia 
    global mes 
    global anio
    global genero
    global Username 

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        Username =request.form['Username']
        password = request.form['password']
        confirma = request.form['confirma']
        determinada = request.form['determinada']
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        anio = request.form.get('anio')
        genero = request.form.get('genero')
        anio = int(anio)
        edad = 2023 - anio
        coincide = validaEdad (determinada,edad)
        errors = []

        legal = legalidad(edad) #Para determinar si es legal o no y guardar ese valor en la base de datos

        if not genero:
            errors.append('Selecciona un genero por favor unu')

        igual = validac(password,confirma)
        
        if (coincide == False):
            errors.append("La fecha de nacimiento no corresponde con la edad determinada")

        if (igual == False):
            errors.append('Las contraseñas no coinciden')

        if (igual and len(errors)==0):
            correoCodigo(correo)
            return (redirect('verificacion'))
        else:
            for e in errors:
                flash(e)
    return (render_template("registro.html"))


@bp.route('/muro',methods = ['GET', 'POST'])
def Muro():
    global session
    legal = session['legal'] #Se recupera el parametro legal de la sesion
    base , c = db.get_db()
    print (legal)
    if (legal == 0):
        cons = "select * from asso.publicaciones where legal = %s ;"# se recuperan las publicaciones segun el parametro legal
        c.execute(cons, (legal,))
        publicaciones = c.fetchall()   
    else:
        cons = "select * from asso.publicaciones;"# se recuperan todas las publicaciones
        c.execute(cons)
        publicaciones = c.fetchall()   

    if request.method == 'POST':
        titulo= request.form['titulo']
        contenido = request.form['contenido']
        ilegal= request.form.get('ilegal') # el valor de checkbox_value será 'on' si el checkbox está marcado, o None si no lo está
        tipo = request.form['tipo']
        username = session['username']
    
        if ilegal == "on":
            ilegal = 1
        else:
            ilegal=0
        if ((legal==1 and ilegal == 1) or (legal==1 and ilegal ==0)):#si es mayor de edad y el usuario es mayor de edad
            c.execute("INSERT INTO publicaciones (titulo,contenido,legal,username,tipo) VALUES (%s,%s,%s,%s,%s)",(titulo,contenido,ilegal,username,tipo))
            base.commit()
            cons = "select * from asso.publicaciones;"
            c.execute(cons)
            publicaciones = c.fetchall() 
        elif (legal==0 and ilegal == 0): #si es un menor de edad publicando segun su edad
            c.execute("INSERT INTO publicaciones (titulo,contenido,legal,username,tipo) VALUES (%s,%s,%s,%s,%s)",(titulo,contenido,ilegal,username,tipo))
            base.commit()
            cons = "select * from asso.publicaciones where legal = %s ;"
            c.execute(cons, (legal,))
            publicaciones = c.fetchall() 
        else:#si es un menor de edad publicando marranadas
            exito = "Un usuario menor de edad no puede publicar contenido +18"
            flash(exito)
            cons = "select * from asso.publicaciones where legal = %s ;"
            c.execute(cons, (legal,))
            publicaciones = c.fetchall()   
    
    return (render_template("Muro.html", publicaciones=publicaciones))


@bp.route('/perfil', methods = ['GET', 'POST'])
def perfil():
    global session
    legal = session['username'] #Se recupera el parametro legal de la sesion
    base , c = db.get_db()
    print (legal)
    if request.method == 'GET':
        cons = "select * from asso.publicaciones where username = %s ;"# se recuperan las publicaciones segun el parametro legal
        c.execute(cons, (legal,))
        publicaciones = c.fetchall()   
    return (render_template("perfil.html", publicaciones=publicaciones))

@bp.route('/comunidad',methods = ['GET', 'POST'])
def comunidad():
    base , c = db.get_db()
    if request.method =='GET':
        cons = "select * from asso.comunidad;"
        c.execute(cons)
        comunidades = c.fetchall() 
        return (render_template("comunidad.html", comunidades=comunidades))
    if request.method =='POST':
        nombre= request.form['nombre']
        descripcion = request.form['descripcion']
        urlimagen= request.form['urlimagen']
        c.execute("INSERT INTO comunidad (nombre,descripcion,urlimg) VALUES (%s,%s,%s)",(nombre,descripcion,urlimagen))
        base.commit()
        cons = "select * from asso.comunidad;"
        c.execute(cons)
        comunidades = c.fetchall() 
        return (render_template("comunidad.html", comunidades=comunidades))

# correo
def codigoVerificacion():
    global codigo
    # numero random
    codigo = random.randint(100000, 999999)
    # formato con cinco 0's 
    for_cod = '{:06d}'.format(codigo)
    return for_cod


def correoCodigo(correo):
    global codigo
    # datos emisor
    sender = "agetube23@gmail.com"
    psswrd = "whskrirfzuiaeqfc"
    yag = yagmail.SMTP(user=sender, password=psswrd)
    # datos receptor
    receiver = correo
    # asunto correo
    subject = "Código de verificación"
    # contenido correo
    codigo = codigoVerificacion()
    message = "Tu código de verificación es: " + codigo
    # enviar correo
    yag.send(receiver, subject, message)
    

@bp.route('/verificacion',methods = ['GET','POST'])
def validaCodigo():
    base, c = db.get_db()
    errors = []
    global codigo
    global password
    if request.method == 'POST':
        codigoUs = request.form['veri']
        codigosUs = int(codigoUs)
        if (codigo == codigoUs):
            #registrar usuario en en DB
            password = generate_password_hash(password)#generar la clave hash de la contraseña
            c.execute("INSERT INTO usuario (nombre,apellidos,correo,cont,genero,legal,dia,mes,anio,username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nombre,apellido,correo,password,genero,legal,dia,mes, anio,Username))            
            base.commit()
            exito = ("BIENVENIDO!! Has sido registrado correctamente C:")
            flash(exito)
            return redirect("/redmuro")
        else:
            errors.append('El codigo es invalido')
        
        for e in errors:
            flash(e)

    return (render_template("verificacion.html"))

@bp.route('/redmuro', methods=['GET', 'POST'])
def redMuro():
    base , c = db.get_db()
    global session
    global correo
    global password

    cons = "select * from asso.usuario where correo = %s" 
    c.execute(cons, (correo,))
    
    usuario = c.fetchone()       

    if usuario:
        legal = usuario['legal']
        if (usuario['cont'] == password):
            session['usr'] = usuario['nombre'] + usuario['apellidos']
            session['legal'] = legal
            session['correo'] = usuario['correo']
            session['username'] = usuario['username']
            return redirect("/muro")
        else:
            no = 'Credenciales incorrectas'
            flash(no)
            print('No')
            pass 
    
    return render_template("index.html")