from django import forms

from bson.objectid import ObjectId

from .models import Book, Dimention, Address

class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        
        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Book
        fields = ('name','content','category', 'dimention','addresses', 'tags')

    def is_valid(self):

        self.data._mutable = True
        self.data['category'] = ObjectId(self.data['category'])
        self._custom_valid_tags()

        valid = super(BookForm, self).is_valid()

        self._custom_valid_dimention()
        self._custom_valid_addresses()
        
        return len(self.errors) == 0

    def save(self,commit=True):

        instance = super(BookForm,self).save(commit=False)
        print(instance.dimention)
        print(self.data)
        instance.dimention = self.data['dimention']

        if instance._id:
            book = Book.objects.get(pk=ObjectId(instance._id))
            #self.data['dimention']['_id'] = book.dimention['_id']
            instance.addresses = book.addresses
            instance.addresses.append(self.data['addresses'][0])
            instance.tags.set(self.data.getlist('tags'))
        else:
            instance.addresses = self.data['addresses']

        if(commit):
            instance.save()

        return instance

    def _custom_valid_tags(self):
        #print(self.data.getlist('tags'))
        self.data.setlist('tags',list(map(lambda tid: ObjectId(tid),self.data.getlist('tags'))))
        #print(self.data.getlist('tags'))


    def _custom_valid_dimention(self):

        if 'dimention' in self.errors:
            del self.errors['dimention']

            #if len(self.errors) == 0:
                #sin errores

        try:
            self.data['dimention'] = Dimention(**{ 
                '_id': ObjectId(),
                'x' : int(self.data['dimention-x']),
                'z' : int(self.data['dimention-z']),
                'y' : int(self.data['dimention-y'])
            })
        except ValueError:
            self.add_error('dimention', 'Al menos una dimención es inválida')
            return False

        """del self.data['dimention-x']
        del self.data['dimention-z']
        del self.data['dimention-y']"""

        return True
            #return False
            #si tenemos errores

    def _custom_valid_addresses(self):

        if 'addresses' in self.errors:
            del self.errors['addresses']

            #if len(self.errors) == 0:
                #sin errores

        if self.data['addresses-0-direction'].strip() == "" or self.data['addresses-0-country'].strip() == "":
            self.add_error('addresses', 'Debes de indicar la dirección completa')
            return False

        self.data['addresses'] = [Address(**{
                '_id' : ObjectId(),
                'country' :self.data['addresses-0-country'].strip(),
                'direction' :self.data['addresses-0-direction'].strip(),
            }
                )
                ]

        del self.data['addresses-0-direction']
        del self.data['addresses-0-country']

        return True
            #return False
            #si tenemos errores