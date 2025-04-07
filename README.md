# 📚 Library Management System

Este proyecto es un sistema de gestión de biblioteca desarrollado con **Python 3** y **Django**. Permite administrar libros, usuarios y préstamos, integrando estructuras de datos lineales (listas, pilas, colas y arreglos) para el manejo interno de la lógica del sistema.

---

## 🔧 Tecnologías utilizadas

- Python 3.x  
- Django 4.x  
- SQLite (por defecto)  
- HTML/CSS (para el frontend)  
- Estructuras de datos lineales implementadas manualmente

---

## ⚙️ Funcionalidades principales

- 📘 CRUD de libros (Crear, Leer, Actualizar)  
- 👥 Registro y administración de usuarios  
- 📥 Préstamos y devoluciones de libros  
- 🔄 Registro de historial de préstamos con colas y pilas  
---

## 📁 Estructura del proyecto
## Crear Entorno Virtual e Instalar Django

```python
  python -m venv env
  source env/bin/activate  # En Windows: env\Scripts\activate
  pip install django
```

## aplicar migraciones

```python
  python manage.py makemigrations
  python manage.py migrate
```
##  Crear superusuario
```python
  python manage.py createsuperuser
```
## Ejecutar el Servidor
```python
  python manage.py runserver
```

## Estructura de Datos 
En el folder library_management se encuentra un archivo llamado data_structures.py donde se encuentran todos los tipos de estructuras.
