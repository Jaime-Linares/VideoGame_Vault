# 🎮👾 VideoGame_Vault 👾🎮

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-darkblue" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.1.1-green" alt="Django">
  <img src="https://img.shields.io/badge/BeautifulSoup-4.12.3-orange" alt="BeautifulSoup">
  <img src="https://img.shields.io/badge/Whoosh-2.7.4-yellow" alt="Whoosh">
  <img src="https://img.shields.io/badge/NumPy-2.0.0-teal" alt="NumPy">
  <img src="https://img.shields.io/badge/scikit--learn-1.5.1-blue" alt="scikit-learn">
  <img src="https://img.shields.io/badge/spaCy-3.8.3-purple" alt="spaCy">
  <img src="https://img.shields.io/badge/langdetect-1.0.9-red" alt="Langdetect">
  <img src="https://img.shields.io/badge/license-MIT-red" alt="License">
</p>

- [Descripción de la aplicación](#descripción-de-la-aplicación)
- [Pasos para iniciar el proyecto](#pasos-para-iniciar-el-proyecto)
- [Licencia](#licencia)


## Descripción de la aplicación
**Video Game Vault** es una aplicación web desarrollada con **Django** que centraliza información sobre videojuegos obtenida mediante *web scraping*. La plataforma permite explorar videojuegos, realizar búsquedas avanzadas y descubrir recomendaciones personalizadas, combinando simplicidad y potencia en un solo lugar.

**Propósito:** VideoGame Vault nació como una herramienta para centralizar información sobre videojuegos y facilitar su búsqueda y descubrimiento, ideal para gamers y coleccionistas.

### Características principales:
- **Obtención de datos:**
  - Los videojuegos se recopilan automáticamente desde [**Instant Gaming**](https://www.instant-gaming.com/) y [**Eneba**](https://www.eneba.com/) utilizando **Beautiful Soup**.
  - Los datos se almacenan en una base de datos y se organizan para realizar diferentes búsquedas.

- **Búsquedas:**
  - **Búsquedas sencillas:** Directamente con Django, explora videojuegos por filtros básicos como género, desarrollador, plataforma...
  - **Búsquedas avanzadas:** Utiliza **Whoosh** para consultas más complejas, como coincidencias específicas de palabras clave.

- **Autenticación para funcionalidades avanzadas:**
  - Algunas funcionalidades, como la carga de datos y del sistema de recomendación o las búsquedas avanzadas, están disponibles únicamente para usuarios autenticados.

- **Visualización detallada de videojuegos:**
  - Consulta detalles como fecha de lanzamiento, descripción, precio, descuento, puntuación, desarrollador, géneros y plataformas.
  - Descubre recomendaciones personalizadas basadas en similitudes con otros videojuegos.

- **Sistema de recomendación basado en contenido:**
  - Basado en contenido, utiliza vectores que combinan atributos de los videojuegos.
  - Implementado con herramientas como **spaCy** para procesar texto en lenguaje natural, **scikit-learn** para cálculos de similitud y **NumPy** para la construcción de los vectores.

### Tecnologías utilizadas:
- **Django:** Framework principal para el desarrollo de la aplicación.
- **Beautiful Soup:** Para la extracción de datos mediante *web scraping*.
- **Whoosh:** Motor de búsqueda para consultas avanzadas.
- **spaCy, scikit-learn y NumPy:** Componentes clave para el sistema de recomendación basado en contenido.


## Pasos para iniciar el proyecto
### Clonamos el proyecto
```bash
git clone https://github.com/Jaime-Linares/VideoGame_Vault.git
```

### Instalación de dependencias
Para ejecutar correctamente este proyecto, es necesario instalar las siguientes dependencias:

* **Instalamos Django:**
```bash
pip install django==5.1.1
``` 
* **Instalamos beautifulsoup y un parser:**
```bash
pip install beautifulsoup4==4.12.3
```
```bash
pip install lxml
```
* **Instalamos Whoosh:**
```bash
pip install whoosh==2.7.4
```
* **Instalamos NumPy:**
```bash
pip install numpy==2.0.0
```
* **Instalamos scikit-learn:**
```bash
pip install scikit-learn==1.5.1
```
* **Instalamos spaCy y los modelos que vamos a usar:**
```bash
pip install spacy==3.8.3
```
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0.tar.gz
```
```bash
pip install https://github.com/explosion/spacy-models/releases/download/es_core_news_md-3.8.0/es_core_news_md-3.8.0.tar.gz
```
* **Instalamos langedetect:**
```bash
pip install langdetect==1.0.9
```

### Ejecutamos las migraciones
```bash
python manage.py migrate
```

### Arrancamos el proyecto
```bash
python manage.py runserver
```
* Tendrás la aplicación desplegada en [http://localhost:8000/](http://localhost:8000/)

### Recomendaciones
Antes de nada, te recomiendo crearte una cuenta, para que puedas cargar la base de datos y el índice de Whoosh, poder cargar el sistema de recomendación y poder realizar las búsquedas avanzadas con Whoosh.

### Vista de la aplicación
* Aplicación recien abierta:

![Pantalla inicial](static/img/home-without-login.png) 

* Aplicación tras registrarse y cargas los datos y el sistema de recomendación:

![Pantalla inicial](static/img/home-register-load.png) 



## Licencia  
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.