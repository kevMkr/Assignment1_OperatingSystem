import threading
import random

LOWER_NUM   = 1
UPPER_NUM   = 10_000
BUFFER_SIZE = 100
MAX_COUNT   = 10_000


buffer         = []   
consumed_count = 0    
lock           = threading.Condition()   

def producer(all_file):
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            while len(buffer) == BUFFER_SIZE:
                lock.wait()
            buffer.append(num)          
            all_file.write(f"{num}\n")
            lock.notify_all()           

def consumer(target_parity: int, out_file):
    global consumed_count
    while True:
        with lock:
            while True:
                if consumed_count >= MAX_COUNT:
                    return                          
                if buffer and buffer[-1] % 2 == target_parity:
                    break                           
                lock.wait()                         

            num = buffer.pop()                      
            consumed_count += 1
            out_file.write(f"{num}\n")
            lock.notify_all()                       


def main():
    with (open("all.txt",  "w") as all_file,
          open("even.txt", "w") as even_file,
          open("odd.txt",  "w") as odd_file):

        t_prod      = threading.Thread(target=producer, args=(all_file,),
                                       name="Producer")
        t_even_cons = threading.Thread(target=consumer, args=(0, even_file),
                                       name="Consumer-Even")
        t_odd_cons  = threading.Thread(target=consumer, args=(1, odd_file),
                                       name="Consumer-Odd")

        t_prod.start()
        t_even_cons.start()
        t_odd_cons.start()

        t_prod.join()
        t_even_cons.join()
        t_odd_cons.join()


if __name__ == "__main__":
    main()
