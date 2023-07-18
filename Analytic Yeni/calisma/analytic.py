import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
import pandas as pd
from pyModbusTCP.server import ModbusServer, DataBank


# Event indicating client stop
stop_event = threading.Event()

column_details = {
    'roll_mean': [],
    'pitch_mean': []
}

# creating a DataFrame object
static_mean_df = pd.DataFrame(column_details)


def process_modbus_data(modbus_data):
    df = pd.read_json(modbus_data)

    roll_mean = df['roll'].mean()
    pitch_mean = df['pitch'].mean()

    roll_mean_sign = "1" if roll_mean < 0 else "0"
    pitch_mean_sign = "1" if pitch_mean < 0 else "0"

    heading_mean = df['heading'].mean()
    heading_mean_sign = "1" if heading_mean < 0 else "0"

    gForcemagnitude_mean = df['gForcemagnitude'].mean()
    gForcemagnitude_mean_sign = "1" if gForcemagnitude_mean < 0 else "0"

    east_offset_mean = df['east_offset'].mean()
    east_offset_mean_sign = "1" if east_offset_mean < 0 else "0"

    north_offset_mean = df['north_offset'].mean()
    north_offset_mean_sign = "1" if north_offset_mean < 0 else "0"

    total_offset_mean = df['total_offset'].mean()
    total_offset_mean_sign = "1" if total_offset_mean < 0 else "0"

    sign_string = roll_mean_sign + pitch_mean_sign + heading_mean_sign + gForcemagnitude_mean_sign + east_offset_mean_sign + north_offset_mean_sign + total_offset_mean_sign

    sign_binary = int(sign_string, 2)

    DataBank.set_words(0, [int(roll_mean * 1000)])  # *1000
    DataBank.set_words(1, [int(pitch_mean * 1000)])  # *1000
    DataBank.set_words(2, [int(heading_mean * 100)])
    DataBank.set_words(3, [int(gForcemagnitude_mean * 100)])
    DataBank.set_words(4, [int(east_offset_mean * 100)])
    DataBank.set_words(5, [int(north_offset_mean * 100)])
    DataBank.set_words(6, [int(total_offset_mean * 100)])

    df_instance = {'roll_mean': roll_mean, 'pitch_mean': pitch_mean}
    static_mean_df = static_mean_df.append(df_instance, ignore_index=True)

    if len(static_mean_df.index) > 500:
        static_mean_df = static_mean_df.iloc[1:, :]

    static_mean_roll = static_mean_df['roll_mean'].mean()
    static_mean_pitch = static_mean_df['pitch_mean'].mean()

    print(f"static_mean_roll, static_mean_pitch: {static_mean_roll}, {static_mean_pitch}")
    print(static_mean_df)

    return static_mean_df


def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            print("the data in the message received on input1 was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("forwarding message to output1")
            await client.send_message_to_output(message, "output1")

            # Process modbus data and get DataFrame
            modbus_data = message.data  # Assuming the message contains the modbus data as a JSON string
            df = process_modbus_data(modbus_data)

            # Do whatever you need to do with the DataFrame 'df' here

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception("The sample requires python 3.5.3+. Current version of Python: %s" % sys.version)
    print("IoT Hub Client for Python")

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
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
