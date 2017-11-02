from better_choices import Choices


class ChoicesMeta(type):

    # Restrict types a bit so we dont create a
    ALLOWED_TYPES = (int, long, float, str, unicode, bool, tuple)

    def __new__(cls, name, bases, dct, **kwargs):
        """
            Extract triplet information from the class definition itself,
            and then return a Choices() object instead.
        """

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

        # sort it, so we can guarantee an order,
        # and the django migrations dont get confused thinking the choices changed.
        choices = sorted(choices)

        return Choices(*choices)