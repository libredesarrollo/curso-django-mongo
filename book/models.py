from djongo import models
from django import forms

class Base(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255)

    @property
    def pk(self):
        return self._id

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Dimention(models.Model):
    _id = models.ObjectIdField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()


class DimentionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DimentionForm, self).__init__(*args, **kwargs)
        
        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Dimention
        fields = ('x','y','z')


class Category(Base):
    class Meta:
        verbose_name_plural = "Categories"

class Address(models.Model):
    _id = models.ObjectIdField()
    direction = models.TextField()
    country = models.CharField(max_length = 20)

class Tag(Base):
    pass

class Book(Base):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dimention = models.EmbeddedField(
        model_container=Dimention,
        model_form_class=DimentionForm
    )
    addresses = models.ArrayField(
        model_container=Address
    )
    tags = models.ManyToManyField(
        Tag,
        through='Taggables',
        through_fields=('book','tag')
    )

class Taggables(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)