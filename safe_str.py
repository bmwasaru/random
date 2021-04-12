def safestr(obj, encoding="utf-8"):
    if obj and hasattr(obj, "__next__"):
        return [safestr(i) for i in obj]
    else:
        return str(obj)

