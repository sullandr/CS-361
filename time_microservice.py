"""API service that returns current date and time in UTC or (optional) passed timezone"""

import socket
import json
from datetime import datetime, timezone, timedelta

def get_utc_time() -> object:
    """
    Returns current time in UTC

    :return: current UTC time object
    """
    return datetime.now(timezone.utc)

def get_adjusted_time(tz_offset) -> object:
    """
    Returns current time in passed timezone offset

    :param tz_offset: integer of timezone offset from UTC
    
    :return: current time object
    """
    try:
        tz = timezone(timedelta(hours=float(tz_offset)))    # finds timezone info for passed offset
        adjusted_time = get_utc_time().astimezone(tz)   #converts from UTC time
        return adjusted_time
    except ValueError:
        return None

def format_time(time_obj, tz_offset) -> dict:
    """
    Converts time object to dictionary for response to client

    :param time_obj: time object from datetime
    :param tz_offset: timezone offset from UTC

    :return: dictionary of values
    """
    return {
        "year": time_obj.year,
        "month": time_obj.month,
        "day": time_obj.day,
        "hour": time_obj.hour,
        "minute": time_obj.minute,
        "second": time_obj.second,
        "UTC_offset": tz_offset
    }

def timezone_search(tz_shortcode):
    """
    Returns UTC offset for passed timezone shortcode

    :param tz_shortcode: shortcodes for timezones 
        (e.g. PST for Pacific Standard Time)

    :return: integer for UTC offset, or returns passed 
        parameter if not in dictionary
    """
    # dictionary of timezone shortcodes
    shortcodes = {
        "ACDT": 10.5,
        "ACST": 9.5,
        "ACT": -5,
        "ACWST": 8.75,
        "ADT": -3,
        "AEDT": 11,
        "AEST": 10,
        "AFT": 4.5,
        "AKDT": -8,
        "AKST": -9,
        "ALMT": 6,
        "AMST": -3,
        "AMT": -4,
        "ANAT": 12,
        "AQTT": 5,
        "ART": -3,
        "AST": 3,
        "AWST": 8,
        "AZOST": 0,
        "AZOT": -1,
        "AZT": 4,
        "BNT": 8,
        "BIOT": 6,
        "BIT": -12,
        "BOT": -4,
        "BRST": -2,
        "BRT": -3,
        "BST": 1,
        "BTT": 6,
        "CAT": 2,
        "CCT": 6.5,
        "CDT": -5,
        "CEST": 2,
        "CET": 1,
        "CHADT": 13.75,
        "CHAST": 12.75,
        "CHOT": 8,
        "CHOST": 9,
        "CHST": 10,
        "CHUT": 10,
        "CIST": -8,
        "CKT": -10,
        "CLST": -3,
        "CLT": -4,
        "COST": -4,
        "COT": -5,
        "CST": -6,
        "CVT": -1,
        "CWST": 8.75,
        "CXT": 7,
        "DAVT": 7,
        "DDUT": 10,
        "DFT": 1,
        "EASST": -5,
        "EAST": -6,
        "EAT": 3,
        "ECT": -4,
        "EDT": -4,
        "EEST": 3,
        "EET": 2,
        "EGST": 0,
        "EGT": -1,
        "EST": -5,
        "FET": 3,
        "FJT": 12,
        "FKST": -3,
        "FKT": -4,
        "FNT": -2,
        "GALT": -6,
        "GAMT": -9,
        "GET": 4,
        "GFT": -3,
        "GILT": 12,
        "GIT": -9,
        "GMT": 0,
        "GST": 4,
        "GYT": -4,
        "HDT": -9,
        "HAEC": 2,
        "HST": -10,
        "HKT": 8,
        "HMT": 5,
        "HOVST": 8,
        "HOVT": 7,
        "ICT": 7,
        "IDLW": -12,
        "IDT": 3,
        "IOT": 6,
        "IRDT": 4.5,
        "IRKT": 8,
        "IRST": 3.5,
        "IST": 1,
        "JST": 9,
        "KALT": 2,
        "KGT": 6,
        "KOST": 11,
        "KRAT": 7,
        "KST": 9,
        "LHST": 10.5,
        "LINT": 14,
        "MAGT": 12,
        "MART": -9.5,
        "MAWT": 5,
        "MDT": -6,
        "MET": 1,
        "MEST": 2,
        "MHT": 12,
        "MIST": 11,
        "MIT": -9.5,
        "MMT": 6.5,
        "MSK": 3,
        "MST": -7,
        "MUT": 4,
        "MVT": 5,
        "MYT": 8,
        "NCT": 11,
        "NDT": -2.5,
        "NFT": 11,
        "NOVT": 7,
        "NPT": 5.75,
        "NST": -3.5,
        "NT": -3.5,
        "NUT": -11,
        "NZDT": 13,
        "NZST": 12,
        "OMST": 6,
        "ORAT": 5,
        "PDT": -7,
        "PET": -5,
        "PETT": 12,
        "PGT": 10,
        "PHOT": 13,
        "PHT": 8,
        "PHST": 8,
        "PKT": 5,
        "PMDT": -2,
        "PMST": -3,
        "PONT": 11,
        "PST": -8,
        "PWT": 9,
        "PYST": -3,
        "PYT": -4,
        "RET": 4,
        "ROTT": -3,
        "SAKT": 11,
        "SAMT": 4,
        "SAST": 2,
        "SBT": 11,
        "SCT": 4,
        "SDT": -10,
        "SGT": 8,
        "SLST": 5.5,
        "SRET": 11,
        "SRT": -3,
        "SST": 8,
        "SYOT": 3,
        "TAHT": -10,
        "THA": 7,
        "TFT": 5,
        "TJT": 5,
        "TKT": 13,
        "TLT": 9,
        "TMT": 5,
        "TRT": 3,
        "TOT": 13,
        "TST": 8,
        "TVT": 12,
        "ULAST": 9,
        "ULAT": 8,
        "UTC": 0,
        "UYST": -2,
        "UYT": -3,
        "UZT": 5,
        "VET": -4,
        "VLAT": 10,
        "VOLT": 3,
        "VOST": 6,
        "VUT": 11,
        "WAKT": 12,
        "WAST": 2,
        "WAT": 1,
        "WEST": 1,
        "WET": 0,
        "WIB": 7,
        "WIT": 9,
        "WITA": 8,
        "WGST": -2,
        "WGT": -3,
        "WST": 8,
        "YAKT": 9,
        "YEKT": 5
    }
    # return value if key is found, else return passed parameter
    return shortcodes.get(tz_shortcode.upper(), tz_shortcode)

def process_client(client_socket):
    """
    Receives client request and sends timestamp
    
    :param client_socket: the client socket
    """
    # format client data as integer
    data = client_socket.recv(1024).decode("utf-8")
    try:
        print(f"Received '{data}'") # print data recieved form client
        timezone_offset = timezone_search(data) # check if client sent timezone shortcode
        adjusted_time = get_adjusted_time(timezone_offset)  # adjust time
        if adjusted_time:
            response = format_time(adjusted_time, timezone_offset)  # format response as dictionary
        else:
            response = {"error": "Invalid timezone format"}
    except ValueError:
        response = {"error": "Invalid input"}

    print(f"Sending '{response}'\n")
    client_socket.send(json.dumps(response).encode("utf-8"))    # respond with JSON

def main():
    """Main function to create server socket and listen for client connections"""
    host = '127.0.0.1'  # set for running locally
    port = 13000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))    # initialize socket
    server_socket.listen()
    print(f"Listening on {host}:{port}...")
    while True:
        client_socket, addr = server_socket.accept()    # accept client connection
        print(f"Connection from {addr}")
        with client_socket:
            process_client(client_socket)    # process client request

if __name__ == "__main__":
    main()
