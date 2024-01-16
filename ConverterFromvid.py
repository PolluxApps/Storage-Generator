import cv2
import numpy as np


def bits_to_file(video_file, output_file_path, width, height, scale_factor):
    # Video öffnen
    video_reader = cv2.VideoCapture(video_file)

    # Bits initialisieren
    bits = ''

    while video_reader.isOpened():
        ret, frame = video_reader.read()
        if not ret:
            break

        # Frame in Graustufen konvertieren und skalieren
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (int(width * scale_factor), int(height * scale_factor)),
                                   interpolation=cv2.INTER_NEAREST)

        # Bits aus dem Frame extrahieren
        for i in range(resized_frame.shape[0]):
            for j in range(resized_frame.shape[1]):
                pixel_value = resized_frame[i, j]
                bits += '1' if pixel_value < 128 else '0'

                print(bits)

    video_reader.release()

    # Bits in eine Datei schreiben
    with open(output_file_path, 'wb') as file:
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            file.write(bytes([int(byte, 2)]))


# Beispielaufruf der Funktion
video_file = 'output_video.mp4'
output_file_path = 'reconstructed_file.txt'
width, height = 1920, 1080
scale_factor = 0.005 # Stellen Sie sicher, dass dies der gleiche Skalierungsfaktor ist, der zum Erstellen des Videos verwendet wurde
bits_to_file(video_file, output_file_path, width, height, scale_factor)
