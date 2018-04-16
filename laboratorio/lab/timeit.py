import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_nome', method.__name__.upper())
            kw['log_time'][name] = int((te - ts))
        else:
            print('%r %.3f s' % (method.__name__, (te - te)))    
        return result
    return timed