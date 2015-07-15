import cherrypy
import os


cherrypy_conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    # '/api': {
    #     'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    #     'tools.response_headers.on': True,
    #     'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    # },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    },
    '/views': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './views'
    }
}

cherrypy_conf_update = {
    'engine.autoreload.on': False,
    'tools.sessions.on': False,
    # 'server.socket_host': public_ip,
    'server.socket_port': 8899,
    'log.screen': True,
}