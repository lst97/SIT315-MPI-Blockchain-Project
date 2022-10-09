from multiprocessing import Process
import subprocess
import webbrowser

#frontend
def angular():
    subprocess.call(['ng', "serve"],cwd='./frontend/block_chain')

#backend
def api():
    subprocess.call(['uvicorn', "api:app", "--reload"],cwd='./backend')

def status_checker():
    subprocess.call(['python', "status_check.py"], cwd='./backend')

#client
def pool():
    subprocess.call(['python', "mpi_mining_pool.py"], cwd='./client')

def main():
    thread_angular = Process(target=angular)
    thread_angular.start()

    thread_api = Process(target=api)
    thread_api.start()

    thread_status_checker = Process(target=status_checker)
    thread_status_checker.start()

    thread_pool = Process(target=pool)
    thread_pool.start()

    url = 'http://localhost:4200/'
    # MacOS
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(url)

    thread_angular.join()
    thread_api.join()
    thread_status_checker.join()
    thread_pool.join()

    print("All Thread TERMINATED!")

if __name__ == '__main__':
    main()
