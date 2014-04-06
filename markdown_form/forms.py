from django.core.exceptions import ValidationError


def markdown_form(cls):
    class MarkdownForm(cls):
        def _clean_fields(self):
            """Populates form fields with markdown metadata.

            """
            md_field = self.fields.pop('markdown')
            value = md_field.widget.value_from_datadict(
                self.data, self.files, self.add_prefix('markdown'))

            try:
                initial = self.initial.get('markdown', md_field.initial)
                value = md_field.clean(value, initial)
                self.cleaned_data['markdown'] = value
            except ValidationError as e:
                self._errors['markdown'] = self.error_class(e.message)
                if 'markdown' in self.cleaned_data:
                    del self.cleaned_data['markdown']

            # set fields value from md metadata
            for name in self.fields:
                if name in md_field.md_meta:
                    self.data[name] = md_field.md_meta[name]

            # clean all other fields and reset sef.fields content
            super(cls, self)._clean_fields()
            self.fields['markdown'] = md_field

    return MarkdownForm
