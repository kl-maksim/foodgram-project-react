from rest_framework import viewsets, mixins


class ViewSetMixin(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pass
