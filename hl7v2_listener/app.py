#!/usr/bin/python3.7

'''HL7v2 listener receives HL7v2 messages, acknowledges
   and stores them in a database
   Arguments: config file
   Returns: exit status
   Authors: Alejandro Cosa-Linan, Alejandro.Cosa-Linan@medma.uni-heidelberg.de
            Lukas Goetz, Lukas.Goetz@medma.uni-heidelberg.de
   Date: October 2020'''

from datetime import datetime
import logging
import os
import sys
import asyncio
import hl7
import psycopg2
import socket

class ConfigValueError(ValueError):
    '''Config parameter must be a number'''

class ClientContext:
    '''Callback class for server'''
    def __init__(self, listener, database, logger):
        self.listener = listener
        self.database = database
        self.logger = logger

    async def handle_echo(self, reader, writer):
        '''Callback function for server'''
        start_block = b"\x0b"
        end_block = b"\x1c"
        carriage_return = b"\x0d"

        sep = end_block + carriage_return
        data = await reader.readuntil(sep)
        message = data.decode('utf-8')
        addr = writer.get_extra_info('peername')

        parsed_message = hl7.parse(message, encoding="utf-8")
        self.logger.info("HL7v2 message received and parsed"\
                        f"(type: {parsed_message[0][9]})")
        self.logger.debug(f"HL7v2 complete message: {message}")

        if self.listener['ack']:
            ack_message = parsed_message.create_ack('AA')
            ack_message = str(ack_message).encode()
            ack = start_block + ack_message + end_block + carriage_return
            writer.write(ack)
            await writer.drain()
            self.logger.info("HL7v2 message acknowledged")
            self.logger.debug(f"HL7v2 acknowledgement message: {ack_message}")

        sender = addr[0]
        receiver = self.listener['host_ip']
        msg_type = parsed_message[0][9]

        with psycopg2.connect(f"""host='{self.database['host']}' \
                                  dbname='{self.database['dbname']}' \
                                  user='{self.database['usr']}' \
                                  password='{self.database['pwd']}'""") as db_conn:
            cur = db_conn.cursor()
            current_utc_ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            query = "INSERT INTO messages (sender, receiver, rectime_utc,"\
                    " message_type, raw_message) VALUES (%s, %s, %s, %s, %s);"
            db_data = (sender, receiver, current_utc_ts, msg_type, message)

            cur.execute(query, db_data)
            db_conn.commit()
            self.logger.info("HL7v2 message stored in database")

        writer.close()

        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect((self.listener['rcv_host'], self.listener['rcv_port']))
        new_socket.sendall(data)
        self.logger.info("HL7v2 message forwarded to FHIR mapper")

        self.logger.info("Close the connection")

async def main(listener, database, logger):
    '''Function for starting the server'''
    ctx = ClientContext(listener, database, logger)
    server = await asyncio.start_server(ctx.handle_echo,
                                        listener['host'],
                                        listener['port'])

    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

try:
    RETURN_VAL = 0
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler('debug.log'),
                                  logging.StreamHandler()])
    NEW_LOGGER = logging.getLogger(__name__)

    LISTENER = {}
    DATABASE = {}
    LISTENER['host'] = '0.0.0.0'
    LISTENER['host_ip'] = os.environ['LISTENER_HOST_IP']
    LISTENER['port'] = int(os.environ['LISTENER_PORT'])
    LISTENER['rcv_host'] = os.environ['LISTENER_RCV_HOST']
    LISTENER['rcv_port'] = int(os.environ['LISTENER_RCV_PORT'])
    LISTENER['ack'] = True
    DATABASE['host'] = os.environ['DATABASE_HOST']
    DATABASE['dbname'] = os.environ['DATABASE_DBNAME']
    DATABASE['usr'] = os.environ['DATABASE_USR']
    DATABASE['pwd'] = os.environ['DATABASE_PWD']

    NEW_LOGGER.info("Running HL7v2 Listener...")
    asyncio.run(main(LISTENER, DATABASE, NEW_LOGGER))

except Exception as exc:
    RETURN_VAL = 1
    NEW_LOGGER.error(f"In '{__name__}': Unexpected error 'exc' occurred", exc_info=True)
finally:
    sys.exit(RETURN_VAL)
