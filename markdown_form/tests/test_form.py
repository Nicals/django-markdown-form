from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import TestCase

from markdown_form.fields import MarkdownField
from markdown_form.forms import markdown_form


@markdown_form
class MarkdownSampleForm(forms.Form):
    title = forms.CharField()
    markdown = MarkdownField()


class DummyModel(models.Model):
    title = models.CharField(max_length=255)
    markdown = models.TextField()


@markdown_form
class DummyModelForm(forms.ModelForm):
    markdown = MarkdownField()

    class Meta:
        model = DummyModel


class MarkdownFieldTestCase(TestCase):
    MD_TEXT = """Title: ham title
Tags: ham, spam
      foo
      bar, baz

text text text
"""

    def test_meta_extraction(self):
        md_file = SimpleUploadedFile('test.md', self.MD_TEXT)

        md_field = MarkdownField(meta_list=['tags'])
        md_field.clean(md_file)

        self.assertDictEqual(md_field.md_meta, {u'title': u'ham title',
                                                u'tags': [u'ham', u'spam',
                                                          u'foo', u'bar',
                                                          u'baz']})

    def test_meta_validation(self):
        md_file = SimpleUploadedFile('test.md', self.MD_TEXT)

        md_field = MarkdownField()
        with self.assertRaises(ValidationError):
            md_field.clean(md_file)

    def test_convert(self):
        md_file = SimpleUploadedFile('test.md', "text text")

        md_field = MarkdownField(md_file)
        data = md_field.clean(md_file)

        self.assertEquals(data, u'<p>text text</p>')


class MarkdownFormTestCase(TestCase):
    def test_markdown(self):
        md_file = SimpleUploadedFile('test.md', "Title: foobar\n\ntext text")
        form = MarkdownSampleForm({}, {'markdown': md_file})
        form.full_clean()

        self.assertEquals(form.cleaned_data['markdown'], u'<p>text text</p>')

    def test_data_dispatch(self):
        @markdown_form
        class MarkdownSampleForm(forms.Form):
            title = forms.CharField()
            markdown = MarkdownField()

        md_file = SimpleUploadedFile('test.md', "Title: foobar\n\ntext text")

        # test markdown value
        form = MarkdownSampleForm({}, {'markdown': md_file})
        form.fields['title'] = forms.CharField()
        form.full_clean()

        self.assertEquals(form.cleaned_data['title'], u'foobar')

        # override markdow value
        form = MarkdownSampleForm({'title': u'ham spam'},
                                  {'markdown': md_file})
        form.full_clean()

        self.assertEquals(form.cleaned_data['title'], u'ham spam')


class MarkdownModelTestCase(TestCase):
    def test_markdown(self):
        md_file = SimpleUploadedFile('test.md', "Title: foobar\n\ntext text")
        form = DummyModelForm({}, {'markdown': md_file})
        form.full_clean()

        dummy_instance = form.save(commit=False)
        self.assertEquals(form.cleaned_data['title'], 'foobar')
        self.assertEquals(dummy_instance.title, 'foobar')
