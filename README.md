Django Markdown Form offers a way to fill form using Markdown meta-data.
More information about markdown and meta-data in the reference section.

## Simple form

Start by creating a django form with a MarkdownField named 'markdown'.
The name of this form is mandatory.

The form must be decorated with markdown_form.
This decorator will fill other inputs according to the markdown meta-data.

    :::python
    from django import forms
    from markdown_forms.forms import markdown_form
    from markdown_form.fields import MarkdownField
    
    @markdown_form
    class MarkdownExampleForm(Form):
        foo = forms.CharField()
        bar = forms.CharField()
        markdown = MarkdownField()

MarkdownField extends django.forms.FileField, so you need to feed it with an UploadedFile.
If the uploaded markdown document contains the meta-data foo and bar, these meta-data will be directly injected into the foo and bar field of the form.

    :::python
    from django.core.files.uploadedfile import SimpleUploadedFile

    markdown_file_content = """foo: this is foo
    bar: this is bar

    And this is the actual content of the markdown file.
    """

    uploaded_file = SimpleUploadedFile('file.md', markdown_file_content)
    form = MarkdownExampleForm(files={'markdown': uploaded_file})

    form.full_clean()

After the form.full_clean(), the form cleaned_data attribute will contain:

    :::python
    {
        u'foo': u'this is foo',
        u'bar': u'this is bar',
        u'markdown': u'<p>And this is the actual content of the markdown file.</p>'
    }


## Extract meta as list

Some markdown meta-data can be used as list.
The values of the tags need to be comma separated or put on different lines.

Last thing to do is to tell the MarkdownField that some fields need to be extracted as a list.
This is done with the meta_list constructor argument.
It is a list containing the name of the meta-data tags to extract as list.


## Overriding markdown tags

If some value are passed to the form constructor that matches some tags name, they will be used instead of the meta-data value.
For example, il ne previous snippet, replacing the form creation by.

    :::python
    form = MarkdownExampleForm(data={'foo': 'overriden foo'},
                                     'files'={'markdown': uploaded_file})

Will result in the following cleaned data:

    :::python
    {
        u'foo': u'overriden foo',
        u'bar': u'this is bar',
        u'markdown': u'<p>And this is the actual content of the markdown file.</p>'
    }


## Markdown Third-party Extensions

You can inject Markdown third-party extensions and it's configuration in the MarkdownField.

TODO


## Model Form

markdown_form cann also decorate some django.forms.ModelForm.
However, if the model bint to the form contains a field intended to contain some markdown,
the markdown form field must be overriden with a MarkdownField.

    :::python
    from django.db import models
    from django import forms
    from markdown_form.forms import markdown_form
    from markdown_form.field import MarkdownField

    class ExampleModel(models.Model):
        foo = models.CharField(max_length=255)
        bar = models.CharField(max_length=255)
        # better use a TextField than a CharField
        markdown = models.TextField()

    @markdown_form
    class ExampleMarkdownModelForm(forms.ModelForm):
        # override defaut forms.TextField
        markdown = MarkdownField()


## Django Rest Framework support

Django markdown-form application also support the Django REST Framework.

TODO


## References
  + https://daringfireball.net/projects/markdown/ - Markdown website
  + http://pythonhosted.org/Markdown/extensions/meta_data.html - Markdown meta
  + http://www.django-rest-framework.org/ - Django Rest Framework
