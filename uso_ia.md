Explica las instrucciones del archivo adjunto // Explica a detalle y dame los comandos necesarios para la "Etapa 0" //
Recomienda un "Prompt" para cumplir con las siguientes características: ...... Según el archivo.
 
Actúa como un desarrollador backend generando datos de prueba. Necesito que crees un arreglo JSON válido con exactamente 40 objetos que representen el catálogo de una ferretería.
Cada objeto debe contener obligatoriamente los siguientes campos:  id: un número entero secuencial del 1 al 40.nombre: el nombre del producto (sé variado y realista).categoria: la clasificación del artículo (ej. Herramientas manuales, Fijaciones).precio: un número entero positivo en pesos chilenos.stock: un número entero entre 0 y 50. Es fundamental que al menos 5 productos tengan el stock en "0" para poder probar la lógica condicional visual de la interfaz.
Devuelve únicamente el arreglo JSON, sin explicaciones adicionales ni bloques de texto.


"Actúa como un desarrollador front end experto en Django. Necesito diseñar la interfaz para un catálogo web de una ferretería utilizando Django Template Language (DTL).

Requisitos técnicos y de diseño:
1. Genera dos archivos:
   - 'base.html': Plantilla base que incluya un encabezado con el nombre de la ferretería, barra de navegación simple, bloque {% block content %} y un pie de página. Usa Bootstrap 5 vía CDN para los estilos.
   - 'lista.html': Plantilla que herede de 'base.html'. Debe mostrar una cuadrícula responsiva (cards) que itere una lista de objetos 'productos' usando un bucle {% for producto in productos %}.
2. Cada tarjeta de producto debe mostrar:
   - Nombre del producto
   - Categoría
   - Precio formateado
   - Stock disponible
   - Un botón o enlace que apunte a la vista de detalle: {% url 'detalle' producto.id %}
3. Entrega el código HTML limpio, semántico y listo para copiar en la carpeta de templates."



"Actúa como un desarrollador Front End Senior. Necesito estructurar y añadir nuevas funcionalidades visuales a la Landing Page (plantillas base.html y lista.html) de un proyecto académico en Django. El sitio es un catálogo online para una ferretería enfocada en materiales técnicos e infraestructura.

Necesito que me generes el código HTML semántico y el CSS puro (sin frameworks como Bootstrap) considerando los siguientes requerimientos:

Nuevas Funciones en la Interfaz:

Diseña una 'Barra de Búsqueda' simulada en el encabezado (header).

Crea una barra lateral (aside) o sección superior de 'Filtros Rápidos' utilizando botones o etiquetas (ej. Herramientas Manuales, Diseño Estructural de Pavimentos, Insumos para Refuerzo de Taludes, Mezclas Asfálticas).

Añade un pie de página (footer) con enlaces de contacto y un diseño corporativo.

Estructura HTML y CSS:

Utiliza CSS Grid para organizar el listado de productos de forma fluida.

Utiliza Flexbox para el encabezado y la alineación de los filtros.

La paleta de colores debe ser profesional e industrial: tonos grises asfalto, blanco para lectura clara y un color de acento de alta visibilidad (como naranja o amarillo de seguridad).

Todo el CSS debe estar debidamente comentado y ordenado por secciones (Variables, Globales, Layout, Componentes).

Integración con Django:

El código debe respetar la sintaxis de herencia de templates ({% block content %}, {% extends %}).

Por favor, entrégame el código de base.html y lista.html por separado, y explica brevemente cómo esta estructura mejora la mantenibilidad del proyecto."



"Actúa como un desarrollador experto en Django y frontend. Estoy construyendo la Etapa 3 de un catálogo web de ferretería. La restricción técnica principal es que no puedo usar modelos ni conexión a base de datos; todos los productos se procesan desde un archivo productos.json leído en views.py.

Necesito que me entregues el código de las vistas (views.py) y los templates (HTML/JS) para simular las siguientes cuatro funcionalidades sin romper la restricción de la base de datos:

Imágenes: Modifica la estructura de mi JSON actual para incluir un campo imagen_url con enlaces a imágenes de placeholder gratuitas enfocadas en materiales de construcción, herramientas o infraestructura vial. Actualiza el template para renderizarlas.

Filtro Dinámico: Crea un script en JavaScript puro para lista.html que permita filtrar en tiempo real las tarjetas de productos por categoria y por rango de precio, ocultando los elementos del DOM dinámicamente sin recargar la página ni hacer consultas al backend.

Simulación de Compra: Diseña un botón de 'Añadir al carro' en la vista de detalle. Al hacer clic, utiliza la API de localStorage de JavaScript para guardar temporalmente los productos seleccionados y muestra un modal confirmando la reserva del pedido, simulando el proceso de forma estática.

Panel de Administración (Mockup): Crea una ruta, una vista y un template llamado admin_landing.html. Debe lucir como un panel de control con un formulario HTML que simule la edición del título de la página principal. Al enviar el formulario mediante POST, la vista debe simplemente retornar un mensaje de éxito usando el framework messages de Django, sin guardar nada en disco."