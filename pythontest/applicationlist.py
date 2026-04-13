import psutil

def get_process_list():
    processes = []
    for proc in psutil.process_iter(['pid','name','exe']):
        processes.append({'pid':proc.info['pid'],'name':proc.info['name'],'exe':proc.info['exe']})

# def print_proc():

