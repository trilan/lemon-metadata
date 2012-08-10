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


site = MetadataSite()
