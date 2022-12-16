
class DatabaseSingleton(type):
    def __init__(self, name, bases, dic):
        self.__single_instance = None
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        if cls.__single_instance:
            return cls.__single_instance
        single_object = cls.__new__(cls)
        single_object.__init__(*args, **kwargs)
        cls.__single_instance = single_object
        return single_object