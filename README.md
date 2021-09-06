# honeywell-bw-solo-python

## Turn on bluetooth
```zsh
$ bluetoothctl

[bluetooth] power on
```

## Installing dependencies
```zsh
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Setting MAC address and auth key
Set `MAC` in `.env` file according to example in `.env.example`
```zsh
MAC=AA:AA:AA:AA:AA:AA
```

## Running
```zsh
python3 main.py
```

## Pairing
After success connection you will see a message: `You now have a minute to pair your devices using bluetoothctl..` in a console, which means that you should run `bluetoothctl` in a terminal and then pair your devices like so `pair AA:AA:AA:AA:AA:AA`
