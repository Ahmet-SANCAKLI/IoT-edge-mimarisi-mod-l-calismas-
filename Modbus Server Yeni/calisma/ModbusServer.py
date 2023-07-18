import asyncio
import sys
import signal
from azure.iot.device.aio import IoTHubModuleClient
import argparse
from pyModbusTCP.server import ModbusServer, DataBank

# Event indicating client stop
stop_event = asyncio.Event()

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()
    return client

async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host")
    parser.add_argument("-p", "--port", type=int, default=1502, help="TCP port")
    args = parser.parse_args()

    # init modbus server and start it
    server = ModbusServer(host=args.host, port=args.port, no_block=True)
    server.start()

    while not stop_event.is_set():
        await asyncio.sleep(1)

    server.stop()

def main():
    if not sys.version >= "3.5.3":
        raise Exception("The sample requires Python 3.5.3+. Current version of Python: %s" % sys.version)

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is terminated by Edge
    def module_termination_handler(signal, frame):
        print("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()

if __name__ == "__main__":
    main()
