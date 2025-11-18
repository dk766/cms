"""
Management command to set up the Editors group with appropriate permissions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cms_app.models import Page, Section, ContentBlock, Media, SiteConfiguration


class Command(BaseCommand):
    help = 'Set up the Editors group with appropriate permissions for the backend editor'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up Editors group...')

        # Create or get the Editors group
        editors_group, created = Group.objects.get_or_create(name='Editors')

        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Editors group'))
        else:
            self.stdout.write('✓ Editors group already exists')

        # Define the permissions editors should have
        models_and_permissions = [
            (Page, ['add', 'change', 'delete', 'view']),
            (Section, ['add', 'change', 'delete', 'view']),
            (ContentBlock, ['add', 'change', 'delete', 'view']),
            (Media, ['add', 'change', 'delete', 'view']),
            (SiteConfiguration, ['change', 'view']),  # Editors can modify but not add/delete site config
        ]

        permissions_to_add = []

        for model, perms in models_and_permissions:
            content_type = ContentType.objects.get_for_model(model)

            for perm_code in perms:
                codename = f'{perm_code}_{model._meta.model_name}'

                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    permissions_to_add.append(permission)
                    self.stdout.write(f'  - {permission.name}')
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'  ! Permission {codename} not found')
                    )

        # Add all permissions to the group
        editors_group.permissions.set(permissions_to_add)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully set up Editors group with {len(permissions_to_add)} permissions'
            )
        )

        self.stdout.write('\nEditors can now:')
        self.stdout.write('  - Create, edit, and delete pages')
        self.stdout.write('  - Manage sections and content blocks')
        self.stdout.write('  - Upload and manage media files')
        self.stdout.write('  - Edit site configuration')
        self.stdout.write('  - Access the backend editor at /backend/')

        self.stdout.write('\nTo add a user to the Editors group:')
        self.stdout.write('  1. Go to Django admin')
        self.stdout.write('  2. Edit the user')
        self.stdout.write('  3. Add them to the "Editors" group')
        self.stdout.write('  Or use: python manage.py shell')
        self.stdout.write('     >>> from django.contrib.auth.models import User, Group')
        self.stdout.write('     >>> user = User.objects.get(username="username")')
        self.stdout.write('     >>> editors = Group.objects.get(name="Editors")')
        self.stdout.write('     >>> user.groups.add(editors)')
