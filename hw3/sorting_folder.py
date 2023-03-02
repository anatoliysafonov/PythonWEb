import concurrent.futures
from multiprocessing import cpu_count
from pathlib import Path
from tkinter.filedialog import askdirectory
from tkinter import Tk

LIST_OF_FOLDERS = {'pictures':     ['JPEG', 'PNG', 'JPG', 'SVG'],
                   'video':        ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio':        ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':     ['ZIP', 'GZ', 'TAR'],
                   'others':       []
                   }

def get_subfolder(filename:Path):
    for key, value in LIST_OF_FOLDERS.items():
        suffix = filename.suffix[1:]       
        if suffix.upper() in value:
            return  key
    return 'others'


def do_sort(source:str):
    global path_to_sorted_folder

    source = Path(source)
    for item in source.iterdir():
       if item.is_file():
            if item.name == ".DS_Store":
                item.unlink()
                continue
            dest_path = Path(path_to_sorted_folder) / get_subfolder(item)
            dest_path.mkdir(parents=True, exist_ok=True)
            dest_path = dest_path / item.name
            item.rename(dest_path)

        
    


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    paths = []
    for i in range(2):
        paths.append(askdirectory())
    path_to_unsorted_folder, path_to_sorted_folder = paths

    list_inner_folders = [folder for folder in Path(path_to_unsorted_folder).rglob('*') if folder.is_dir()]
    list_inner_folders.append(path_to_unsorted_folder)
    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        results = filter(None,list(executor.map(do_sort, list_inner_folders)))
    
    [print(res) for res in results]
