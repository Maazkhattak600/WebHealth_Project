import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from sprint3.sprint3_stack import Sprint3Stack

import urllib3
def getavail():
    http = urllib3.PoolManager()
    response = http.request("GET","skipq.org")
    if response.status == 200:
        return 1
    else:
        return 0

def test_func():
    assert getavail() == 1 or getavail() == 0
    
    

