def dynamic_import_from(name):

    components = name.split('.')
    try:
        mod = __import__('.'.join(components[:-1]))
        for comp in components[1:]:
            mod = getattr(mod, comp)
    except:
        raise ImportError(f"Could not import '{name}'. Please check your config file.")
    return mod