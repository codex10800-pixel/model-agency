from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil


class Command(BaseCommand):
    help = (
        'Copy project media files into a mounted persistent disk (Render). '
        'Useful during build/release to populate the mounted media folder from the repo media/ directory.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--src', help='Source media directory (defaults to project media folder)', default=None)
        parser.add_argument('--dest', help='Destination media directory (defaults to $RENDER_MEDIA_ROOT)', default=None)
        parser.add_argument('--dry-run', action='store_true', help='Show what would be copied but do not perform copy')
        parser.add_argument('--remove-stale', action='store_true', help='Remove files in destination that are not present in source')

    def handle(self, *args, **options):
        src = options['src']
        dest = options['dest']
        dry_run = options['dry_run']
        remove_stale = options['remove_stale']

        project_media = os.path.join(settings.BASE_DIR, 'media')
        if not src:
            src = project_media

        if not dest:
            dest = os.environ.get('RENDER_MEDIA_ROOT') or getattr(settings, 'MEDIA_ROOT', None)

        if not dest:
            self.stderr.write('Destination not provided and RENDER_MEDIA_ROOT not set. Aborting.')
            return

        src = os.path.abspath(src)
        dest = os.path.abspath(dest)

        if not os.path.exists(src):
            self.stderr.write(self.style.ERROR(f'Source media directory does not exist: {src}'))
            return

        self.stdout.write(f'Syncing media from {src} to {dest}')
        if dry_run:
            self.stdout.write('Dry run enabled — no files will be copied.')

        # Ensure destination exists
        if not dry_run:
            os.makedirs(dest, exist_ok=True)

        # Copy files and directories
        copied = 0
        for root, dirs, files in os.walk(src):
            rel = os.path.relpath(root, src)
            target_dir = os.path.join(dest, rel) if rel != '.' else dest
            if not dry_run:
                os.makedirs(target_dir, exist_ok=True)
            for f in files:
                sfile = os.path.join(root, f)
                tfile = os.path.join(target_dir, f)
                if dry_run:
                    self.stdout.write(f'Would copy: {sfile} -> {tfile}')
                else:
                    try:
                        shutil.copy2(sfile, tfile)
                        copied += 1
                    except Exception as e:
                        self.stderr.write(f'Failed to copy {sfile} -> {tfile}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Copied {copied} files.'))

        if remove_stale:
            removed = 0
            for root, dirs, files in os.walk(dest):
                rel = os.path.relpath(root, dest)
                src_dir = os.path.join(src, rel) if rel != '.' else src
                for f in files:
                    dest_file = os.path.join(root, f)
                    src_file = os.path.join(src_dir, f)
                    if not os.path.exists(src_file):
                        if dry_run:
                            self.stdout.write(f'Would remove stale file: {dest_file}')
                        else:
                            try:
                                os.remove(dest_file)
                                removed += 1
                            except Exception as e:
                                self.stderr.write(f'Failed to remove {dest_file}: {e}')
            self.stdout.write(self.style.SUCCESS(f'Removed {removed} stale files.'))
