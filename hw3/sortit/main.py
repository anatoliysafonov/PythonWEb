import concurrent.futures
from multiprocessing import cpu_count, RLock
from datetime import datetime
from pathlib import Path
import argparse

from prompt_toolkit.shortcuts import yes_no_dialog
from loguru import logger


LIST_OF_FOLDERS = {'pictures':     ['JPEG', 'PNG', 'JPG', 'SVG'],
                   'video':        ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio':        ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':     ['ZIP', 'GZ', 'TAR'],
                   'LOGS':          ['LOG'],
                   'others':       []
                   }

source_folder = destination_folder = None
locker = RLock()
logger_ = logger

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
    global logger_
    source = Path(source)
    for item in source.iterdir():
       if item.is_file():
            if item.name == ".DS_Store":
                item.unlink()
                continue
            if item.name == 'sortis.log':
                continue
            dest_path = destination_folder / get_subfolder(item)
            dest_path.mkdir(parents=True, exist_ok=True)
            dest_path = dest_path / item.name
            with locker:
                item.rename(dest_path)
                logger_.info(f'{source.absolute()} -> {dest_path.absolute()}')
            
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
    logs = []

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

    answer = True
    if source_folder ==  current_folder or source_folder =='.':
        answer = yes_no_dialog(
            title='WARNING',
            text='Do You really want to sort CURRENT folder?'
        ).run()
    if not answer:
        quit()
    
    
    #logs записуємо тільки у файл 
    logger_.remove(0)
    logger_.add(f'{destination_folder}/sortit.log', format='{message}')
    logger_.info (f'\n-- {datetime.now()} --')

    source_folder = Path(source_folder)
    destination_folder = Path(destination_folder)
    #визначаємо всі вкладені папки в папці яку треба розсортувати 
    list_inner_folders = [folder for folder in source_folder.rglob('*') if folder.is_dir()]
    list_inner_folders.append(source_folder.name)

    #запускаємо для кожної папки окремий процесс в pool
    results = None
    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        filter(None,list(executor.map(do_sort, list_inner_folders)))

    print('DONE!!!')
    print(f'see {destination_folder.absolute()}/sortit.log file')

if __name__ == '__main__':
    main()
    
