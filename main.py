import flask;
from flask import request, redirect, send_file, render_template
from dataclasses import dataclass 
from typing import *;
from time import time_ns;
import flask


@dataclass
class RequsetRecord:
    ip :str;
    unix:List[int];




NS_COEF = 10**9;
BUCKET:Dict[str, List[RequsetRecord]] = dict();
RATE_DURATION:int = 5*NS_COEF; #in ns
RATE_COUNT_LIMIT = 3; #in ns

def add_request_record(ip)->RequsetRecord:
    global BUCKET
    output:RequsetRecord = RequsetRecord(ip=ip, unix=time_ns());
    if ip not in BUCKET:
        BUCKET[ip] = [output,];
    else:
        BUCKET[ip].append(output);
    return output;


def get_rate_for_ip(ip:str)->int:
    output:int = 0;
    if ip not in BUCKET:
        return output;
    reqs:List[RequsetRecord] = BUCKET[ip];
    req:RequestRecord;
    current_unix:int = time_ns();
    for req in reqs:
        output += (current_unix - req.unix) <= RATE_DURATION;
    return output

def count_for_ip(ip:str)->int:
    if ip not in BUCKET:
        return None;
    return BUCKET[ip].__len__();


def is_ip_limited(ip:str)->bool:
    count:int = get_rate_for_ip(ip=ip);
    print(f"""
[DEBUG]:
    IP:{ip}
    visits in last {RATE_DURATION} secs:
        {count}
    total requests:
        {count_for_ip(ip)}

        """)
    return count >= RATE_COUNT_LIMIT;




app:flask.Flask = flask.Flask("rate limiter demo");


@app.before_request
def rate_limit_checker():
    print(request.url_rule);
    if request.url_rule == "/sorry":
        return None
    ip:str = request.remote_addr;

    req : RequestRecord = add_request_record(ip=ip);
    
    if is_ip_limited(ip=ip):
        return render_template("sorry.html", RATE_DURATION=RATE_DURATION/NS_COEF)
    else:
        return None

    


@app.route("/pack_1")
def hh_test():
    return send_file("pack_1.zip");


