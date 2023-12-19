import cv2
import numpy as np


def video_to_bits(video_file, width, height, fps):
    cap = cv2.VideoCapture(video_file)
    bits = ''
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % fps == 0:  # Verarbeite nur das erste Frame jeder Sekunde
            for i in range(height):
                for j in range(width):
                    pixel = frame[i, j]
                    bits += '1' if np.all(pixel == 0) else '0'
        frame_count += 1
    cap.release()
    return bits


def bits_to_file(bits, output_file):
    with open(output_file, 'wb') as file:
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            byte = int(byte, 2)
            file.write(byte.to_bytes(1, byteorder='big'))


video_file = 'output_video.mp4'  # Pfad zum Video
output_file = 'output_file.txt'  # Ausgabedatei
fps = 25  # Bildrate des Videos

bits = video_to_bits(video_file, 1920, 1080, fps)
bits_to_file(bits, output_file)
