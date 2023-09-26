"""Singleton type for models."""

__all__ = ["SingletonMeta"]


class SingletonMeta(type):
    """The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.

    Examples:
        ::

            >>> class X(dict, metaclass=SingletonMeta):
            ...     ...
            >>> Xn = X()
            >>> Xn["__all__"] = ["SomeClass"]
            >>> Xp = X()
            >>> print(Xp.values())
            dict_values([['SomeClass']])

    Notes:
        The Singleton metaclass defines the `__call__` method, which allows
        the class instance to be called as a function. The important part of
        this method is the use of the `cls` argument, which refers to the
        class itself. Thereby, an instance of the class can be created and
        returned without explicitly calling the constructor.

    Warnings:
        #. The Singleton class can be implemented in different ways in Python.
           Some possible methods include: base class, decorator, metaclass.
           We will use the metaclass because it is best suited for this purpose.
        #. **The Singleton class does not allow you to create multiple instances
           of the same class.**
        #. **If your class is a subclass of a Singleton class, then it will also
           be a Singleton class.**
        #. **If you want to create a Singleton class, then you need to inherit
           from the SingletonMeta metaclass.**
    """

    #: dict: Instances of the singleton class.
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Possible changes to the value of the `__init__` argument do not
        affect the returned instance."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
