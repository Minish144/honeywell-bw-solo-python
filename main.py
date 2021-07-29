from bluepy.btle import Peripheral, Characteristic, Descriptor, Service, UUID, DefaultDelegate
import time
import os
import dotenv

dotenv.load_dotenv()

MAC = os.getenv('MAC')
if not MAC:
    raise Exception('MAC address was not found in')

class Honeywell(Peripheral):
    '''
    RD1212 is a class which provides
    you useful methods to work with
    Honeywell BW Solo
    '''
    def __init__(self, MAC: str):
        super().__init__(MAC)
    
    def inspect(self) -> None:
        '''
        inspect prints available
        services and its characteristics
        '''
        svcs = self.getServices()
        for svc in svcs: 
            print(f'\n       {svc.uuid}       ')
            print('--------------------------------------------------')
            for ch in svc.getCharacteristics():
                print(f'[{ch.getHandle()}]', '0x'+ format(ch.getHandle(),'02X')  +'   '+str(ch.uuid) +' ' + ch.propertiesToString())
        print('\n')

class NotificationDelegate(DefaultDelegate):
    '''
    NotificationDelegate is a
    DefaultDelegate class with
    overridden notification handler
    '''
    def __init__(self, device: Honeywell):
        super().__init__()
        self.device = device

    def handleNotification(self, hnd, data):
        '''
        handleNotification handles new notification
        '''
        print(f'[{hnd}]: {list(data)}')


def main():
    print('Connecting..')
    device = Honeywell(MAC) # initialize connection
    print('Connected!')

    device.inspect()
    
if __name__ == '__main__':
    main()