def make_it_cache(res, etag):
    res.headers['Cache-Control'] = 'public; max-age:8640000'
    res.headers['eTag'] = etag
    return res

