## Modbus Server and Client

Implementations in Python 3 can be found in
`server.py`
and `client.py`.

## Dependencies

* numpy

## Installation

Using a virtual environment (recommended), install with:

```
python -m venv venv && source venv/bin/activate
(venv) pip3 install modbus
```

If you wish to run with the default modbus/tcp port 502/tcp,
consider creating and activating the virtualenv using sudo.

## Usage Examples

### Server

The IANA defined default TCP port for modbus/tcp is `502/tcp`.
To run on this low-numbered port requires root privileges.

```
sudo python3 -m modbus.server ...to run server in commandline
```

* For Register Read,
  the server sends value starting from 1 and incrementing upto 6000.
  For example,
  the client wants to read with
  `FuncCode=3`,
  `Address=0`,
  `and Length=4`.
  Then the server's reply for values will be
  `1,2,3,4`
  for the first read
  and values will increment
  for every subsequent read.



### 使用方法：
getip.py:查看本机ip地址\
test.py:运行client例程