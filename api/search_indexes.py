# from haystack import indexes
# from .models import Job
#
# class JobIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     title = indexes.CharField(model_attr="title")
#     organization = indexes.CharField(model_attr="employer__organization")
#
#     def get_model(self):
#         return Job
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
