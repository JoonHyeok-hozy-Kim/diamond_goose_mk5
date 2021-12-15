import csv
import os
from datetime import datetime

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, ListView

from diamond_goose_mk5 import settings
from hozylabapp.models import Laboratory


class HozyLabHomeView(ListView):
    model = Laboratory
    template_name = 'hozylabapp/lab_home.html'


def import_excel(request):
    try:
        if request.method == 'POST' and request.FILES['transaction_file']:

            transaction_file = request.FILES['transaction_file']
            in_media_directory = 'convert_transaction_excel'

            company = request.POST['company']
            in_media_directory += '/'
            in_media_directory += company
            in_media_directory += '/'

            save_dir = os.path.join(settings.MEDIA_ROOT, in_media_directory)
            fs = FileSystemStorage(location=save_dir)
            file_name = fs.save(transaction_file.name, transaction_file)
            new_dir = in_media_directory + file_name

            uploaded_file_url = fs.url(new_dir)
            excel_file = uploaded_file_url

            excel_transaction_data = pd.read_excel("."+excel_file, sheet_name=0, header=[0, 1])
            db_frame = excel_transaction_data.fillna('')
    except Exception as identifier:
        print('import_excel excel_reading Exception: ', identifier)

    try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="excel_transform_csv.csv"'
            response.write(u'\ufeff'.encode('utf8'))

            writer = csv.writer(response)
            # Header Insert
            writer.writerow([
                'ticker',
                'transaction_type',
                'quantity',
                'price',
                'transaction_fee',
                'transaction_tax',
                'transaction_date',
                'note',
            ])

            for row in db_frame.itertuples():

                if company == 'daeshin':

                    if int(row[0])%2 == 0:
                        # print('-------------------------------')
                        # print(row[1],    'transaction_date_yyyy/mm/dd')
                        # print(row[2],    'transaction_type1')
                        # print(row[3],    'currency')
                        # print(row[6],    'exchange_rate')
                        # print(row[7],    'ticker')
                        # print(row[8],    'quantity')
                        # print(row[10],   'domestic_tax')
                        # print(row[13],   'note')

                        transaction_date_yyyymmdd = row[1]
                        transaction_date_string_list = [transaction_date_yyyymmdd, ' 00:00:']
                        transaction_type1 = row[2]
                        currency = row[3]
                        exchange_rate = row[6]
                        ticker = str(row[7])

                        if row[8] == '':
                            quantity = 0
                        else:
                            quantity = row[8]

                        if row[10] == '':
                            domestic_tax = 0
                        else:
                            domestic_tax = row[10]

                        note = row[13]

                    else:
                        # print(row[1],    'transaction_sequence')
                        # print(row[2],    'transaction_type2')
                        # print(row[7],    'name')
                        # print(row[8],    'price')
                        # print(row[9],    'transaction_fee')
                        # print(row[10],   'foreign_tax')

                        transaction_date_string_list.append(str(row[1]//10))
                        transaction_date_string_list.append(str(row[1]%10))
                        transaction_date = datetime.strptime(transaction_date_yyyymmdd, "%Y/%m/%d")
                        # transaction_date = datetime.strptime(''.join(transaction_date_string_list), "%Y/%m/%d %H:%M:%S")

                        transaction_type2 = row[2]
                        name = row[7]

                        if row[8] == '':
                            price = 0
                        else:
                            price = row[8]

                        if row[9] == '':
                            transaction_fee = 0
                        else:
                            transaction_fee = row[9]

                        if row[10] == '':
                            foreign_tax = 0
                        else:
                            foreign_tax = row[10]
                        total_tax = domestic_tax + foreign_tax

                        transaction_type_final = 'UNDEFINED_INITIAL'
                        if transaction_type1 == '해외증권장내매매':
                            if transaction_type2 == '현금매도':
                                transaction_type_final = 'SELL'
                            elif transaction_type2 == '현금매수':
                                transaction_type_final = 'BUY'
                            else:
                                transaction_type_final = 'UNEXPECTED in 해외증권장내매매'

                        elif transaction_type2 == '외화매도환전':
                            if transaction_type1 == '출금':
                                transaction_type_final = 'EX_SELL'
                                ticker = 'EX_USD'
                                price = exchange_rate
                            else:
                                transaction_type_final = 'UNEXPECTED in 외화매도환전'
                        elif transaction_type2 == '외화매수환전':
                            if transaction_type1 == '입금':
                                transaction_type_final = 'EX_BUY'
                                ticker = 'EX_USD'
                                price = exchange_rate
                            else:
                                transaction_type_final = 'UNEXPECTED in 외화매수환전'

                        elif transaction_type2 == '계좌대체입고':
                            transaction_type_final = 'EQUITY_TRANSIT_IN'
                        elif transaction_type2 == '타사대체신청':
                            transaction_type_final = 'EQUITY_INTER_BANK_TRANSIT_OUT'

                        elif transaction_type2 == '타사대체출고':
                            transaction_type_final = 'INTER_BANK_TRANSIT_OUT'
                        elif transaction_type2 == '타사대체입고':
                            transaction_type_final = 'INTER_BANK_TRANSIT_IN'

                        elif transaction_type2 == '배당금':
                            if transaction_type1 == '입금':
                                transaction_type_final = 'DIVIDEND'

                        elif transaction_type2 == '액면교체':
                            transaction_type_final = 'SPLIT'

                        elif transaction_type2 == '병합단수주대':
                            transaction_type_final = 'SPLIT_ADDITIONAL ' + transaction_type2

                        elif transaction_type2 in ['개별상품대체입금',
                                                   '전자금융이체입금',] and transaction_type1 == '입금':
                            ticker = '_money'
                            transaction_type_final = 'MONEY_TRANSFER_IN'

                        elif transaction_type2 in ['개별상품대체출금'] and transaction_type1 == '출금':
                            ticker = '_money'
                            transaction_type_final = 'MONEY_TRANSFER_OUT'

                        elif transaction_type2 == '해외배당세환급' and transaction_type1 == '입금':
                            ticker = '_money_'+ticker
                            transaction_type_final = 'FOREIGN_DIV_TAX_REFUND'

                        elif transaction_type2 == '예탁금이용료' and transaction_type1 == '입금':
                            ticker = '_money_'
                            transaction_type_final = 'INTEREST_CMA'

                        elif transaction_type2 == '대체성전자출금' and transaction_type1 == '출금':
                            ticker = '_money_'+ticker
                            transaction_type_final = 'MONEY_OUT_OTHERS'

                        elif transaction_type2 == '은행이체출금' and transaction_type1 == '출금':
                            ticker = '_money'
                            transaction_type_final = 'MONEY_TRANSFER_OUT_OTHER_BANK'


                        # string_list = [str(ticker),
                        #                transaction_type_final,
                        #                str(quantity),
                        #                str(price),
                        #                str(total_tax),
                        #                str(transaction_fee),
                        #                str(transaction_date),
                        #                str(note)]
                        # for i in range(len(string_list)):
                        #     if string_list[i] == 'nan':
                        #         string_list[i] = 'None'
                        # print(','.join(string_list))

                        # Excel Line Insert
                        writer.writerow([
                            str(ticker),
                            transaction_type_final,
                            str(quantity),
                            str(price),
                            str(total_tax),
                            str(transaction_fee),
                            str(transaction_date),
                            str(note)
                        ])

                elif company == 'hankook':
                    if int(row[0])%2 == 0:
                        # print('-------------------------------')
                        # print(row[1],    'transaction_date_yyyy.mm.dd')
                        # print(row[2],    'name')
                        # print(row[3],    'quantity')
                        # print(row[4],    'exchange_rate')
                        # print(row[5],    'transaction_amount')
                        # print(row[6],    'transaction_fee')

                        transaction_date_yyyymmdd = row[1]
                        name = row[2]
                        skip_flag = False
                        if '삼성전자' in name:
                            if name == '삼성전자' or '보통주' in name:
                                ticker = "'005930"
                            else:
                                ticker = "'005935"
                        else:
                            skip_flag = True
                            ticker = 'N/A'
                            continue

                        quantity = row[3]
                        exchange_rate = row[4]
                        transaction_fee = comma_remover(row[6])
                        transaction_amount = comma_remover(row[5])

                    else:
                        if skip_flag:
                            continue

                        # print(row[1],    'transaction_type')
                        # print(row[3],    'price')
                        # print(row[6],    'transaction_tax')
                        # print(row[7],    'tax')
                        # print(row[8],    'vat')

                        transaction_date = datetime.strptime(transaction_date_yyyymmdd, "%Y.%m.%d")
                        note = ''

                        price = comma_remover(row[3])
                        if '주식매수' in row[1]:
                            transaction_type_final = 'BUY'
                        elif '주식매도' in row[1]:
                            transaction_type_final = 'SELL'
                        elif row[1] == '배당금입금':
                            transaction_type_final = 'DIVIDEND'
                            price = transaction_amount
                        else:
                            note = row[1]
                            transaction_type_final = 'UNEXPECTED_TRANSACTION'

                        total_tax = comma_remover(row[6]) + comma_remover(row[7]) + comma_remover(row[8])

                        # Excel Line Insert
                        writer.writerow([
                            str(ticker),
                            transaction_type_final,
                            str(quantity),
                            str(price),
                            str(total_tax),
                            str(transaction_fee),
                            str(transaction_date),
                            str(note)
                        ])


            # return HttpResponseRedirect(reverse('hozylabapp:lab_home'))
            return response
    except Exception as identifier:
        print('import_excel csv_writing Exception: ', identifier)


    return reverse('hozylabapp:lab_home')


def comma_remover(string_number):
    result_list = ['0']
    for i in string_number:
        if i != ',':
            result_list.append(i)
    return float(''.join(result_list))