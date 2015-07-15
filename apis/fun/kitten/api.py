__author__ = 'Fartash'
from pyquery import PyQuery
import re




def execute(path, params):


    try:

        if re.match("/kitten/([0-9]+)/([0-9]+)$",path[4:]):
            params=path.split('/')
            q = PyQuery('http://placekitten.com/g/{}/{}'.format(params[-2],params[-1]))

        else:
            q = PyQuery('http://placekitten.com/')

        imgs=q('img')
        kittens=[q(i).attr('src') for i in imgs]
        return  kittens

    except Exception, e:
        return {'kitten':'Error (' + str(e) + ')'}
