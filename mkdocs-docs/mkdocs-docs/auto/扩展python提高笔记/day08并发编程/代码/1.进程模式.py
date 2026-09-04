import multiprocessing


def tast():
    print(123)


def run():
    multiprocessing.set_start_method("fork")
    p = multiprocessing.Process(target=tast)
    p.start()


if __name__ == '__main__':
    run()
