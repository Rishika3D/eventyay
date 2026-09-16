from django.db import migrations


def make_events_public_and_indexed(apps, schema_editor):
    Event = apps.get_model('base', 'Event')
    Event_SettingsStore = apps.get_model('base', 'Event_SettingsStore')

    meetup_ids = list(
        Event_SettingsStore.objects.filter(key='event_type', value='meetup').values_list(
            'object_id', flat=True
        )
    )

    # Make previously hidden events show up in lists/search again.
    Event.objects.filter(is_public=False).exclude(pk__in=meetup_ids).update(is_public=True)

    # Drop any stored meta_noindex override so events fall back to the indexed default.
    Event_SettingsStore.objects.filter(key='meta_noindex').exclude(
        object_id__in=meetup_ids
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0074_bbbserver_disable_ssl_janusserver_disable_ssl_and_more'),
    ]

    operations = [
        migrations.RunPython(
            make_events_public_and_indexed,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
