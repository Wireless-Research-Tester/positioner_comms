# from multiprocessing import Process, Queue
from threading import Thread
from queue import Queue, Empty, Full
from time import time, sleep

import sys
sys.path.append("D:\\")

import positioner as pos
import integer as qi
import packet as pkt
import packet_parser as par


def Transceiver_Thread(q, qpt):
    p = par.Packet_Parser()
    while True:
        try:
            s = q.get_nowait()
        except Empty as e:
            s = 'Get_Status'

        if s == 'Get_Status':
            rx = qpt.comms.positioner_query(pkt.get_status())


        if qpt.status_executing is False:
            break
            
        sleep(.1)


if __name__=='__main__':
    qpt = pos.Positioner()

    q = Queue()

    transceiver = Thread(target=Transceiver_Thread, args=(q,qpt,), daemon=True)
    transceiver.start()
    

    # qpt.move_to(0,0,'zero')
    # qpt.move_to(-180,-90,'abs')
    # qpt.move_to(180,90,'abs')

    # transceiver.join()

    while True:
        sleep(1)
    #     # if qpt.executing == False:
    #     #     transceiver.start()



