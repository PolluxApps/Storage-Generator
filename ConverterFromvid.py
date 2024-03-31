import cv2

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

        counter = 0
        blank_counter = 0

        # Bits aus dem Frame extrahieren
        breaker = False
        for i in range(resized_frame.shape[0]):
            for j in range(resized_frame.shape[1]):
                if not breaker:
                    pixel_value = resized_frame[i, j]
                    bits += get_bit_from_pixel(pixel_value)
                    counter = counter + 1
                    if get_bit_from_pixel(pixel_value) == '0':
                        blank_counter = blank_counter + 1

                    if blank_counter == 8:
                        breaker = True
                    if counter == 8:
                        counter = 0
                        blank_counter = 0

        bits = bits[:-8]

    video_reader.release()

    # Bits in eine Datei schreiben
    with open(output_file_path, 'wb') as file:
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            file.write(bytes([int(byte, 2)]))


def get_bit_from_pixel(pixel_value):
    return '1' if pixel_value < 128 else '0'


# Beispielaufruf der Funktion
video_file = 'output_video.mp4'
output_file_path = 'reconstructed_file.txt'
width, height = 1920, 1080
scale_factor = 0.25  # Stellen Sie sicher, dass dies der gleiche Skalierungsfaktor ist, der zum Erstellen des Videos verwendet wurde
bits_to_file(video_file, output_file_path, width, height, scale_factor)