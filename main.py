from bluepy.btle import Peripheral, Characteristic, Descriptor, Service, UUID, DefaultDelegate
import time
import os
import dotenv
import binascii

ENABLE_NOTIFICATIONS = b'\x01\x00'

UUID_SVC_BATTERY = UUID('0000180f-0000-1000-8000-00805f9b34fb')
UUID_CHAR_BATTERY_LEVEL = UUID('00002a19-0000-1000-8000-00805f9b34fb')

UUID_GAS_SERVICE = UUID('fc247940-6e08-11e4-80fc-0002a5d5c51b')
UUID_GAS_WRITEONLY_CHAR = UUID('3d115840-6e0b-11e4-b24f-0002a5d5c51b')
UUID_GAS_NOTIFICATION_CHAR = UUID('f833d6c0-6e0b-11e4-9136-0002a5d5c51b')

FIRST_WRITE = b'\x3c\x61\x30\x31\x38\x30\x30\x31\x30\x30\x31\x65\x36\x33\x30\x45\x3d\x31\x32\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x42\x45\x46\x31\x3e'
SECOND_WRITE = b'\x3c\x61\x30\x31\x38\x30\x30\x31\x30\x30\x33\x62\x36\x30\x30\x32\x3f\x3b\x36\x31\x30\x41\x3f\x3b\x36\x30\x30\x41\x3f\x3b\x36\x30\x30\x39\x3f\x3b\x36\x30\x30\x37\x3f\x3b\x36\x30\x30\x38\x3f\x3b\x36\x30\x30\x34\x3f\x3b\x36\x30\x30\x35\x3f\x3b\x32\x41\x32\x32\x3f\x3b\x32\x41\x32\x33\x3f\x43\x35\x44\x34\x3e'
THIRD_FOURTH_WRITE = b'\x3c\x61\x30\x31\x38\x30\x30\x31\x30\x30\x30\x36\x36\x33\x30\x46\x3d\x31\x41\x30\x31\x30\x3e'
FIFTH_WRITE = b'\x7b\x41\x00\x08\x40\xa2\x02\x01\x01\xea\x2f\x7d'

NOTIFICATION_REQUEST = b'\x7b\x41\x00\x06\x40\xa1\x01\x3f\xfb\x7d'

dotenv.load_dotenv()

MAC = os.getenv('MAC')
if not MAC:
    raise Exception('MAC address was not found in .env file')

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

    def get_gas_write_char(self) -> Characteristic:
        svc: Service = self.getServiceByUUID(UUID_GAS_SERVICE)
        chars = svc.getCharacteristics(UUID_GAS_WRITEONLY_CHAR)
        if len(chars) != 0:
            return chars[0]
        else:
            raise Exception(f'failed to get write char, could not find such in {UUID_GAS_SERVICE} service')

    def get_gas_notification_char(self) -> Characteristic:
        svc: Service = self.getServiceByUUID(UUID_GAS_SERVICE)
        chars = svc.getCharacteristics(UUID_GAS_NOTIFICATION_CHAR)
        if len(chars) != 0:
            return chars[0]
        else:
            raise Exception(f'failed to get notification char, could not find such in {UUID_GAS_SERVICE} service')
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
    device = Honeywell(MAC) # initializing connection
    print('Connected!')

    print('You now have a minute to pair your devices using bluetoothctl..')
    time.sleep(60)

    writeChar = device.get_gas_write_char()

    delegate = NotificationDelegate(device) # enabling notificaions here
    device.setDelegate(delegate)
    writeChar.write(ENABLE_NOTIFICATIONS)

    # device.inspect()
    print('Battery level: ', device.read_battery_level())

    # auth? !! set True to False if it fails !!
    writeChar.write(FIRST_WRITE, True)
    device.waitForNotifications(5)
    writeChar.write(SECOND_WRITE, True)
    device.waitForNotifications(5)
    writeChar.write(THIRD_FOURTH_WRITE, True)
    device.waitForNotifications(5)
    writeChar.write(THIRD_FOURTH_WRITE, True)
    device.waitForNotifications(5)

    while True:
        writeChar.write(NOTIFICATION_REQUEST, True)
        time.sleep(5)

if __name__ == '__main__':
    main()