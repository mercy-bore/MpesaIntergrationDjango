#   serializer_class = TransactionSerializer
#     def post(self, request, *args, **kwargs):
#         logging.info("{}".format("Callback from MPESA"))
#         data = request.body
#         # return gateway.callback_handler(json.loads(data))
#         serializer = TransactionSerializer(data)
#         if serializer.is_valid():
#             payment = serializer.save()
#             return gateway.callback_handler(json.loads(payment))

#         else: #if the serialized data is not valid, return error response
#                 data = {"detail":serializer.errors, 'status':False}            
#                 return Response(data, status=status.HTTP_400_BAD_REQUEST)



{'id': 4,
 'transaction_no': 'a0ed1c06-8eaf-424d-b225-521c526e1745', 
 'phone_number': '',
 'checkout_request_id': '<app.stkpush.MpesaGateWay object at 0x7f15dfa151c0>',
 'reference': '', 
 'description': None, 
 'amount': '',
 'status': 1037,
 'receipt_no': None, 
 'created': '2022-07-09T08:29:22.844645+03:00',
 'ip': None}