# 🎮👾 VideoGame_Vault 👾🎮

**Video Game Vault** es una aplicación web desarrollada con **Django** que centraliza información sobre videojuegos obtenida mediante *web scraping*. La plataforma permite explorar videojuegos, realizar búsquedas avanzadas y descubrir recomendaciones personalizadas, combinando simplicidad y potencia en un solo lugar.

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

