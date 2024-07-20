from flask import Flask, jsonify, request, current_app
import sqlite3
import os
from contextlib import contextmanager

app = Flask(__name__)

palabras_comunes = [
    ("casa", 1), ("perro", 1), ("gato", 1), ("árbol", 1), ("libro", 1),
    ("mesa", 1), ("silla", 1), ("coche", 1), ("bicicleta", 2), ("teléfono", 1),
    ("computadora", 2), ("ventana", 1), ("puerta", 1), ("cocina", 1), ("dormitorio", 1),
    ("jardín", 1), ("escuela", 1), ("trabajo", 1), ("amigo", 1), ("familia", 1),
    ("comida", 1), ("agua", 1), ("aire", 1), ("fuego", 1), ("tierra", 1),
    ("sol", 1), ("luna", 1), ("estrella", 1), ("mar", 1), ("montaña", 1),
    ("río", 1), ("bosque", 1), ("ciudad", 1), ("país", 1), ("música", 1),
    ("arte", 2), ("deporte", 1), ("tiempo", 1), ("reloj", 1), ("dinero", 1),
    ("amor", 1), ("felicidad", 2), ("tristeza", 2), ("sueño", 1), ("realidad", 2),
    ("viaje", 1), ("aventura", 2), ("historia", 2), ("futuro", 2), ("presente", 2),
    ("color", 1), ("forma", 1), ("tamaño", 1), ("sabor", 1), ("olor", 1),
    ("sonido", 1), ("movimiento", 2), ("vida", 1), ("muerte", 2), ("juego", 1),
    ("película", 1), ("televisión", 1), ("radio", 1), ("internet", 2), ("teléfono", 1),
    ("ropa", 1), ("zapatos", 1), ("sombrero", 1), ("bolsa", 1), ("reloj", 1),
    ("anillo", 1), ("collar", 1), ("pulsera", 2), ("pendientes", 2), ("gafas", 1),
    ("camisa", 1), ("pantalón", 1), ("falda", 1), ("vestido", 1), ("abrigo", 1),
    ("calcetines", 1), ("zapatos", 1), ("botas", 1), ("sandalias", 2), ("pijama", 1),
    ("cama", 1), ("almohada", 1), ("sábana", 2), ("manta", 1), ("colchón", 2),
    ("armario", 1), ("espejo", 1), ("cepillo", 1), ("peine", 1), ("jabón", 1),
    ("champú", 2), ("toalla", 1), ("ducha", 1), ("bañera", 2), ("inodoro", 2),
    ("lavabo", 2), ("grifo", 2), ("agua", 1), ("caliente", 1), ("frío", 1),
    ("temperatura", 2), ("calor", 1), ("fresco", 1), ("viento", 1), ("lluvia", 1),
    ("nieve", 1), ("hielo", 1), ("tormenta", 2), ("rayo", 1), ("trueno", 2),
    ("nube", 1), ("cielo", 1), ("arcoíris", 2), ("sol", 1), ("luna", 1),
    ("estrella", 1), ("planeta", 2), ("universo", 2), ("espacio", 2), ("galaxia", 2),
    ("tierra", 1), ("continente", 2), ("océano", 1), ("isla", 1), ("playa", 1),
    ("arena", 1), ("roca", 1), ("montaña", 1), ("valle", 2), ("bosque", 1),
    ("selva", 2), ("desierto", 2), ("pradera", 2), ("campo", 1), ("granja", 1),
    ("animal", 1), ("planta", 1), ("flor", 1), ("árbol", 1), ("hoja", 1),
    ("raíz", 2), ("tallo", 2), ("semilla", 1), ("fruta", 1), ("verdura", 1),
    ("manzana", 1), ("naranja", 1), ("plátano", 1), ("uva", 1), ("fresa", 1),
    ("tomate", 1), ("lechuga", 1), ("zanahoria", 1), ("patata", 1), ("cebolla", 1),
    ("ajo", 1), ("arroz", 1), ("pan", 1), ("pasta", 1), ("carne", 1),
    ("pescado", 1), ("pollo", 1), ("huevo", 1), ("leche", 1), ("queso", 1),
    ("yogur", 2), ("mantequilla", 2), ("aceite", 1), ("sal", 1), ("azúcar", 1),
    ("café", 1), ("té", 1), ("jugo", 1), ("refresco", 2), ("cerveza", 1),
    ("vino", 1), ("agua", 1), ("hielo", 1), ("sopa", 1), ("ensalada", 1),
    ("postre", 2), ("helado", 1), ("pastel", 1), ("chocolate", 1), ("caramelo", 1),
    ("dulce", 1), ("salado", 1), ("amargo", 2), ("picante", 2), ("sabor", 1),
    ("olor", 1), ("aroma", 2), ("perfume", 2), ("cocina", 1), ("receta", 2),
    ("ingrediente", 2), ("mezclar", 2), ("cortar", 1), ("cocinar", 1), ("freír", 2),
    ("hervir", 2), ("hornear", 2), ("microondas", 2), ("nevera", 1), ("congelador", 2),
    ("plato", 1), ("vaso", 1), ("taza", 1), ("cuchara", 1), ("tenedor", 1),
    ("cuchillo", 1), ("servilleta", 2), ("mantel", 2), ("mesa", 1), ("silla", 1),
    ("sofá", 1), ("sillón", 2), ("cama", 1), ("escritorio", 2), ("estantería", 2),
    ("lámpara", 1), ("luz", 1), ("sombra", 1), ("oscuridad", 2), ("día", 1),
    ("noche", 1), ("mañana", 1), ("tarde", 1), ("hora", 1), ("minuto", 1),
    ("segundo", 1), ("semana", 1), ("mes", 1), ("año", 1), ("calendario", 2),
    ("cumpleaños", 1), ("fiesta", 1), ("celebración", 2), ("regalo", 1), ("sorpresa", 2),
    ("alegría", 2), ("risa", 1), ("sonrisa", 1), ("llanto", 2), ("tristeza", 2),
    ("enojo", 2), ("miedo", 1), ("valor", 2), ("coraje", 2), ("fuerza", 1),
    ("debilidad", 2), ("salud", 1), ("enfermedad", 2), ("dolor", 1), ("medicina", 2),
    ("hospital", 1), ("doctor", 1), ("enfermera", 2), ("paciente", 2), ("tratamiento", 2),
    ("cura", 2), ("vacuna", 2), ("inyección", 2), ("pastilla", 2), ("jarabe", 2),
    ("farmacia", 2), ("receta", 2), ("seguro", 2), ("emergencia", 2), ("ambulancia", 2),
    ("accidente", 2), ("herida", 2), ("sangre", 1), ("corazón", 1), ("cerebro", 2),
    ("pulmón", 2), ("estómago", 2), ("hígado", 2), ("riñón", 2), ("músculo", 2),
    ("hueso", 1), ("piel", 1), ("cabello", 1), ("uña", 1), ("diente", 1),
    ("lengua", 1), ("ojo", 1), ("nariz", 1), ("oreja", 1), ("boca", 1),
    ("cara", 1), ("cuello", 1), ("hombro", 2), ("brazo", 1), ("codo", 1),
    ("muñeca", 2), ("mano", 1), ("dedo", 1), ("pierna", 1), ("rodilla", 1),
    ("tobillo", 2), ("pie", 1), ("espalda", 1), ("pecho", 1), ("cintura", 2),
    ("cadera", 2), ("trasero", 2), ("cuerpo", 1), ("bebé", 1), ("niño", 1),
    ("adolescente", 2), ("adulto", 1), ("anciano", 2), ("hombre", 1), ("mujer", 1),
    ("padre", 1), ("madre", 1), ("hijo", 1), ("hija", 1), ("hermano", 1),
    ("hermana", 1), ("abuelo", 1), ("abuela", 1), ("tío", 1), ("tía", 1),
    ("primo", 1), ("prima", 1), ("sobrino", 2), ("sobrina", 2), ("nieto", 1),
    ("nieta", 1), ("esposo", 1), ("esposa", 1), ("novio", 1), ("novia", 1),
    ("amigo", 1), ("amiga", 1), ("compañero", 2), ("compañera", 2), ("vecino", 1),
    ("vecina", 1), ("jefe", 1), ("empleado", 2), ("cliente", 2), ("estudiante", 1),
    ("profesor", 1), ("maestro", 1), ("alumno", 1), ("clase", 1), ("escuela", 1),
    ("colegio", 1), ("universidad", 2), ("biblioteca", 2), ("libro", 1), ("cuaderno", 1),
    ("lápiz", 1), ("bolígrafo", 2), ("goma", 1), ("regla", 1), ("mochila", 1),
    ("pizarra", 2), ("tiza", 2), ("examen", 2), ("nota", 1), ("tarea", 1),
    ("estudio", 2), ("aprender", 2), ("enseñar", 2), ("leer", 1), ("escribir", 1),
    ("contar", 1), ("sumar", 1), ("restar", 1), ("multiplicar", 2), ("dividir", 2),
    ("número", 1), ("letra", 1), ("palabra", 1), ("frase", 2), ("oración", 2),
    ("párrafo", 2), ("texto", 1), ("historia", 1), ("cuento", 1), ("novela", 2),
    ("poesía", 2), ("autor", 2), ("escritor", 2), ("lector", 2), ("idioma", 2),
    ("lenguaje", 2), ("gramática", 2), ("vocabulario", 2), ("diccionario", 2), ("traducción", 2),
    ("hablar", 1), ("escuchar", 1), ("entender", 2), ("explicar", 2), ("preguntar", 1),
    ("responder", 2), ("conversación", 2), ("diálogo", 2), ("discusión", 2), ("debate", 2),
    ("argumento", 2), ("opinión", 2), ("idea", 1), ("pensamiento", 2), ("memoria", 2),
    ("imaginación", 2), ("creatividad", 2), ("arte", 1), ("música", 1), ("pintura", 1),
    ("escultura", 2), ("danza", 1), ("teatro", 2), ("cine", 1), ("fotografía", 2),
    ("cámara", 1), ("video", 1), ("película", 1), ("actor", 1), ("actriz", 2),
    ("director", 2), ("productor", 2), ("guión", 2), ("escena", 2), ("personaje", 2),
    ("público", 2), ("aplauso", 2), ("fama", 2), ("éxito", 2), ("fracaso", 2),
    ("premio", 1), ("trofeo", 2), ("medalla", 2), ("competencia", 2), ("juego", 1),
    ("deporte", 1), ("equipo", 1), ("jugador", 1), ("entrenador", 2), ("árbitro", 2),
    ("estadio", 2), ("cancha", 2), ("pelota", 1), ("balón", 1), ("red", 1),
    ("gol", 1), ("punto", 1), ("victoria", 2), ("derrota", 2), ("empate", 2),
    ("teclado", 1), ("ratón", 1), ("pantalla", 1), ("impresora", 2), ("escáner", 2),
    ("altavoz", 2), ("micrófono", 2), ("auriculares", 2), ("cable", 1), ("batería", 1),
    ("cargador", 1), ("tablet", 2), ("aplicación", 2), ("programa", 2), ("archivo", 2),
    ("carpeta", 1), ("documento", 2), ("imagen", 1), ("video", 1), ("audio", 2),
    ("red", 1), ("wifi", 2), ("contraseña", 2), ("usuario", 2), ("correo", 1),
    ("mensaje", 1), ("chat", 2), ("foro", 2), ("blog", 2), ("web", 2),
    ("enlace", 2), ("descarga", 2), ("subir", 1), ("bajar", 1), ("compartir", 2),
    ("buscar", 1), ("encontrar", 2), ("guardar", 1), ("borrar", 1), ("copiar", 1),
    ("pegar", 1), ("cortar", 1), ("seleccionar", 2), ("editar", 2), ("formato", 2),
    ("fuente", 2), ("tamaño", 1), ("color", 1), ("negrita", 2), ("cursiva", 2),
    ("subrayado", 2), ("alinear", 2), ("justificar", 2), ("lista", 1), ("tabla", 1),
    ("gráfico", 2), ("presentación", 2), ("diapositiva", 2), ("animación", 2), ("transición", 2),
    ("perfil", 2), ("cuenta", 1), ("amigo", 1), ("seguidor", 2), ("like", 2),
    ("comentario", 2), ("publicación", 2), ("estado", 2), ("actualización", 2), ("notificación", 2),
    ("etiqueta", 2), ("mención", 2), ("tendencia", 2), ("viral", 2), ("influencer", 2),
    ("meme", 2), ("emoji", 2), ("sticker", 2), ("gif", 2), ("streaming", 2),
    ("podcast", 2), ("canal", 1), ("suscriptor", 2), ("visualización", 2), ("monetización", 2),
    ("anuncio", 2), ("publicidad", 2), ("marca", 1), ("producto", 2), ("servicio", 2),
    ("cliente", 1), ("venta", 1), ("compra", 1), ("precio", 1), ("oferta", 1),
    ("descuento", 2), ("promoción", 2), ("cupón", 2), ("tarjeta", 1), ("efectivo", 2),
    ("banco", 1), ("cuenta", 1), ("ahorro", 2), ("préstamo", 2), ("hipoteca", 2),
    ("inversión", 2), ("bolsa", 1), ("acción", 2), ("dividendo", 2), ("interés", 2),
    ("impuesto", 2), ("declaración", 2), ("factura", 2), ("recibo", 2), ("gasto", 1),
    ("ingreso", 2), ("presupuesto", 2), ("economía", 2), ("mercado", 1), ("empresa", 1),
    ("negocio", 2), ("emprendedor", 2), ("startup", 2), ("innovación", 2), ("tecnología", 2),
    ("ciencia", 2), ("investigación", 2), ("desarrollo", 2), ("avance", 2), ("descubrimiento", 2),
    ("invento", 2), ("patente", 2), ("laboratorio", 2), ("experimento", 2), ("teoría", 2),
    ("hipótesis", 2), ("prueba", 1), ("resultado", 2), ("conclusión", 2), ("informe", 2),
    ("artículo", 2), ("revista", 1), ("periódico", 2), ("noticia", 1), ("reportaje", 2),
    ("entrevista", 2), ("periodista", 2), ("redactor", 2), ("editor", 2), ("columnista", 2),
    ("titular", 2), ("portada", 2), ("sección", 2), ("suplemento", 2), ("editorial", 2),
    ("opinión", 2), ("crítica", 2), ("reseña", 2), ("análisis", 2), ("comentario", 2),
    ("debate", 2), ("discusión", 2), ("argumento", 2), ("razonamiento", 2), ("lógica", 2),
    ("filosofía", 2), ("ética", 2), ("moral", 2), ("valor", 1), ("principio", 2),
    ("derecho", 2), ("ley", 1), ("norma", 2), ("regla", 1), ("constitución", 2),
    ("gobierno", 2), ("estado", 2), ("nación", 2), ("ciudadano", 2), ("sociedad", 2),
    ("cultura", 2), ("tradición", 2), ("costumbre", 2), ("hábito", 2), ("rutina", 2),
    ("horario", 2), ("agenda", 2), ("cita", 1), ("reunión", 2), ("entrevista", 2),
    ("conferencia", 2), ("seminario", 2), ("taller", 2), ("curso", 1), ("formación", 2),
    ("certificado", 2), ("diploma", 2), ("título", 1), ("grado", 2), ("máster", 2),
    ("doctorado", 2), ("tesis", 2), ("investigación", 2), ("proyecto", 2), ("propuesta", 2),
    ("plan", 1), ("estrategia", 2), ("objetivo", 2), ("meta", 2), ("logro", 2),
    ("éxito", 2), ("fracaso", 2), ("error", 1), ("problema", 1), ("solución", 2),
    ("decisión", 2), ("elección", 2), ("opción", 2), ("alternativa", 2), ("oportunidad", 2),
    ("riesgo", 2), ("desafío", 2), ("reto", 2), ("obstáculo", 2), ("dificultad", 2),
    ("crisis", 2), ("conflicto", 2), ("guerra", 1), ("paz", 1), ("acuerdo", 2),
    ("tratado", 2), ("alianza", 2), ("cooperación", 2), ("colaboración", 2), ("equipo", 1),
    ("grupo", 1), ("comunidad", 2), ("sociedad", 2), ("población", 2), ("demografía", 2),
    ("censo", 2), ("estadística", 2), ("promedio", 2), ("porcentaje", 2), ("tasa", 2),
    ("índice", 2), ("indicador", 2), ("medida", 1), ("peso", 1), ("altura", 1),
    ("distancia", 1), ("velocidad", 2), ("aceleración", 2), ("fuerza", 1), ("energía", 2),
    ("potencia", 2), ("electricidad", 2), ("corriente", 2), ("voltaje", 2), ("resistencia", 2),
    ("circuito", 2), ("motor", 1), ("máquina", 1), ("herramienta", 1), ("instrumento", 2),
    ("aparato", 2), ("dispositivo", 2), ("mecanismo", 2), ("sistema", 2), ("estructura", 2),
    ("construcción", 2), ("edificio", 1), ("casa", 1), ("apartamento", 2), ("oficina", 1),
    ("fábrica", 2), ("almacén", 2), ("tienda", 1), ("supermercado", 2), ("centro comercial", 2),
    ("restaurante", 1), ("cafetería", 2), ("bar", 1), ("discoteca", 2), ("cine", 1),
    ("teatro", 2), ("museo", 1), ("galería", 2), ("biblioteca", 2), ("gimnasio", 2),
    ("parque", 1), ("jardín", 1), ("plaza", 1), ("calle", 1), ("avenida", 2),
    ("carretera", 1), ("autopista", 2), ("puente", 1), ("túnel", 2), ("estación", 1),
    ("aeropuerto", 2), ("puerto", 2), ("frontera", 2), ("aduana", 2), ("pasaporte", 2),
    ("visa", 2), ("turista", 2), ("viajero", 2), ("mochilero", 2), ("guía", 1),
    ("mapa", 1), ("brújula", 2), ("GPS", 2), ("ruta", 1), ("destino", 2),
    ("origen", 2), ("ida", 2), ("vuelta", 1), ("escala", 2), ("conexión", 2),
    ("reserva", 2), ("check-in", 2), ("equipaje", 2), ("maleta", 1), ("bolso", 1),
    ("billete", 2), ("ticket", 2), ("boarding pass", 2), ("asiento", 1), ("ventanilla", 2),
    ("pasillo", 2), ("salida", 1), ("entrada", 1), ("llegada", 2), ("retraso", 2),
    ("cancelación", 2), ("emergencia", 2), ("seguridad", 2), ("control", 2), ("inspección", 2),
    ("detector", 2), ("escáner", 2), ("rayos X", 2), ("metal", 1), ("líquido", 2),
    ("sólido", 2), ("gas", 1), ("plasma", 2), ("átomo", 2), ("molécula", 2),
    ("célula", 2), ("tejido", 2), ("órgano", 2), ("sistema", 2), ("organismo", 2),
    ("especie", 2), ("género", 2), ("familia", 1), ("orden", 1), ("clase", 1),
    ("filo", 2), ("reino", 2), ("dominio", 2), ("evolución", 2), ("adaptación", 2),
    ("mutación", 2), ("selección", 2), ("supervivencia", 2), ("extinción", 2), ("fósil", 2),
    ("genética", 2), ("ADN", 2), ("cromosoma", 2), ("gen", 2), ("alelo", 2),
    ("fenotipo", 2), ("genotipo", 2), ("herencia", 2), ("rasgo", 2), ("característica", 2),
    ("variación", 2), ("diversidad", 2), ("biodiversidad", 2), ("ecosistema", 2), ("hábitat", 2),
    ("nicho", 2), ("cadena alimentaria", 2), ("depredador", 2), ("presa", 2), ("simbiosis", 2),
    ("parasitismo", 2), ("mutualismo", 2), ("comensalismo", 2), ("competencia", 2), ("cooperación", 2),
    ("equilibrio", 2), ("sostenibilidad", 2), ("conservación", 2), ("protección", 2), ("restauración", 2),
    ("contaminación", 2), ("residuo", 2), ("reciclaje", 2), ("reutilización", 2), ("reducción", 2),
    ("energía renovable", 2), ("solar", 1), ("eólica", 2), ("hidráulica", 2), ("geotérmica", 2),
    ("biomasa", 2), ("combustible", 2), ("fósil", 2), ("petróleo", 2), ("carbón", 1),
    ("gas natural", 2), ("nuclear", 2), ("fisión", 2), ("fusión", 2), ("radiación", 2),
    ("isótopo", 2), ("partícula", 2), ("onda", 2), ("frecuencia", 2), ("amplitud", 2),
    ("longitud", 2), ("espectro", 2), ("luz", 1), ("color", 1), ("sonido", 1),
    ("vibración", 2), ("resonancia", 2), ("acústica", 2), ("óptica", 2), ("lente", 2),
    ("prisma", 2), ("reflexión", 2), ("refracción", 2), ("difracción", 2), ("interferencia", 2),
    ("polarización", 2), ("magnetismo", 2), ("electricidad", 2), ("carga", 2), ("campo", 1),
    ("fuerza", 1), ("gravedad", 2), ("aceleración", 2), ("velocidad", 2), ("movimiento", 1),
    ("reposo", 2), ("inercia", 2), ("fricción", 2), ("resistencia", 2), ("presión", 2),
    ("densidad", 2), ("volumen", 2), ("masa", 2), ("peso", 1), ("temperatura", 1),
    ("calor", 1), ("frío", 1), ("congelación", 2), ("ebullición", 2), ("evaporación", 2),
    ("condensación", 2), ("sublimación", 2), ("fusión", 2), ("solidificación", 2), ("cristalización", 2)
]


