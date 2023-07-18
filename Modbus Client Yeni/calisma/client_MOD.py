import os
import sys
import time
import platform
from datetime import datetime
# from importlib_metadata import version


# print(version('pyModbusTCP'))


# FUNCTIONS
def timestamp():  # Returns timestamp as string
    dt_now = datetime.now()
    return dt_now.strftime("%Y-%m-%d %H:%M:%S")


# LOG INIT
def log_msg(arg_msg):  #
    # print(f"Msg {arg_msg}", flush=True)
    global arg_name_log_file
    dt_now = datetime.now()
    timestamp_log = dt_now.strftime("%Y-%m-%d %H:%M:%S>> ") + str(arg_msg) + "\n"
    file = open(arg_name_log_file, "a+")
    file.write(timestamp_log)
    file.close()
    return


# EoF Functions
path_parent = os.path.dirname(os.getcwd())
cwd = os.getcwd()
arg_name_log_file = cwd + "\\LOG_INIT.log"

debug_log_dir_LMS = cwd + "\\LMS\\"
try:
    if not os.path.exists(debug_log_dir_LMS):
        os.mkdir(debug_log_dir_LMS)
        # else:
        # print(["Debug Log LMS folder exists @ "+debug_log_dir_LMS])
except Exception as exc:
    # print(["Exception @ Debug Log LMS folder: "])
    log_msg([f"Exception @ Debug Log LMS folder: {str(exc)}"])

debug_log = cwd + "\\LMS\\DebugLogs\\"

try:
    if not os.path.exists(debug_log):
        os.mkdir(debug_log)
    else:
        arg_name_log_file = debug_log + "LOG_INIT.log"
        log_msg("LOG INIT")
        # print(["Debug Log folder exists @ "+debug_log])
except Exception as exc:
    # print(["Exception @ Debug Log folder: "])
    log_msg([f"Exception @ Debug Log folder: {str(exc)}"])

debug_log_dir = cwd + "\\LMS\\DebugLogs\\"
# print(debug_log_dir)
now = datetime.now()
timestamp_file_name = now.strftime("-%Y-%m-%d_%H-%M-%S")
arg_name_log_file = debug_log_dir + "DebugLog" + timestamp_file_name + ".log"
f = open(arg_name_log_file, "a+")
f.write(timestamp() + "\n")
f.write("OS Version     : " + platform.platform() + "||" + platform.machine() + "\n")
f.write("Python Version : " + sys.version + "\n")
f.write("Current working dir: " + cwd + "\n")
f.write("Debug & Log Folder : " + debug_log_dir + "\n")
f.close()

try:
    from pyModbusTCP.client import ModbusClient

    log_msg(["Modbus lib 'pyModbusTCP' is imported"])
except Exception as exc:
    log_msg([f"Modbus lib import ERR! {exc}"])
    print(f"Exception @ import library: {exc}", flush=True)
    sys.exit(1)


try:
    SERVER_IP = sys.argv[1]
    SERVER_PORT = sys.argv[2]
    log_msg(["Socket from args => " + str(SERVER_IP) + ":" + str(SERVER_PORT)])

    # SERVER_HOST = "192.168.2.146"
    # SERVER_HOST = "192.168.11.44"
    # SERVER_HOST ="192.168.1.20"
    # print("Host:", SERVER_HOST)
    # print("Port:", SERVER_PORT)
except Exception as exc:
    # print("No ARGs")
    SERVER_IP = "107.218.3.14"
    SERVER_PORT = 1502
    log_msg([f"Args exception => {exc}" + str(SERVER_IP) + ":" + str(SERVER_PORT)])

log_msg(["Socket settings => " + str(SERVER_IP) + ":" + str(SERVER_PORT)])

client_obj = ModbusClient()
log_msg(["Modbus Client Obj generated"])
# uncomment this line to see debug message
# client_obj.debug(True)
# define modbus server host, port
# print(f"{SERVER_HOST}:{SERVER_PORT}", flush=True)
client_obj.host = SERVER_IP
client_obj.port = SERVER_PORT
client_obj.auto_open = True 
client_obj.auto_close = False
log_msg(["Modbus Client Obj IP:PORT are set @" + str(SERVER_IP) + ":" + str(SERVER_PORT)])
log_msg(["Endless Loop is starting"])
debug_cnt = 0

while True:
    try:  # if open() is ok, read register (modbus function 0x03)
        if client_obj.open():
            if client_obj.is_open:
                # read 10 registers at address 0, store result in regs list
                if debug_cnt < 10:
                    log_msg(["Debug Count-" + str(debug_cnt) + "=>" + "Register read OK"])
                try:
                    regs = client_obj.read_holding_registers(0, 86)
                    # if success display registers
                    if regs:
                        print(str(regs), flush=True)
                        if debug_cnt < 10:
                            log_msg(["Debug Count-" + str(debug_cnt) + "=>" + str(regs)])
                except Exception as exc:
                    log_msg([f"Client reading from registers exception ERR! {exc}"])
            else:
                log_msg([f"[1] unable to connect to {str(SERVER_IP)} : {str(SERVER_PORT)}"])
                print(f"[1] unable to connect to {str(SERVER_IP)} : {str(SERVER_PORT)}", flush=True)
        else:
            log_msg([f"[2] unable to connect to {str(SERVER_IP)} : {str(SERVER_PORT)}"])
            print(f"[2] unable to connect to {str(SERVER_IP)} : {str(SERVER_PORT)}", flush=True)
    except Exception as exc:
        log_msg([f"client_obj.is_open() exception ERR! {exc}"])

    # sleep 10 sec before next polling   
    time.sleep(3)  # 10

    if debug_cnt < 10:
        debug_cnt += 1
