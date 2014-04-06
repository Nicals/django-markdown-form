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


def markdown_rest_serializer(cls):
    class MarkdownRestSerializer(cls):
        def restore_fields(self, data, files):
            """

            """
            reverted_data = dict()

            # restore markdown field
            md_field = self.fields.pop('markdown')
            md_field.initialize(parent=self, field_name='markdown')

            try:
                md_field.field_from_native(data, files,
                                           'markdown', reverted_data)
            except ValidationError as e:
                self._errors['markdown'] = list(e.message)

            # inject markdown result in the other fields if there are
            # not overriden
            for field_name, field_value in md_field.md_meta.items():
                if field_name not in data:
                    data[field_name] = field_value

            # restore other fields
            reverted_data = dict(
                reverted_data, **cls.restore_fields(self, data, files))

            # restore fields list state
            self.fields['markdown'] = md_field

            return reverted_data

    return MarkdownRestSerializer
