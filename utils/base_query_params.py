def get_selector(self, key):
    value = self.request.GET.get(key, None) or self.request.query_params.get(key, None)
    return value
