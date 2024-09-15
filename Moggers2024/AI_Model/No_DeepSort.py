import cv2
from ultralytics import YOLO

# Inicializar el modelo YOLOv8
model = YOLO('ModelSecurity.pt')

# Verificar que el modelo esté cargado correctamente
print("Clases del modelo:", model.names)

# Definir las clases de interés
CLASSES_OF_INTEREST = {0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}

# Conectar a la cámara (puedes cambiar el número si tienes múltiples cámaras conectadas)
cap = cv2.VideoCapture(0)

# Configurar la resolución opcionalmente (baja resolución para mayor velocidad)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 920)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el frame")
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

    # Mostrar el frame con las detecciones
    cv2.imshow('Webcam Feed - PPE Detection', frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpiar
cap.release()
cv2.destroyAllWindows()
