__author__ = 'Fartash'
from pyquery import PyQuery



def execute(path, params):
    try:
        if path.endswith('/help'):
            return {'help':'''This API returns the text from Wikipedia based on paragraphs. There 4
        parameter you can pass.
            URL: Wikipedia url e.g. http://en.wikipedia.org/wiki/Joseph_von_Fraunhofer
            s: Skip value, How many paragraph from begining must be skiped, by default is 0,
            n: Number of paragraphs after the given skip point, by default is 1

        Example
            /wiki?url= http://en.wikipedia.org/wiki/Joseph_von_Fraunhofer&s=3&n=2

        Return:
            A dictionary like this:
                {
                    'url':'',
                    'n':2,
                    's':0,
                    'wikis': [ 'soem text', 'some text',..]
                }'''}
        url = params.get('url', None)
        if url:
            q = PyQuery(url)
            pTags = q('p')
            wikis = [q(x).text() for x in pTags if q(x).text()][ int(params.get('s', 0)):int(params.get('s', 0))+int(params.get('n', 1))]
            params['wikis'] = wikis
            return params
        pass
    except Exception, e:
        return {'wiki':'Error (' + str(e) + ')'}
    return ''

print execute('', {'url':'http://en.wikipedia.org/wiki/Joseph_von_Fraunhofer', 'n':1, 's':0})