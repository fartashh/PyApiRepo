__author__ = 'Fartash'



def execute(path, params):
    return {'t':444,'average': sum([int(x) for x in params.values()])/float(len(params))}
