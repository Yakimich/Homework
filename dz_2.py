import hashlib 
import time
import multiprocessing as mp 
alphabet = "abcdefghijklmnopqrstuvwxyz"


def password_generation(idx):
    password = ""
    for i in range(5): #то что 5 симоволов
        password += alphabet[idx % len(alphabet)]
        idx = idx // len(alphabet)

    return password[::-1] 

def bruteforce_sha256(): 
    start_time = time.perf_counter()

    hash_list = ["1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
              "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
              "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f"]

    N = 26**5-1 #максимальное кол во паролей
    num_threads = int(input("Количество потоков для SHA256:")) 
    per_thread = N // num_threads 
    threads_list = []

    start = 0
    for i in range(num_threads): 
        end = start + per_thread
        t = mp.Process(target=sha256_in_thread, args=(i, hash_list, start, end)) 
        threads_list.append(t)
        t.start()
        start = end 

    for thread in threads_list:
        thread.join()
   
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print("Время выполнения: {}.".format(elapsed))

def bruteforce_md5():
    start_time = time.perf_counter()

    hash_list = ["81d45c9cf678fbaa8d64a6f29a6f97e3",
              "1f3870be274f6c49b3e31a0c6728957f",
              "d9308f32f8c6cf370ca5aaaeafc0d49b"]

    N = 26**5-1
    num_threads = int(input("Количество потоков для MD5:"))
    per_thread = N // num_threads
    threads_list = []

    start = 0
    for i in range(num_threads):
        end = start + per_thread
        t = mp.Process(target=md5_in_thread, args=(i, hash_list, start, end))
        threads_list.append(t)
        t.start()
        start = end

    for thread in threads_list:
        thread.join()

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print("Время выполнения: {}.".format(elapsed))


def sha256_in_thread(idx, hashes, start, end):
    for i in range(start, end):
        password = password_generation(i)
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        for h in hashes:
            if hash != h:
                continue
            print("Хэш {} найден пароль: {}. Поток №{}.".format(hash, password, idx))


def md5_in_thread(idx, hashes, start, end):
    for i in range(start, end):
        password = password_generation(i)
        hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        for h in hashes:
            if hash != h:
                continue
            print("Хэш {} найден пароль: {} Поток №{}.".format(hash, password, idx))

if __name__ == '__main__': 
    bruteforce_sha256()
    bruteforce_md5()