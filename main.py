import flask;
from flask import request, redirect, send_file
from dataclasses import dataclass 
from typing import *;
from time import time_ns;
import flask


@dataclass
class RequsetRecord:
    ip :str;
    unix:List[int];





BUCKET:Dict[str, List[RequsetRecord]] = dict();
RATE_DURATION:int = 3600;
RATE_COUNT_LIMIT = 10;

def add_request_record(ip)->RequsetRecord:
    global BUCKET
    output:RequsetRecord = RequsetRecord(ip=ip, unix=time_ns());
    BUCKET[ip] = (output);
    return output;


def count_for_ip(ip:str)->int:
    output:int = 0;
    if ip not in BUCKET:
        return output;
    reqs:List[RequsetRecord] = BUCKET[ip];
    req:RequestRecord;
    current_unix:int = time_ns();
    for req in reqs:
        output += current_unix - req.unix >= RATE_DURATION;
    return output


def is_ip_limited(ip:str)->bool:
    return count_for_ip(ip=ip) >= RATE_COUNT_LIMIT;




app:flask.Flask = flask.Flask("rate limiter demo");


@app.before_request
def rate_limit_checker():
    print(request.url_rule);
    if request.url_rule == "/sorry":
        return None
    ip:str = request.remote_addr;
    req : RequestRecord = add_request_record(ip=ip);
    
    if is_ip_limited:
        return "you are being rate limited!";
    else:
        return None

    


@app.route("/test")
def hh_test():
    return send_file("./test.txt");