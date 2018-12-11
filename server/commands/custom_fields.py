import sys
import click

from server.web import app
from server.models import (
    db,
    CustomFieldsSchema
)
from server.utils.database import get_or_create


def add_custom_field_main():
    with app.app_context():
        add_custom_field_wizard()

def delete_custom_field_main():
    with app.app_context():
        delete_custom_field_wizard()


def delete_custom_field_wizard():
    print('This wizard will guide you to DELETE custom field to the vulneraiblity model.')
    print('All available custom fields are:')
    for custom_field in db.session.query(CustomFieldsSchema):
        print('* {0}'.format(custom_field.field_name))
    print('End of custom fields')
    field_name = click.prompt('Field name')
    custom_field = db.session.query(CustomFieldsSchema).filter_by(field_name=field_name).first()
    if custom_field:
        db.session.delete(cusotm_field)
        db.session.commit()
    else:
        print('Custom field not found')

def add_custom_field_wizard():
    print('This wizard will guide you to ADD custom field to the vulneraiblity model.')
    field_name = click.prompt('Field name')
    field_display_name = click.prompt('Display name')
    field_type = click.prompt('Field type (int, str, list)', type=click.Choice(['int', 'str', 'list']))
    custom_fields = db.session.query(CustomFieldsSchema)
    current_used_orders = set()
    if custom_fields.count():
        print('Custom field current order')
    for custom_field in custom_fields:
        current_used_orders.add(custom_field.field_order)
        print('Field {0}, order {1}'.format(custom_field.field_display_name, custom_field.field_order))
    field_order = click.prompt('Field order index')
    while int(field_order) in current_used_orders:
        print('Field order already used, please choose another value')
        field_order = click.prompt('Field order index')
    confirmation = click.prompt('New CustomField will be added to vulnerability -> Order {order} ({0},{1},{2}) <-, confirm to continue (yes/no)'.format(field_name, field_display_name, field_type, order=field_order))
    if not confirmation:
        sys.exit(1)

    custom_field_data, created = get_or_create(
            db.session,
            CustomFieldsSchema,
            table_name='vulnerability',
            field_name=field_name,
            field_order=field_order,
    )
    if not created:
        print('Custom field already exists, skipping')
        sys.exit(1)
    custom_field_data.field_display_name = field_display_name,
    custom_field_data.field_type = field_type
    db.session.commit()
