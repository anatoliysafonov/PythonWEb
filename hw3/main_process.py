from multiprocessing import cpu_count
import concurrent.futures
from main import get_digits
from time import time

data = [128, 255, 99999, 10651060]

if __name__ == '__main__':

    time_start = time()
    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        results = list(executor.map(get_digits, data))
    print(f'Time requested: {time() - time_start}')
    [print(item) for item in results]
