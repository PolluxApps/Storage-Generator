import cv2
import numpy as np


def file_to_bits(file_path):
    bits = ''
    with open(file_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            bits += format(ord(byte), '08b')
            byte = file.read(1)
    return bits


def create_image_from_bits(bits, width, height):
    if len(bits) < width * height:
        bits += '0' * (width * height - len(bits))
    image = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            bit = bits[i * width + j]
            image[i, j] = 0 if bit == '1' else 255
    return image


def create_video_from_bits(bits, width, height, video_file, frame_rate, scale_factor):
    # Neue Frame-Größe berechnen
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)

    # Anzahl der Frames anpassen
    scaled_frame_count = round(len(bits) / (scaled_width * scaled_height) + 0.5)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_file, fourcc, frame_rate, (width, height), False)

    total_bits = scaled_width * scaled_height * scaled_frame_count
    for i in range(0, total_bits, scaled_width * scaled_height):
        frame_bits = bits[i:i + scaled_width * scaled_height]
        frame = create_image_from_bits(frame_bits, scaled_width, scaled_height)

        # Skalieren Sie das Frame zurück auf die ursprüngliche Größe
        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)

        video_writer.write(resized_frame)
    video_writer.release()


# Convert file to bits
file_path = 'file.txt'
bits = file_to_bits(file_path)

# Parameters for video
width, height = 1920, 1080
frame_rate = 25  # Frames per second, adjust as needed
# Calculate
frame_count = round(len(bits) / (width * height) + 0.5)  # Number of frames to generate, adjust as needed

print(frame_count)

# Create the video
video_file = 'output_video.mp4'
create_video_from_bits(bits, width, height, video_file, frame_rate, 0.25)
