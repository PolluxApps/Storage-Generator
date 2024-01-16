def create_video_from_bits(bits, width, height, video_file, frame_rate, frame_count):
    # Skalierungsfaktor, z.B. 0.5 für Halbierung der Größe
    scale_factor = 0.5

    # Angepasste Größe für das Frame
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_file, fourcc, frame_rate, (width, height), False)

    total_bits = width * height * frame_count
    for i in range(0, total_bits, width * height):
        frame_bits = bits[i:i + width * height]
        frame = create_image_from_bits(frame_bits, scaled_width, scaled_height)

        # Skalieren Sie das Frame zurück auf die ursprüngliche Größe
        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)

        video_writer.write(resized_frame)
    video_writer.release()