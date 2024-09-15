import cv2
from flask import Flask, render_template, Response
from ultralytics import YOLO

app = Flask(__name__)

# Inicializar el modelo YOLOv8
model = YOLO('Internet.pt')

# Definir las clases de interés
CLASSES_OF_INTEREST = {0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}

# Definir el puerto de la cámara (webcam_source)
webcam_source = 0  # Cambia esto si usas otro puerto para la cámara

# Función para capturar frames de la cámara y aplicar el modelo YOLO
def gen_frames():
    cap = cv2.VideoCapture(webcam_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 920)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Realizar la detección con YOLO en el frame actual
        results = model(frame, verbose=False)  # Ejecutar sin detalles adicionales para optimizar

        # Procesar las detecciones de YOLO
        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy.cpu().numpy()[0])  # Bounding box en formato x1, y1, x2, y2
            confidence = result.conf.cpu().numpy()[0]  # Obtener la puntuación de confianza
            class_label = int(result.cls.cpu().numpy()[0])  # Obtener el índice de la clase

            # Dibujar solo las clases de interés
            if class_label in CLASSES_OF_INTEREST:
                label = CLASSES_OF_INTEREST[class_label]  # Obtener el nombre de la etiqueta
                color = (0, 255, 0) if label in ['Hardhat', 'Mask', 'Safety Vest'] else (0, 0, 255)

                if label == "Person":
                    color = (255, 255, 255)  # Color blanco para personas

                # Dibujar el cuadro y la etiqueta
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Codificar el frame como JPEG para enviar a la web
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Devolver el frame en formato de flujo de video
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Ruta principal para renderizar la página HTML

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('home.html')

# Ruta para 'Proyecto.html'
@app.route('/proyecto')
def proyecto():
    return render_template('Proyecto.html')

# Ruta para servir el video en streaming
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')