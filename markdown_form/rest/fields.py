from rest_framework.fields import FileField

from markdown_form.fields import BaseMarkdownField


class MarkdownField(FileField, BaseMarkdownField):
    """Markdown field for rest_framework fields

    """
    def __init__(self, *args, **kwargs):
        # TODO: check if we can simplify this.
        #       for the moment, it is just a copy-paste from
        #       markdown_form.fields.MarkdownField
        base_md_args = dict()
        base_md_args['meta_list'] = kwargs.pop('meta_list', None)
        base_md_args['ext'] = kwargs.pop('extensions', None)
        base_md_args['ext_cfg'] = kwargs.pop('extension_configs', None)

        FileField.__init__(self, *args, **kwargs)
        # For default args compatibility, we only pass non-None arguments
        BaseMarkdownField.__init__(self, **{k: v for k, v in
                                            base_md_args.items() if
                                            v is not None})

    def from_native(self, data):
        data = FileField.from_native(self, data)
        self.md_text = data.read()
        self.md_meta = self._extract_meta(self.md_text)

        return self._convert(self.md_text)

    def to_native(self, value):
        return value
