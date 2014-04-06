from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import TestCase

from rest_framework.fields import CharField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer, ModelSerializer

from markdown_form.rest.serializers import markdown_rest_serializer
from markdown_form.rest.fields import MarkdownField


class DummyModel(models.Model):
    title = models.CharField(max_length=255)
    markdown = models.TextField()


@markdown_rest_serializer
class MarkdownSampleSerializer(Serializer):
    title = CharField()
    markdown = MarkdownField()


@markdown_rest_serializer
class MarkdownSampleModelSerializer(ModelSerializer):
    markdown = MarkdownField()

    class Meta:
        model = DummyModel
        fields = ('title', 'markdown')


class RestMarkdownFieldTestCase(TestCase):
    MD_TEXT = """title: ham title
tags: ham, spam
      foo
      bar, baz

text text text
"""

    def test_meta_extraction(self):
        md_file = SimpleUploadedFile('test.md', self.MD_TEXT)

        md_field = MarkdownField(meta_list=['tags'])
        data = md_field.from_native(md_file)

        self.assertEquals(data, u'<p>text text text</p>')
        self.assertDictEqual(md_field.md_meta, {u'title': u'ham title',
                                                u'tags': [u'ham', u'spam',
                                                          u'foo', u'bar',
                                                          u'baz']})

    def test_meta_validation(self):
        """Test if trying to extract a list without specifying it

        """
        md_file = SimpleUploadedFile('test.md', self.MD_TEXT)

        md_field = MarkdownField()

        with self.assertRaises(ValidationError):
            md_field.from_native(md_file)


class RestMarkdownSerializerTestCase(TestCase):
    def test_markdown(self):
        md_file = SimpleUploadedFile('test.md', 'Title: foobar\n\ntext text')
        serializer = MarkdownSampleSerializer(data={},
                                              files={'markdown': md_file})

        self.assertTrue(serializer.is_valid())

        self.assertEquals(serializer.data['markdown'], u'<p>text text</p>')
        self.assertEquals(serializer.data['title'], u'foobar')

    def test_field_override(self):
        md_file = SimpleUploadedFile('test.md', 'Title: foobar\n\ntext text')
        serializer = MarkdownSampleSerializer(data={'title': 'overriden'},
                                              files={'markdown': md_file})

        self.assertTrue(serializer.is_valid())

        self.assertEquals(serializer.data['title'], u'overriden')


class RestMarkdownModelSerializerTestCase(TestCase):
    def test_markdown(self):
        md_file = SimpleUploadedFile('test.md', 'Title: foobar\n\ntext text')
        serializer = MarkdownSampleModelSerializer(data={},
                                                   files={'markdown': md_file})

        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.object.title, u'foobar')
        self.assertEquals(serializer.object.markdown, u'<p>text text</p>')
