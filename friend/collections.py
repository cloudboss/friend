def select_dict(coll, key, value):
    """
    Given an iterable of dictionaries, return the dictionaries
    where the values at a given key match the given value.
    If the value is an iterable of objects, the function will
    consider any to be a match.

    This is especially useful when calling REST APIs which
    return arrays of JSON objects. When such a response is
    converted to a Python list of dictionaries, it may be
    easily filtered using this function.

    :param iter coll: An iterable containing dictionaries
    :param obj key: A key to search in each dictionary
    :param value: A value or iterable of values to match
    :type value: obj or iter
    :returns: A list of dictionaries matching the query
    :rtype: list

    :Example:

    ::

      dicts = [
          {'hi': 'bye'},
          {10: 2, 30: 4},
          {'hi': 'hello', 'bye': 'goodbye'},
      ]

      matches = select(dicts, 'hi', 'bye')
      # Returns [{'hi': 'bye'}]

      matches = select(dicts, 'hi', ('bye', 'hello'))
      # Returns [{'hi': 'bye'}, {'hi': 'hello', 'bye': 'goodbye'}]
    """
    if getattr(value, '__iter__', None):
        iterable = value
    else:
        iterable = [value]
    return [v for v in coll if key in v and v[key] in iterable]
