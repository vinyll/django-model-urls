class DummyModel(object):

    def __init__(self, name="dummy-model", ref=None):
        self.pk = 8
        self.name = name
        self.ref = ref

    @property
    def subref(self):
        return self.ref.name
