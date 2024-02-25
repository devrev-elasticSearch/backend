from Integration.DataModelCreator import loop as datamodelLoop
from Integration.Features import loop as featureLoop
from Integration.Denoiser import loop as denoiserLoop
from Integration.TicketGenerator import generator as ticketGenerator
from multiprocessing import Process
import json


if __name__ == "__main__":
    print("Starting")
    processes = []
    
    try:
        p = Process(target=datamodelLoop.loop)
        p.start()
        processes.append(p)
        
        p = Process(target=featureLoop.loop)
        p.start()
        processes.append(p)
        
        p = Process(target=denoiserLoop.loop)
        p.start()
        processes.append(p)
        
        p = Process(target=ticketGenerator.generateTickets)
        p.start()
        processes.append(p)
        
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
            p.join()
    
    
    print("hello")