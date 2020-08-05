import signal
from pylib.pycsv import PyCsv
from multiprocessing import Pool
import time
class pyPool():
    # 1 - passe a potência
    # 2 - o pacote em formato [{'indice':'item','indice':'item'}]
    # 3 - o caminho para o arquivo de log
    # 4 - a instância da função que irá processar os dados
    def __init__(self,potencia):
        print('Processando...')
        self.pacote = ''
        self.potencia = potencia
        # self.log = log
        self.function = ''
        self.pool = Pool(potencia)
        self.results =[]
    def start(self):
        self.results.append(self.pool.apply_async(self.function,(self.pacote,)))    
    def init_worker(self): 
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    def log(self,data):
       logger = PyCsv(self.log)
       logger.add_row_csv([data])
    def execute(self,pacote):
        print(pacote)

    def run(self,function,pacote):
        self.function = function
        self.pacote = pacote
        self.start()
    def close(self):
        self.pool.close()
    def join(self):
        self.pool.join()


