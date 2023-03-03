import concurrent.futures
from multiprocessing import cpu_count, RLock
from pathlib import Path
import argparse

LIST_OF_FOLDERS = {'pictures':     ['JPEG', 'PNG', 'JPG', 'SVG'],
                   'video':        ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio':        ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':     ['ZIP', 'GZ', 'TAR'],
                   'others':       []
                   }

source_folder = destination_folder = None
locker = RLock()

#взнаємо назву папки по розширенню файла який переноситься
def get_subfolder(filename:Path):
    for key, value in LIST_OF_FOLDERS.items():
        suffix = filename.suffix[1:]       
        if suffix.upper() in value:
            return  key
    return 'others'

#функція як поток процесса по перенесенню файлів з папки яку сортуємо
def do_sort(source:str):
    global destination_folder
    global locker
    source:Path = Path(source)
    for item in source.iterdir():
       if item.is_file():
            if item.name == ".DS_Store":
                item.unlink()
                continue
            dest_path = Path(destination_folder) / get_subfolder(item)
            dest_path.mkdir(parents=True, exist_ok=True)
            dest_path = dest_path / item.name
            with locker:
                item.rename(dest_path)
    #якщо ми запустити скрипт з самої папки яку треба розслртувати, то скрипт буде намагатись видалили саму папку в яку ми кладемо файли ,тому ігноруємо помилку
    with locker:
        try:
            source.rmdir()
        except Exception:
            pass
        
    


def main():
    #Визначаємо глобальні змінні для використання в процессах
    global source_folder
    global destination_folder

    #визначаємо вихідну папку та вхідну
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=str, help='-> Path to source folder. When is empty source folder = current folder')
    parser.add_argument('destination', nargs='?', type=str, help='-> Optional. Path to distanation folde.  When is empty destination folder = current folderr')
    parser.add_argument('-l','--log', nargs='?', default=False, help='-> Output log info  file')
    args = parser.parse_args()

    #якщо не вказана вхідна та вихідна папка, тоді використовуємо папку з якої запустився скрипт
    current_folder = Path().absolute()
    source_folder = args.source or current_folder
    destination_folder = args.destination or current_folder

    #визначаємо всі вкладені папки в папці яку треба розсортувати 
    list_inner_folders = [folder for folder in Path(source_folder).rglob('*') if folder.is_dir()]
    list_inner_folders.append(source_folder)

    #запускаємо для кожної папки окремий процесс в pool
    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        results = filter(None,list(executor.map(do_sort, list_inner_folders)))
    
if __name__ == '__main__':
    main()