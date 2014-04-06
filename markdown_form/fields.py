# This file is part of django-markdown-form.
#
# django-markdown-form is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-markdown-form is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-markdown-form.  If not, see <http://www.gnu.org/licenses/>.

import itertools

from django import forms
from django.core.exceptions import ValidationError

import markdown


class BaseMarkdownField(object):
    """This field handles markdown files. It converts a markdown file into
    an html string. It also extracts meta data from the file to store
    them in self.md_meta.

    By default, tags are extracted as strings. If specific configuration
    is given at runtime, some tags can be processed as list. This tags
    can be comma separated on one line or on several lines.

    ex: Tags: ham, spam
            foo
            bar, baz


    """

    def __init__(self, meta_list=[], extensions=['meta'],
                 extensions_cfg={}):
        """The meta list argument is used to specifie meta item that must
        be processed as lists.

        The extensions parameter can be used to set extensions to use with
        the markdown converter. Check the python-markdown documentation for
        more info on this feature. extension_config parameter is used for
        markdown configuration.

        """
        self.meta_list = meta_list
        self.md_extensions = extensions
        self.md_extensions_cfg = extensions_cfg
        self.md_meta = {}

    def _convert_tag(self, tag_name, value):
        """Convert a tag to a raw value or a list according to the field
        configuration (md_list constructor argument).

        """
        if tag_name in self.meta_list:
            value = list(itertools.chain(
                *[v.split(',') for v in value]))
            value = [v.strip() for v in value]
        else:
            if len(value) > 1:
                raise ValidationError('%s can\'t be a list' % tag_name)
            value = value[0]

        return value

    def _extract_meta(self, md_text):
        """Extract markdown meta.

        """
        self.md = markdown.Markdown(extensions=['meta'])

        # here is a copy-paste of a part of the preprocessing part of
        # mardown.Markdown.convert
        if not md_text.strip():
            return {}

        try:
            md_text = markdown.util.text_type(md_text)
        except UnicodeDecodeError as e:
            e.reason += '. -- Note: Markdown only accepts unicode input!'
            raise

        lines = md_text.split('\n')
        for preproc in self.md.preprocessors.values():
            lines = preproc.run(lines)

        md_meta = {}

        for key, val in self.md.Meta.items():
            key = key.lower()
            md_meta[key] = self._convert_tag(key, val)

        return md_meta

    def _convert(self, md_text, extensions=None, extensions_configs=None):
        """Convert markdown text into html.

        """
        ext = extensions or self.md_extensions
        cfg = extensions_configs or self.md_extensions_cfg

        self.md = markdown.Markdown(extensions=ext, extension_configs=cfg)

        return self.md.convert(md_text)


class MarkdownField(forms.FileField, BaseMarkdownField):
    """Markdown field for native django form.

    """
    def __init__(self, *args, **kwargs):
        """Accept both forms.FileField and BaseMarkdownField init
        arguments.

        """
        base_md_args = dict()
        # for some reason, if BaseMarkdownField.__init__ is called before
        # forms.FileField.__init__, some attributes are not set
        base_md_args['meta_list'] = kwargs.pop('meta_list', None)
        base_md_args['ext'] = kwargs.pop('extensions', None)
        base_md_args['ext_cfg'] = kwargs.pop('extension_configs', None)

        forms.FileField.__init__(self, *args, **kwargs)
        BaseMarkdownField.__init__(self, **{k: v for k, v in
                                            base_md_args.items() if
                                            v is not None})

    def clean(self, data, initial=None):
        """

        """
        data = forms.FileField.clean(self, data, initial)
        self.md_text = data.read()
        self.md_meta = self._extract_meta(self.md_text)

        return self._convert(self.md_text)
