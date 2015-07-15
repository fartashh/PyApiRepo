__author__ = 'Fartash'
import json
import urllib




def execute(path, params):


    try:
      query = urllib.urlencode({'q': path.split()[-1]})
      url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
      search_response = urllib.urlopen(url)
      search_results = search_response.read()
      results = json.loads(search_results)
      data = results['responseData']


      res=dict(Total_results=data['cursor']['estimatedResultCount'],
               hits = data['results'],
               more_results=data['cursor']['moreResultsUrl']
               )

      return res




    except Exception, e:
        return {'search':'Error (' + str(e) + ')'}
