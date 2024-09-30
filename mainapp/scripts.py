from datetime import date

#Create your views here.
def success(msg):
    # Create a dictionary named 'response' with two key-value pairs
    response={
        'status_code':0, # Key 'status_code' with value 0
        'data':msg       # Key 'data' with value 'msg' (the input parameter)
    }
    # Return the 'response' dictionary
    return response

def error(msg):
    # Create a dictionary with error details
    response={
        'status_code':1, # Status code indicating error
        'data':msg  # Error message
    }
    # Return the 'response' dictionary
    return response

def unique_id(pre, last_id):
    today1=date.today()
    today = today1.strftime("%d%m%y")
    last_ids = int(last_id) + 1
    if len(str(last_ids)) == 1:
        id = pre + today + '00' + str(last_ids)
    elif len(str(last_ids)) == 2:
        id = pre + today + '0' + str(last_ids)
    else:
        id = pre + today + str(last_ids)
    return id