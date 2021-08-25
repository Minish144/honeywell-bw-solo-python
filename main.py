from bluepy.btle import Peripheral, Characteristic, Descriptor, Service, UUID, DefaultDelegate
import time
import os
import dotenv

UUID_SVC_BATTERY = UUID('0000180f-0000-1000-8000-00805f9b34fb')
UUID_CHAR_BATTERY_LEVEL = UUID('00002a19-0000-1000-8000-00805f9b34fb')

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

    def read_battery_level(self) -> int:
        char: Characteristic = self.get_battery_level_char()
        if char.supportsRead():
            return list(char.read())[0]
        else:
            raise Exception('Battery level characteristic is not readable')

    def get_battery_level_char(self) -> Characteristic:
        svc: Service = self.getServiceByUUID(UUID_SVC_BATTERY)
        chars = svc.getCharacteristics(UUID_CHAR_BATTERY_LEVEL)
        if len(chars) != 0:
            return chars[0]
        else:
            raise Exception(f'failed to get battery level char, could not find such in {UUID_SVC_BATTERY} service')


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
    while True:
        print('Battery level: ', device.read_battery_level())
        time.sleep(30)

if __name__ == '__main__':
    main()