from rest_framework import mixins, viewsets


class ViewSetMixin(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pass
