from django.db import models, transaction


class Todo(models.Model):
    title   = models.CharField(max_length=200, db_index=True)
    text    = models.TextField()
    rank    = models.IntegerField(db_index=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f'{self.title} - {self.text} - ({self.rank}) - {self.pk}'

    @classmethod
    def create(cls, title=title, text=text):
        cls.objects.create(
                title=title,
                text=text,
                rank=cls.highest_rank + 1)

    @classmethod
    @property
    def highest_rank(cls):
        return int(cls.objects.all().aggregate(models.Max('rank'))['rank__max'] or 0)


    def rerank(self, new_rank):
        with transaction.atomic():
            if self.rank == new_rank:
                return
            elif new_rank < self.rank:
                delta = 1
                todos = type(self).objects.filter(rank__gte=new_rank).filter(rank__lte=self.rank)
            else:
                delta = -1
                todos = type(self).objects.filter(rank__gte=self.rank).filter(rank__lte=new_rank)
            for todo in todos:
                if todo.rank == self.rank:
                    todo.rank = new_rank
                else:
                    todo.rank += delta

            type(self).objects.bulk_update(todos, fields=('rank',))

    @classmethod
    def rerank_by_list(cls, reranked):
        todos = [todo.pk for todo in cls.objects.all()]
        for i, samples in enumerate(zip(todos, reranked)):
            if not samples[0] == samples[1]:
                new_i_index = reranked.index(todos[i])
                if new_i_index > i + 1:
                    #down
                    cls.objects.get(pk=todos[i]).rerank(new_i_index+1)
                else:
                    #up or swap
                    cls.objects.get(pk=reranked[i]).rerank(new_i_index)
                break

    def delete(self, *arg, **kwargs):
        self.rerank(type(self).highest_rank)
        super(type(self), self).delete(*arg, **kwargs)
