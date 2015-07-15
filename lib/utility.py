from uuid import uuid1
import time

def gen_id():
    return str(str(uuid1()).replace('-',''))

def validate_signup_data(data):
    compulsory_field=['userName','email','firstName','lastName','password']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")


def validate_check_uniqueness_data(data):
    compulsory_field=['filed','value']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")


def validate_signin_data(data):
    compulsory_field=['userName','password']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")


def validate_manage_api_data(data):
    compulsory_field=['user_id','api_id']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")


def validate_credit_request_data(data):
    compulsory_field=['user_id','amount']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")

def validate_register_api_data(data):
    compulsory_field=['name','creator_id','tag_path','description','version']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")

def validate_call_api_data(data):
    compulsory_field=['user_id','consumer_key']
    if(not all([data.get(x,False) for x in compulsory_field])):
        raise Exception("Failed argument validation: Compulsory field :: Missing value")


def is_user_authorized_to_call_api(user, api):
    #check api is in stand bax
    if api['is_in_sandbox']:
        raise Exception("UnAuthorized api is in sandbox") if api['creator']!=str(user['_id']) else True
    else:
        count_of_user_request_in_this_month=len([r for r in user.get('api_requests',[]) if r['api_id']==str(api['_id']) and time.gmtime(r['time']).tm_mon==time.gmtime(time.time()).tm_mon])
        if count_of_user_request_in_this_month>=api['monthly_free_request'] and user['credit'].get('amount',0)<api['cost_per_request']:
            raise Exception("UnAuthorized user request exceed of free request and there is no sufficient credit")

def is_it_free(user, api):
    count_of_user_request_in_this_month=len([r for r in user.get('api_requests',[]) if r['api_id']==str(api['_id']) and time.gmtime(r['time']).tm_mon==time.gmtime(time.time()).tm_mon])
    if count_of_user_request_in_this_month>=api['monthly_free_request']:
        return False
    return True