@contextmanager
def get_db_connection():
    conn = None
    try:
        if os.environ.get('RENDER'):
            conn = sqlite3.connect(':memory:', check_same_thread=False)
        else:
            conn = sqlite3.connect('palabras_juego.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()


def init_db():
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS palabras (
                    palabra TEXT PRIMARY KEY,
                    dificultad INTEGER
                )
            ''')
            conn.executemany('INSERT OR REPLACE INTO palabras (palabra, dificultad) VALUES (?, ?)',
                             palabras_comunes)
            conn.commit()
        current_app.logger.info("Table 'palabras' created and populated successfully.")
    except Exception as e:
        current_app.logger.error(f"Error initializing database: {e}")


# Initialize the database when the app is created
with app.app_context():
    init_db()


@app.route('/')
def home():
    return "API de palabras está funcionando"


@app.route('/palabras', methods=['GET'])
def obtener_todas_las_palabras():
    try:
        with get_db_connection() as conn:
            palabras = conn.execute('SELECT palabra, dificultad FROM palabras').fetchall()
        return jsonify([{'palabra': row['palabra'], 'dificultad': row['dificultad']} for row in palabras])
    except Exception as e:
        current_app.logger.error(f"Error fetching words: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/palabra/aleatoria', methods=['GET'])
def obtener_palabra_aleatoria():
    try:
        dificultad = request.args.get('dificultad', type=int)
        with get_db_connection() as conn:
            if dificultad:
                palabra = conn.execute(
                    'SELECT palabra, dificultad FROM palabras WHERE dificultad = ? ORDER BY RANDOM() LIMIT 1',
                    (dificultad,)).fetchone()
            else:
                palabra = conn.execute('SELECT palabra, dificultad FROM palabras ORDER BY RANDOM() LIMIT 1').fetchone()
        if palabra:
            return jsonify({'palabra': palabra['palabra'], 'dificultad': palabra['dificultad']})
        return jsonify({'error': 'No se encontraron palabras'}), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching random word: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/palabras/dificultad/<int:dificultad>', methods=['GET'])
def obtener_palabras_por_dificultad(dificultad):
    try:
        cantidad = request.args.get('cantidad', default=10, type=int)
        with get_db_connection() as conn:
            palabras = conn.execute(
                'SELECT palabra, dificultad FROM palabras WHERE dificultad = ? ORDER BY RANDOM() LIMIT ?',
                (dificultad, cantidad)).fetchall()
        return jsonify([{'palabra': row['palabra'], 'dificultad': row['dificultad']} for row in palabras])
    except Exception as e:
        current_app.logger.error(f"Error fetching words by difficulty: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/palabras/contar', methods=['GET'])
def contar_palabras():
    try:
        with get_db_connection() as conn:
            count = conn.execute('SELECT COUNT(*) FROM palabras').fetchone()[0]
        return jsonify({'total_palabras': count})
    except Exception as e:
        current_app.logger.error(f"Error counting words: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/palabras', methods=['POST'])
def agregar_palabra():
    try:
        datos = request.json
        if not datos or 'palabra' not in datos or 'dificultad' not in datos:
            return jsonify({'error': 'Se requiere palabra y dificultad'}), 400

        with get_db_connection() as conn:
            conn.execute('INSERT INTO palabras (palabra, dificultad) VALUES (?, ?)',
                         (datos['palabra'], datos['dificultad']))
            conn.commit()
        return jsonify({'mensaje': 'Palabra agregada exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'La palabra ya existe en la base de datos'}), 409
    except Exception as e:
        current_app.logger.error(f"Error adding word: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/debug/db_status')
def db_status():
    try:
        with get_db_connection() as conn:
            count = conn.execute('SELECT COUNT(*) FROM palabras').fetchone()[0]
        return jsonify({'status': 'ok', 'word_count': count})
    except Exception as e:
        current_app.logger.error(f"Error checking database status: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
