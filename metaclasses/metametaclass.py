from better_choices import Choices


class ChoicesMetaMeta(type):

    PROXIED_METHODS = ['__len__', '__iter__', '__getattr__', '__getitem__', '__eq__', '__contains__']

    def __new__(cls, name, bases, dct):
        """
            This method will take care of building/assembling ChoicesMeta.
            We want to add the magic methods dinamically to its definition.
        """

        # build a dictionary of proxies to use.
        proxies = {}

        # iterate thru the methods we want to proxy
        for method_name in ChoicesMetaMeta.PROXIED_METHODS:

            # a closure for our proxy
            def _proxy(_method_name):

                # the method that will get injected into the class
                def proxy(cls, *args, **kwargs):

                    choices_obj = cls.__dict__['choices_obj']

                    method = getattr(choices_obj, _method_name)

                    return method(*args, **kwargs)

                return proxy

            proxies[method_name] = _proxy(method_name)

        # add our proxies to the class
        dct.update(proxies)

        # create the class and return it
        return type(name, bases, dct)


class ChoicesMeta(type):

    __metaclass__ = ChoicesMetaMeta

    ALLOWED_TYPES = (int, long, float, str, unicode, bool, tuple)

    def __init__(cls, name, bases, dct, **kwargs):
        """
            Extract triplet information from the class definition itself,
            and then return a Choices() object instead.
        """
        super(ChoicesMeta, cls).__init__(name, bases, dct)

        # list of triplets
        choices = []

        # iterate thru the attributes defined in the class
        for attr_name, attr_val in dct.iteritems():

            # dont mess with "private" attributes, or attributes whose value is not allowed
            if attr_name.startswith('__') or type(attr_val) not in ChoicesMeta.ALLOWED_TYPES:
                continue

            # if the attribute value is a tuple with length 2, then we have a verbose name.
            # if its not, then use the attribute name as the verbose name.
            if isinstance(attr_val, tuple):
                if len(attr_val) != 2:
                    raise ValueError(
                        'Tuple values for Choices must have 2 elements, in the format (db_value, description)'
                    )
                choices.append((attr_val[0], attr_name, attr_val[1]))
            else:
                choices.append((attr_val, attr_name, attr_name))

            # __getattr__ Called when an attribute lookup has not found the attribute in the usual places.
            delattr(cls, attr_name)

        # sort it, so we can guarantee an order,
        # and the django migrations dont get confused thinking the choices changed.
        choices = sorted(choices)

        cls.choices_obj = Choices(*choices)
        return

    # we will keep __repr__ as to show the name of the class, we dont actually want to delegate it.
    def __repr__(cls):
        return '{}({})'.format(
            cls.__name__, ', '.join((repr(i) for i in cls.choices_obj._triples))
        )