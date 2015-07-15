#Wiki
This API returns the text from Wikipedia based on paragraphs.There 4 parameter you can pass

+ `url`: Wikipedia url e.g. `http://en.wikipedia.org/wiki/Joseph_von_Fraunhofer`
+ `s`: Skip value, How many paragraph from begining must be skiped, by default is `0`,
+ `n`: Number of paragraphs after the given skip point, by default is `1`

#Example
    `/wiki?url= http://en.wikipedia.org/wiki/Joseph_von_Fraunhofer&s=3&n=2`

#Return:
    A dictionary like this:

```            {
                'url':'',
                'n':2,
                's':0,
                'wikis': [ 'soem text', 'some text',..]
            }```