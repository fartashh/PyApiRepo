

import cherrypy
from cherrypy.lib.static import serve_file
import config
from lib import shared
import api_repository
from uuid import uuid1
import time
import json
import timeit

shared.start()
db=shared.DB
api_repository.set_db(db)
url_map = {}
app_db = {}




class Root(object):
    @cherrypy.expose
    def index(self):
        return open(r"./views/app.html",'rb').read()

    #user signup
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def signup(self):
        try:
            data=cherrypy.request.json
            res = api_repository.signup(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res

    #check_uniqueness
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def check_uniqueness(self):
        try:
            data=cherrypy.request.json
            res = api_repository.check_uniqueness(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res


    #user signin
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def signin(self):
        try:
            data=cherrypy.request.json
            res = api_repository.signin(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res



    #user get_user_info
    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def get_user_info(self,*args,**kwargs):
        try:
            data=cherrypy.request.params
            res = api_repository.get_user_info(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res


    #Create new consumer key
    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def create_consumer_key(self,*args,**kwargs):
        try:
            data=cherrypy.request.params
            res = api_repository.create_consumer_key(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res

    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def reset_consumer_key(self,*args,**kwargs):
        try:
            data=cherrypy.request.params
            res = api_repository.reset_consumer_key(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")
        return res



    #user Manage api he wants to use add or delete
    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def manage_api(self,**kwargs):
        try:
            method=cherrypy.request.method
            return api_repository.manage_api(method,kwargs)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")

    #user request for credit
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def credit_request(self):
        try:
            data=cherrypy.request.json
            return api_repository.credit_request(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")


    #user get report
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def get_usage_stat(self,**kwargs):
        try:
            data=cherrypy.request.json
            return api_repository.get_usage_stat(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")

    #get_api_log
    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    def get_api_log(self,**kwargs):
        try:
            data=cherrypy.request.json
            res= api_repository.get_api_log(data)
            return serve_file(res['result'], "application/x-download", "attachment")
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")




    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def load_apis(self):
        try:
            return api_repository.load_apis('')
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")




    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def api_readme(self,**kwargs):
        try:
            return api_repository.api_readme(kwargs)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")

    @cherrypy.expose
    def help(self, **kwargs):
        try:
            html = api_repository.api_readme(kwargs)['result']
            return '''<html><head><link href="../static/css/lib/bootstrap.min.css" rel="stylesheet"></head><body><div class='container'>{}</div></body></html>'''.format(html)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")


    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def load_credit(self):
        try:
            data=cherrypy.request.json
            return api_repository.load_credit(data)
        except Exception,e:
            print("Very Bad Exception ::{}".format(e))
            raise cherrypy.HTTPError(666, "General Exception")


    @cherrypy.expose
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def api(self,*args,**kwargs):
        start = timeit.default_timer()
        res=api_repository.call_api(cherrypy.request, url_map, app_db)
        stop = timeit.default_timer()


        res['run_time']=stop-start
        data=cherrypy.request
        request_transaction=dict(
            ip=cherrypy.request.remote.ip,
            api_name=res.get('api','NA'),
            api_id=res.get('api_id','NA'),
            user_id=kwargs.get('user_id'),
            request_line=json.dumps(cherrypy.request.request_line),
            time=int(time.time()),
            credit=res.get('credit','NA'),
            credit_before_api_call=res.get('credit_before_api_call','NA'),
            rescode=res.get('rescode','NA')
        )

        db.update_direct('logs',where={'time':'1'},set_criteria=request_transaction)
        res.pop('credit_before_api_call',None)
        res.pop('api_id',None)
        return res






def main():
    global url_map, app_db
    api_repository.register_api({}, once=False)
    import re

    apis = list(db.db.apis.find({}))
    url_map = {re.compile(pt, re.IGNORECASE):v['_id'] for v in apis for pt in (v['url_pattern']+['/'+v['name']]) }
    app_db = {v['_id']:v for v in apis}
    app=Root()
    cherrypy.config.update(config.cherrypy_conf_update)
    cherrypy.quickstart(app, '/', config.cherrypy_conf)


if __name__ == '__main__':
    main()


    pass
