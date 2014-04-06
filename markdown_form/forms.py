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
