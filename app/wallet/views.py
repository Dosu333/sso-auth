from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import requests


@api_view(['POST', ])
def web_hook(request):
    print(request.data)

    
@api_view(['POST',])
def webhook(request):
    pass
#     if request.method == 'POST':
#         if request.data['event'] == 'transfer.success':
#             print('Im in event')

#             transfer = Transaction.objects.get(reference=request.data['data']['reference'])
#             transfer.status = 'SUCCESSFUL'
#             transfer.save()
#             return Response(status=status.HTTP_200_OK)
            
#         if request.data['event'] == "transfer.failed":
#             print('Im in event 2')

#             transfer = Transaction.objects.get(reference=request.data['data']['reference'])
#             transfer.status = 'FAILED'
#             transfer.save()
#             return Response(status=status.HTTP_200_OK)

#         if request.data['event'] == "transfer.reversed":
#             print('Im in event 3')

#             transfer = Transaction.objects.get(reference=request.data['data']['reference'])
#             transfer.status = 'REVERSED'

#             wallet = Wallet.objects.get(store_owner=transfer.associated_store)

#             wallet.available_funds = float(wallet.available_funds) + float(request['data']['amount'])
#             wallet.save()
            
#             transfer.save()
#             return Response(status=status.HTTP_200_OK)

#         if request.data['event'] == 'charge.success':
#             print('Im in event 4')
#             print(request.data) 
#             ref = request.data['data']['reference']
#             app = request.data['data']['metadata']['app']
#             amount = request.data['data']['amount']
#             # user = request.data['data']['metadata']['user_id']
#             try:
#                 if app == 'delivery-dashboard':
#                     url = f'https://delivery.boxin.ng/api/v1/deliveries/update-offstordelivery/?ref={ref}&amount={amount}&type=offstore'
#                     # user = get_user_model().objects.get(id=user)
#                     # transaction, created = Transaction.objects.update_or_create(reference=ref, owner=user, amount=amount, defaults={'status': 'SUCCESSFUL'})
#                     res = requests.get(url, verify=False)
#                     response = res.json()

#                     if response['success']:
#                         return Response(status=status.HTTP_200_OK)

#                 if not app:
#                     url = f'https://delivery.boxin.ng/api/v1/deliveries/update-offstordelivery/?ref={ref}&amount={amount}&type=api'

#                     res = requests.get(url, verify=False)
#                     response = res.json()

#                     if response['success']:
#                         return Response(status=status.HTTP_200_OK)
#             except Exception as e:
#                 print(str(e))

#         if request.data['event'] == 'charge.failed':
#             print('Im in event 5')
#             # print(request.data)
#             ref = request.data['data']['reference']
#             app = request.data['data']['metadata']['app']
#             try:
#                 if app == 'delivery-dashboard':
#                    return Response(status=status.HTTP_200_OK)
#             except Exception as e:
#                 print(str(e))
#         print(request.data)
#         return Response(status=status.HTTP_200_OK)
