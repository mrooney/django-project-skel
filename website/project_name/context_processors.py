def pluralize(count, string, plural=None):
    if count == 1:
        return u"%i %s" % (count, string)
    else:
        return u"%i %s" % (count, plural if plural else string+"s")

def processor(request):
    context = {
            'request': request,
            'pluralize': pluralize,
            'len': len,
            'str': str,
            'dir': dir,
    }
    return context

