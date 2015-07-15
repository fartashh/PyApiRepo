import cherrypy
from lib import mongo
from lib import utility
from bson.objectid import ObjectId
import time
import importlib
import uuid
import os
import json
from datetime import datetime,timedelta as td
import re
import markdown2
import csv




db = None


def set_db(_db):
    global db
    db = _db


def signup(data):
    try:
        utility.validate_signup_data(data)
        try:
            res = db.update_direct('users', where={'email': data['email']}, set_criteria=data)
            data['id'] = str(res.get('upserted', None))
            return dict(rescode='00', res_message='Success', result=data, timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : SignUP :Insertion', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))
    pass


def check_uniqueness(data):
    try:
        utility.validate_check_uniqueness_data(data)
        try:
            cursor = db.query_gen('users', criteria={data['filed']: data['value']})
            if cursor.next() == 0:
                return dict(rescode='00', res_message='Success', timestamp=int(time.time()))
            else:
                return dict(rescode='03', res_message='data existsh', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : uniqueness :Check', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=str(e), timestamp=int(time.time()))


def signin(data):
    try:
        utility.validate_signin_data(data)
        try:
            cursor = db.query_gen('users', criteria={'userName': data['userName'], 'password': data['password']})
            if cursor.next() == 1:
                res = cursor.next()
                res['id'] = str(res.pop('_id'))
                return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid userName or password', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : Signin', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def get_user_info(data):
    try:
        if (not all([data.get(x, False) for x in ['user_id']])):
            raise Exception("Failed argument validation: Compulsory field :: Missing value")
        try:
            cursor = db.query_gen('users', criteria={'_id': ObjectId(data['user_id'])})
            if cursor.next() == 1:
                res = cursor.next()
                res['id'] = str(res.pop('_id'))
                return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : get user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def create_consumer_key(data):
    try:
        if (not all([data.get(x, False) for x in ['user_id']])):
            raise Exception("Failed argument validation: Compulsory field :: Missing value")
        try:

            client_id = str(uuid.uuid1())
            client_secret = str(uuid.uuid1()).replace('-', '')
            consumer_key = str(uuid.uuid1()).replace('-', '')
            credentials = dict(client_id=client_id, client_secret=client_secret, consumer_key=consumer_key)
            res = db.update_direct('users', where={'_id': ObjectId(data['user_id'])}, set_criteria=credentials)

            return dict(rescode='00', res_message='Success', result=credentials, timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : SignUP :Insertion', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def reset_consumer_key(data):
    try:
        if (not all([data.get(x, False) for x in ['user_id']])):
            raise Exception("Failed argument validation: Compulsory field :: Missing value")
        try:
            consumer_key = str(uuid.uuid1()).replace('-', '')
            credentials = dict(consumer_key=consumer_key)
            res = db.update_direct('users', where={'_id': ObjectId(data['user_id'])}, set_criteria=credentials)
            return dict(rescode='00', res_message='Success', result=credentials, timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : SignUP :Insertion', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def load_apis(data):
    try:
        a = 1
        try:
            cursor = db.query_gen('apis')
            apis_count = cursor.next()
            if apis_count >= 1:
                apis = [cursor.next() for i in range(apis_count)]
                for api in apis:
                    api['id']=str(api.pop('_id'))
                    api['creation_time']=time.strftime("%Y-%m-%d", time.localtime(api.pop('creation_time')))
                return dict(rescode="00", resmessage='Success', result=apis, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : get user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))



def api_readme(data):
    try:
        a = 1
        try:
            cursor = db.query_gen('apis',criteria={'name':data['api_name']},projection={'tag_path':1,'_id':0})
            apis_count = cursor.next()
            if apis_count >= 1:
                api = cursor.next()
                path=os.getcwd()+'/'+ api['tag_path'].replace('.','/')+'/readme.md'
                with open(path) as f:
                    md=f.read()
                    html=markdown2.markdown(md)


                return dict(rescode="00", resmessage='Success', result=html, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : get user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def manage_api(method,data):
    try:
        utility.validate_manage_api_data(data)
        try:
            cursor = db.query_gen('users', criteria={'_id': ObjectId(data['user_id'])})
            if cursor.next() == 1:  # user exist
                cursor = db.query_gen('apis', criteria={'_id': ObjectId(data['api_id'])})
                if cursor.next() == 1:  # api exist
                    try:
                        if(method=='GET'):
                            res = db.update_direct('users', update_modifier='$pull',
                                                   where={'_id': ObjectId(data['user_id'])},
                                                   set_criteria={'apis': (data['api_id'],data['api_name'],False, data['api_title'] )})
                            res = db.update_direct('users', update_modifier='$addToSet',
                                                   where={'_id': ObjectId(data['user_id'])},
                                                   set_criteria={'apis': (data['api_id'],data['api_name'],True, data['api_title'])})
                        else:
                            res = db.update_direct('users', update_modifier='$pull',
                                                   where={'_id': ObjectId(data['user_id'])},
                                                   set_criteria={'apis': (data['api_id'],data['api_name'],True, data['api_title'])})

                            res = db.update_direct('users', update_modifier='$addToSet',
                                                   where={'_id': ObjectId(data['user_id'])},
                                                   set_criteria={'apis': (data['api_id'],data['api_name'],False, data['api_title'])})


                        return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
                    except Exception, e:
                        return dict(rescode='04', res_message='Exception : Update user apis',
                                    timestamp=int(time.time()))
                else:
                    return dict(rescode='04', res_message='Exception : Api does not exist', timestamp=int(time.time()))
            else:
                return dict(rescode='03', res_message='Exception : User does not exist', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : Geting user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def credit_request(data):
    # status 0: unapproved
    # status 1: approved
    # status 2: pending
    try:
        utility.validate_credit_request_data(data)
        try:
            cursor = db.query_gen('users', criteria={'_id': ObjectId(data['user_id'])})
            if cursor.next() == 1:  #user exist
                try:
                    data['amount']=float(data['amount'])

                    credit_report = dict(trid=utility.gen_id(), amount=data['amount'],
                                         time=int(time.time()), type='in', status=1)
                    res = db.update_direct('users', update_modifier='$addToSet',
                                           where={'_id': ObjectId(data['user_id'])},
                                           set_criteria={'credit.reports': credit_report})
                    # call payment gateway API

                    db.update_direct('users', update_modifier='$inc',
                                              where={'_id': ObjectId(data['user_id'])},
                                              set_criteria={'credit.amount': data['amount']})


                    return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
                except Exception, e:
                    return dict(rescode='04', res_message='Exception : update credit report',
                                timestamp=int(time.time()))
            else:
                return dict(rescode='03', res_message='Exception : User does not exist', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : Geting user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def load_credit(data):
    try:
        perpage = 25
        try:
            cursor = db.query_gen('users',criteria={'_id': ObjectId(data['user_id'])}, projection={'credit':1})
            if cursor.next() >= 1:
                credit= cursor.next()['credit']
                credit['reports']=[x for x in credit['reports'] if x['type']=='in']
                credit['reports'].sort(key=lambda x:x['time'],reverse=True)
                for rep in credit['reports']:
                    rep['time']=time.strftime("%Y-%m-%d  %H:%M", time.localtime(rep['time']))

                credit['report_count']=len(credit['reports'])
                page=data.get('page',1)
                credit['page']=page
                credit['reports']=credit['reports'][(page-1)*perpage:((page-1)*perpage)+perpage]



                return dict(rescode="00", resmessage='Success', result=credit, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : get user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))



def register_api(data, once = True):
    new_apis_config = []
    try:
        for root, subdirs, files in os.walk(os.getcwd() + '/apis'):
            if 'conf.json' in files:
                with open(root + '/conf.json') as f:
                    config = json.load(f)
                    config['creation_time'] = int(time.time())
                    new_apis_config.append(config)
                    f.close()
                    if once:
                        os.rename(root + '/conf.json', root + '/_conf.json')
    except Exception, e:
        print("Error in reading api config {}".format(e))

    for api_conf in new_apis_config:
        try:
            utility.validate_register_api_data(api_conf)
            try:
                cursor = db.query_gen('users', criteria={'_id': ObjectId(api_conf['creator_id'])})
                if cursor.next() == 1:  # user exist
                    api_conf['creator_name']=cursor.next()['userName']
                    try:
                        res = db.update_direct('apis', where={'name': api_conf['name']}, set_criteria=api_conf)
                        print "new api registerd ::{}".format(api_conf['name'])
                        # return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
                    except Exception, e:
                        return dict(rescode='04', res_message='Exception : Add api', timestamp=int(time.time()))
                else:
                    return dict(rescode='03', res_message='Exception : User does not exist', timestamp=int(time.time()))
            except Exception, e:
                return dict(rescode='02', res_message='Exception : Geting user info', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def get_usage_stat(data):
    try:
        perpage = 25
        try:
            cursor = db.query_gen('users',criteria={'_id': ObjectId(data['user_id'])}, projection={'credit':1,'api_requests':1,'apis':1})
            c=cursor.next()
            if c >= 1:
                user= cursor.next()
                reports=[]
                chart_data=[]
                chart_header=['day']
                chart_body=[]
                for api in user['apis']:

                    report={}
                    report['name']=api[1]
                    credit_reports=[r for r in user.get('credit',[]).get('reports',[]) if r.get('api_name')==api[1]]
                    report['total_request']=len(credit_reports)
                    report['total_request_cost']=sum([r['amount'] for r in credit_reports])
                    request_this_month=[r for r in credit_reports if time.gmtime(r['time']).tm_mon==time.gmtime(time.time()).tm_mon]
                    report['month_request']=len(request_this_month)
                    report['month_request_cost']=sum([r['amount'] for r in request_this_month])


                    api_chart_data=[]
                    credit_reports.sort(key=lambda x:x['time'])
                    if credit_reports:
                        chart_header.append(api[1])
                        start_date=datetime.fromtimestamp(credit_reports[0]['time'])
                        end_date=datetime.fromtimestamp(credit_reports[-1]['time'])

                        for i in range((end_date-start_date).days+1):
                            request_day=[]
                            _day=start_date+td(days=i)
                            request_day.append(_day.strftime('%d %b'))
                            request_day.append(len([r for r in credit_reports if datetime.fromtimestamp(r['time']).date()==_day.date()])/86400.)
                            api_chart_data.append(request_day)

                        report['api_chart_data']=api_chart_data



                    reports.append(report)

                for report in reports:
                    if report.get('api_chart_data',None):
                        if not chart_body:
                            chart_body=report['api_chart_data']
                        else:
                            for r in chart_body:
                                same_day_record=[d for d in report['api_chart_data'] if d[0]==r[0]]
                                if len(same_day_record):
                                    r.append(same_day_record[0][1])
                                else:
                                    r.append(0.000)
                            for d in report['api_chart_data']:
                                if not len([r for r in chart_body if r[0]==d[0]]):
                                    temp=[d[0]]
                                    temp.extend([0]*(len(chart_body[0])-2))
                                    temp.append(d[1])
                                    chart_body.append(temp)


                chart_data.append(chart_header)
                chart_body.sort(key=lambda x:x[0])
                chart_data.extend(chart_body)
                res={'chart_data':chart_data,'table_data':reports}



                return dict(rescode="00", resmessage='Success', result=res, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : '+str(e), timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))



def get_api_log(data):
    try:
        a = 1
        try:


            cursor = db.query_gen('logs',criteria={'api_name':data['api_name']},projection={'api_id':0,'_id':0,'user_id':0})
            logs_count = cursor.next()
            if logs_count>= 1:
                logs = [cursor.next() for i in range(logs_count)]
                for log in logs:
                    log['time']=time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(log.pop('time')))

                keys=['time','api_name','credit','credit_before_api_call','ip','request_line','rescode']
                temp_file_name=os.getcwd()+"/log_reports/"+ utility.gen_id()+'.csv'
                with open(temp_file_name,'wb') as f:
                    dict_writer=csv.DictWriter(f,keys)
                    dict_writer.writer.writerow(keys)
                    dict_writer.writerows(logs)



                return dict(rescode="00", resmessage='Success', result=temp_file_name, timestamp=int(time.time()))
            else:
                return dict(rescode="03", resmessage='Invalid user id', timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : get user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=e, timestamp=int(time.time()))


def call_api(request, url_map, app_db):
    data = request.params

    try:
        utility.validate_call_api_data(data)
        try:
            cursor = db.query_gen('users',
                                  criteria={'_id': ObjectId(data['user_id']), 'consumer_key': data['consumer_key']})
            if cursor.next() == 1:  # user exist
                user = cursor.next()

                try:
                    pt = request.path_info.split('?')[0]
                    url_endpoint = [v for k, v in url_map.items() if k.match(pt[4:])]
                    #cursor = db.query_gen('apis', criteria={'_id':ObjectId(data['api_id']) })
                    if url_endpoint and app_db.get(url_endpoint[0], None): # cursor.next() == 1:  # apis is exist
                        api = app_db.get(url_endpoint[0], None) #url_endpoint[0] # cursor.next()

                        if([v for v in api['url_pattern'] if re.match(v, pt[4:])]):
                            try:
                                module = importlib.import_module(api['tag_path']+'.api')
                                try:
                                    utility.is_user_authorized_to_call_api(user, api)
                                    try:
                                        [data.pop(x) for x in ['consumer_key','user_id']]
                                        res = module.execute(request.path_info, data)

                                        trid = utility.gen_id()
                                        cost_of_request = 0.00
                                        if (utility.is_it_free(user, api)):
                                            credit_report = dict(trid=trid, api_name=api['name'], amount=0.00,
                                                                 time=time.time(), type='out', status=1)
                                            earn_report = dict(trid=trid, api_name=api['name'], amount=0.00,
                                                               time=time.time())
                                        else:
                                            credit_report = dict(trid=trid, api_name=api['name'],
                                                                 amount=api['cost_per_request'], time=time.time(),
                                                                 type='out', status=1)
                                            earn_report = dict(trid=trid, api_name=api['name'],
                                                               amount=api['cost_per_request'], time=time.time())
                                            cost_of_request = api['cost_per_request']

                                        db.update_direct('users', update_modifier='$addToSet',
                                                     where={'_id': user['_id']},
                                                     set_criteria={'credit.reports': credit_report})

                                        db.update_direct('users', update_modifier='$inc',
                                                     where={'_id': user['_id']},
                                                     set_criteria={'credit.amount': cost_of_request * -1})

                                        db.update_direct('users', update_modifier='$push',
                                                     where={'_id': user['_id']},
                                                     set_criteria={'api_requests': {'api_id':str(api['_id']),'time':int(time.time())}})

                                        db.update_direct('users', update_modifier='$addToSet',
                                                     where={'_id': ObjectId(api['creator_id'])},
                                                     set_criteria={'earned.reports': earn_report})

                                        db.update_direct('users', update_modifier='$inc',
                                                     where={'_id': ObjectId(api['creator_id'])},
                                                     set_criteria={'earned.amount': cost_of_request})


                                        remain_credit = user['credit']['amount'] - cost_of_request


                                        return dict(rescode='00', res_message='Success', timestamp=int(time.time()),
                                                    api=api['name'],api_id=str(api['_id']),
                                                    credit_before_api_call="{0:.2f}".format(user['credit']['amount']),
                                                    credit="{0:.2f}".format(remain_credit), result=res)

                                    except Exception, e:
                                        return dict(rescode='09', res_message='Exception : api execution '+str(e),
                                                    timestamp=int(time.time()))
                                except Exception, e:
                                    return dict(rescode='08', res_message=str(e), timestamp=int(time.time()))
                            except Exception, e:
                                return dict(rescode='07', res_message='Exception : importing api',
                                            timestamp=int(time.time()))
                        else:
                            return dict(rescode='06', res_message='Exception : Given pattern doesnt match', hint=api['url_pattern'],
                                    timestamp=int(time.time()))

                    else:
                        return dict(rescode='05', res_message='Exception : Api does not exist',
                                    timestamp=int(time.time()))
                except Exception, e:
                    return dict(rescode='04', res_message='Exception : Getting API info', timestamp=int(time.time()))
            else:
                return dict(rescode='03', res_message='Exception : User does not exist or wrong consumer key',
                            timestamp=int(time.time()))
        except Exception, e:
            return dict(rescode='02', res_message='Exception : Getting user info', timestamp=int(time.time()))
    except Exception, e:
        return dict(rescode='01', res_message=str(e), timestamp=int(time.time()))









