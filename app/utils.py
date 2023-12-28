# from app import settings
# import datetime
#
# def payment(request):
#     if request.method == 'POST':
#         # Process input data and build url payment
#         form = request.form(request.POST)
#         if form.is_valid():
#             order_type = form.cleaned_data['order_type']
#             order_id = form.cleaned_data['order_id']
#             amount = form.cleaned_data['amount']
#             order_desc = form.cleaned_data['order_desc']
#             bank_code = form.cleaned_data['bank_code']
#             language = form.cleaned_data['language']
#             ipaddr = get_client_ip(request)
#             # Build URL Payment
#             vnp = vnpay()
#             vnp.requestData['vnp_Version'] = '2.1.0'
#             vnp.requestData['vnp_Command'] = 'pay'
#             vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
#             vnp.requestData['vnp_Amount'] = amount * 100
#             vnp.requestData['vnp_CurrCode'] = 'VND'
#             vnp.requestData['vnp_TxnRef'] = order_id
#             vnp.requestData['vnp_OrderInfo'] = order_desc
#             vnp.requestData['vnp_OrderType'] = order_type
#             # Check language, default: vn
#             if language and language != '':
#                 vnp.requestData['vnp_Locale'] = language
#             else:
#                 vnp.requestData['vnp_Locale'] = 'vn'
#                 # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
#             if bank_code and bank_code != "":
#                 vnp.requestData['vnp_BankCode'] = bank_code
#
#             vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
#             vnp.requestData['vnp_IpAddr'] = ipaddr
#             vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
#             vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
#             print(vnpay_payment_url)
#             # Redirect to VNPAY
#             return redirect(vnpay_payment_url)
#         else:
#             print("Form input not validate")
#
#     else:
#     return render(request, "payment.html", {"title": "Thanh toán"})
#
#
# def payment_return(request):
#     inputData = request.GET
#     if inputData:
#         vnp = vnpay()
#         vnp.responseData = inputData.dict()
#         order_id = inputData['vnp_TxnRef']
#         amount = int(inputData['vnp_Amount']) / 100
#         order_desc = inputData['vnp_OrderInfo']
#         vnp_TransactionNo = inputData['vnp_TransactionNo']
#         vnp_ResponseCode = inputData['vnp_ResponseCode']
#         vnp_TmnCode = inputData['vnp_TmnCode']
#         vnp_PayDate = inputData['vnp_PayDate']
#         vnp_BankCode = inputData['vnp_BankCode']
#         vnp_CardType = inputData['vnp_CardType']
#         if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
#             if vnp_ResponseCode == "00":
#                 return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
#                                                                "result": "Thành công", "order_id": order_id,
#                                                                "amount": amount,
#                                                                "order_desc": order_desc,
#                                                                "vnp_TransactionNo": vnp_TransactionNo,
#                                                                "vnp_ResponseCode": vnp_ResponseCode})
#             else:
#                 return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
#                                                                "result": "Lỗi", "order_id": order_id,
#                                                                "amount": amount,
#                                                                "order_desc": order_desc,
#                                                                "vnp_TransactionNo": vnp_TransactionNo,
#                                                                "vnp_ResponseCode": vnp_ResponseCode})
#         else:
#             return render(request, "payment_return.html",
#                           {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
#                            "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
#                            "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
#     else:
#         return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": ""})
