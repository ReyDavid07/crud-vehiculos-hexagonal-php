# CRUD Hexagonal PHP + MySQL

Proyecto base alineado con las guías del curso:
- Arquitectura hexagonal
- DDD
- CQRS
- CRUD de usuarios
- Login
- Recuperación de contraseña por correo
- CRUDL de vehículos

## Instalación
1. Importa `database.sql` en MySQL.
2. Ajusta `config/database.php`.
3. Sirve la carpeta del proyecto en Apache/Laragon/XAMPP.
4. Abre `public/index.php`.

## Credenciales de prueba
- Correo: `admin@demo.com`
- Contraseña: `Admin123*`

## Ramas sugeridas
- feature/guia-crud-usuarios
- feature/login
- feature/recuperacion-password
- feature/crudl-vehiculo
- docs/pdf-entrega


## Modulo Vehiculos
Se implemento CRUDL de vehiculos con persistencia en MySQL.
=======
## Recuperacion de contrasena
Se implemento recuperacion de contrasena mediante correo y contrasena temporal.
=======
## Modulo Login
Se implemento inicio de sesion con validacion de credenciales y sesiones PHP.
=======
## Modulo Usuarios
Se implemento CRUD de usuarios siguiendo la guia y arquitectura hexagonal.



