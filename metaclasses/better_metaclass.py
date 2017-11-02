from better_choices import Choices


class ChoicesMeta(type):

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

    # delegate the magic methods and operators to the Choices instance
    def __len__(cls):
        return len(cls.choices_obj)

    def __iter__(cls):
        return iter(cls.choices_obj)

    def __getattr__(cls, attname):
        return getattr(cls.choices_obj, attname)

    def __getitem__(cls, key):
        return cls.choices_obj[key]

    def __eq__(cls, other):
        if isinstance(other, cls.__class__):
            return cls.choices_obj == other.choices_obj
        return False

    def __contains__(cls, item):
        return item in cls.choices_obj

    def __repr__(cls):
        return '{}({})'.format(
            cls.__name__, ', '.join((repr(i) for i in cls.choices_obj._triples))
        )
