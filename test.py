from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool

def squareNumber(n):
    return n ** 2

# function to be mapped over
def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(squareNumber, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    squaredNumbers = calculateParallel(numbers, 4)
    for n in squaredNumbers:
        print(n)

        executor = ThreadPoolExecutor(max_workers=10)
        a = executor.submit(my_function)