from multiprocessing import cpu_count
import concurrent.futures
from time import time


def get_digits(value:int) -> list[int]:
    return [i for i in range(1, value + 1) if value % i == 0]


if __name__ == '__main__':
    data = [128, 255, 99999, 10651060]
    time_start = time()
    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        results = list(executor.map(get_digits, data))
    print(f'Time requested: {time() - time_start}')
    [print(item) for item in results]
