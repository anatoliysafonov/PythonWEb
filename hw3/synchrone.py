from time import time


def get_digits(max_value: int) -> list:
    return [i for i in range(1, max_value + 1) if max_value % i == 0]


def deco(func):
    def inner(*args):
        t_start = time()
        result = func(*args)
        runtime = time() - t_start
        return result, runtime
    return inner


@deco
def do_work(*args) -> list:
    result = []
    for item in args:
        result.append(get_digits(item))
    return result


if __name__ == '__main__':
    res, time_running = do_work(128, 255, 99999, 10651060)
    print(f'Time requested: {time_running}')
    [print(item) for item in res]
