# py-ur

## Control Universal Robot via python

### Simple functions and convenience class to manipulate UR data

Dashboard Functions based
on : [DashboardServer_e-Series_2022](https://s3-eu-west-1.amazonaws.com/ur-support-site/42728/DashboardServer_e-Series_2022.pdf)

Modbus Registers functions based
on : [ModBus Server Data](https://s3-eu-west-1.amazonaws.com/ur-support-site/16377/ModBus%20Server%20Data.pdf)
https://www.universal-robots.com/articles/ur/interface-communication/modbus-server/

## Modbus Register commands

### Read from register

| Transaction ID | Protocol ID | Length    | Unit ID | Function Code | Starting Address | Quantity  |
|:---------------|:------------|:----------|:--------|:--------------|:-----------------|:----------|
| 0x00 0x01      | 0x00 0x00   | 0x00 0x06 | 0x01    | 0x02          | 0x00 0x00        | 0x00 0x08 |

### Write to register

| Transaction ID | Protocol ID | Length    | Unit ID | Function Code | Register Address | Value     |
|:---------------|:------------|:----------|:--------|:--------------|:-----------------|:----------|
| 0x00 0x01      | 0x00 0x00   | 0x00 0x06 | 0x01    | 0x06          | 0x00 0x01        | 0x12 0x34 |

1. Transaction id can be anything, I use the register address, so it's easier to keep track of the returning packets.
2. Protocol ID is alway 0000 for modbus
3. Length is always 6 if you only interact with one register at a time
4. Unit ID doesn't matter, so I usually put 0
5. Function codes can be
   found [here](https://www.universal-robots.com/articles/ur/interface-communication/modbus-server/)

> * 0x01: READ_COILS (read output bits)
> * 0x02: READ_DISCRETE_INPUTS (read input bits)
> * 0x03: READ_HOLDING_REGISTERS (read output registers)
> * 0x04: READ_INPUT_REGISTERS (read input registers)
> * 0x05: WRITE_SINGLE_COIL (write output bit)
> * 0x06: WRITE_SINGLE_REGISTER(write output register)
> * 0x0F: WRITE_MULTIPLE_COILS (write multiple output bits)
> * 0x10: WRITE_MULTIPLE_REGISTERS (write multiple output registers)

## Dashboard commands

| command                       | return value                                                                                                                                                       |                                                                                                                                                                                                                                description |
|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| <pre>load <program.urp></pre> | <pre>On success: "Loading program:<program.urp>" <br/>On Failure:<br/> - "File not found:<program.urp>" <br/> - "Error while loading program: <program.urp>"</pre> | Returns when both program and associated installation has loaded (or failed). The load command fails if the associated installation requires confirmation of safety. The return  value in this case will be 'Error while loading program'. |
|
| hello                         | world                                                                                                                                                              |                                                                                                                                                                                                                                     whynot |
