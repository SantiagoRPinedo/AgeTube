instructions =[
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS usuario;',
    'DROP TABLE IF EXISTS publicaciones;',
    'DROP TABLE IF EXISTS comunidad;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE usuario (
            id          INT PRIMARY KEY AUTO_INCREMENT,
            nombre      VARCHAR (50) NOT NULL,
            apellidos   VARCHAR(50) NOT NULL,
            correo      VARCHAR(100) NOT NULL,
            cont        VARCHAR(250) NOT NULL,
            genero      VARCHAR(20) NOT NULL,
            legal       TINYINT(1) NOT NULL DEFAULT 0,
            dia         INT NOT NULL,
            mes         INT NOT NULL,
            anio        INT NOT NULL,
            username    VARCHAR(30) NOT NULL
        );
        CREATE TABLE publicaciones(
            titulo      VARCHAR(100)NOT NULL,
            contenido   VARCHAR(500)NOT NULL,
            legal       TINYINT(1) NOT NULL DEFAULT 0,
            username    VARCHAR(100) NOT NULL,
            tipo        VARCHAR(25) NOT NULL
        );
        CREATE TABLE comunidad(
            nombre      VARCHAR(50) NOT NULL,
            descripcion VARCHAR(250),
            urlimg      VARCHAR(250)
        );
    """
    ]