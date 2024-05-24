from django.core.management.base import BaseCommand
from bankDatas.utils import get_data_by_openAPI_and_save, check_old_and_delete
from bankDatas.models import Bank, FixedDeposit, SavingsAccount

class Command(BaseCommand):
    help = 'Fetch data from Open API and save to the database'

    def handle(self, *args, **kwargs):
        get_data_by_openAPI_and_save('depositProductsSearch', FixedDeposit)
        get_data_by_openAPI_and_save('savingProductsSearch', SavingsAccount)
        check_old_and_delete(FixedDeposit)
        check_old_and_delete(SavingsAccount)
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved data.'))