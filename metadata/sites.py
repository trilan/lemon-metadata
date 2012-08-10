from .options import ModelMetadata


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class MetadataSite(object):

    def __init__(self):
        self._registry = {}

    def register(self, model, model_metadata_class=None, **options):
        if not model_metadata_class:
            model_metadata_class = ModelMetadata

        if model in self._registry:
            raise AlreadyRegistered(
                u'The model %s already registered' % model.__name__)

        model_metadata = model_metadata_class(model, **options)
        model_metadata.enable()
        self._registry[model] = model_metadata

    def unregister(self, model):
        if model not in self._registry:
            raise NotRegistered(
                u'The model %s is not registered' % model.__name__)

        model_metadata = self._registry[model]
        model_metadata.disable()
        del self._registry[model]

    def unregister_all(self):
        for model in list(self._registry):
            self.unregister(model)


site = MetadataSite()
