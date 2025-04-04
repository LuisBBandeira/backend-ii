import time
import multiprocessing

def calculate_squares():
    start = time.time()
    result = [i * i for i in range(1, 1000001)]
    print(f"Calculating squares took {time.time() - start:.2f} seconds.")

def calculate_cubes():
    start = time.time()
    result = [i ** 3 for i in range(1, 1000001)]
    print(f"Calculating cubes took {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    start = time.time()
    p1 = multiprocessing.Process(target=calculate_squares)
    p2 = multiprocessing.Process(target=calculate_cubes)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"Total time: {time.time() - start:.2f} seconds.")