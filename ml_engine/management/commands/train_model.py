from django.core.management.base import BaseCommand
from ml_engine.model import train_model


class Command(BaseCommand):
    help = 'Train (or retrain) the Random Forest skill-level prediction model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--synthetic-only',
            action='store_true',
            help='Train on synthetic data only (ignores real quiz attempts)',
        )

    def handle(self, *args, **options):
        self.stdout.write('🤖 Training Random Forest model...')
        use_real = not options['synthetic_only']
        try:
            train_model(use_real_data=use_real)
            self.stdout.write(self.style.SUCCESS('✅ Model trained and saved successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Training failed: {e}'))
