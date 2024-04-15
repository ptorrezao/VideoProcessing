import os
import datetime
import cv2
import shutil

def create_folder_if_not_exists(folder):
    """Cria a pasta se ela não existir."""
    if not os.path.exists(folder):
        os.makedirs(folder)

def is_video_file(file):
    """Verifica se o arquivo é um vídeo MP4."""
    return file.lower().endswith('.mp4')

def move_mp4_files_to_video_folder():
    """Move arquivos MP4 para a pasta 'Source'."""
    video_folder = 'Source'
    create_folder_if_not_exists(video_folder)

    current_folder = os.getcwd()
    files = os.listdir(current_folder)

    for file in files:
        if is_video_file(file):
            source_path = os.path.join(current_folder, file)
            dest_path = os.path.join(current_folder, video_folder, file)
            shutil.move(source_path, dest_path)
            print(f"Arquivo '{file}' movido para a pasta 'Source'.")

    print("Todos os vídeos foram movidos com sucesso para a pasta 'Source'.")

def process_video_with_label_and_acceleration(video_path, output_folder):
    """Processa um vídeo com label e aceleração."""
    if not os.path.exists(video_path):
        print(f"O vídeo '{video_path}' não existe.")
        return

    create_folder_if_not_exists(output_folder)

    # Verifica se o arquivo de saída já existe
    output_video_path = os.path.join(output_folder, f"processed_{os.path.basename(video_path)}")
    if os.path.exists(output_video_path):
        print(f"O vídeo '{video_path}' já foi processado anteriormente.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo '{video_path}'.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_color = (255, 255, 255, 100)
    thickness = 1
    position = (50, height - 50)
    position_title = (50, height - 100)

    speed = 1.5
    new_fps = fps * speed

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), new_fps, (width, height))

    modification_time = os.path.getmtime(video_path)
    modification_datetime = datetime.datetime.fromtimestamp(modification_time)
    current_date = modification_datetime.strftime('%d-%b-%Y')
    filename = "Vilhas Velhas"
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(frame, filename, position_title, font, font_scale, font_color, 2, cv2.LINE_AA)
        cv2.putText(frame, current_date, position, font, font_scale, font_color, 1, cv2.LINE_AA)

        out.write(frame)

        frame_count += 1
        print(f"Processando frame {frame_count}/{total_frames}")

    cap.release()
    out.release()

    print(f"Vídeo processado e acelerado em {speed}x salvo em '{output_video_path}'.")

def create_transition_video(input_folder, output_folder):
    """Cria transições entre vídeos na pasta de entrada."""
    if not os.path.exists(input_folder):
        print(f"A pasta de entrada '{input_folder}' não existe.")
        return

    create_folder_if_not_exists(output_folder)
    
    files = os.listdir(input_folder)
    video_files = [file for file in files if is_video_file(file)]

    if len(video_files) < 2:
        print("Pelo menos dois vídeos são necessários para criar transições.")
        return

    for i in range(len(video_files) - 1):
        video_path_1 = os.path.join(input_folder, video_files[i])
        video_path_2 = os.path.join(input_folder, video_files[i + 1])
        output_video_path = os.path.join(output_folder, f"transition_{i}.mp4")
        create_transition_between_videos(video_path_1, video_path_2, output_video_path)

    print(f"Vídeos de transição criados e salvos na pasta '{output_folder}'.")

def concatenate_videos(input_folder, output_path):
    """Concatena todos os vídeos na pasta de entrada em um único arquivo de vídeo."""
    if not os.path.exists(input_folder):
        print(f"A pasta de entrada '{input_folder}' não existe.")
        return

    create_folder_if_not_exists(os.path.dirname(output_path))

    files = os.listdir(input_folder)
    video_files = [file for file in files if is_video_file(file)]

    if len(video_files) == 0:
        print("Não há vídeos na pasta de entrada para concatenar.")
        return
    
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 44.955, (3840, 2160))
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        append_video(video_path, output_video)

    output_video.release()
    print(f"Vídeos concatenados e salvos em '{output_path}'.")

def append_video(video_path, output_video):
    """Adiciona um vídeo ao arquivo de vídeo de saída."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo '{video_path}'.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count= 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output_video.write(frame)
        frame_count += 1
        print(f"Processando frame {video_path} ->{frame_count}/{total_frames}")

    cap.release()

# Exemplo de uso das funções
move_mp4_files_to_video_folder()

input_folder = 'Source'
processed_folder = 'Processed'
processed_folder = 'Processed'

for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    
    if is_video_file(file_name):
        process_video_with_label_and_acceleration(file_path, processed_folder)

concatenate_videos(processed_folder, 'Export/Concatenados.MP4')