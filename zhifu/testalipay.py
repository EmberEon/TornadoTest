from zhifu import zhifubao

seller_id = "seller_id"
total_amount = 1
timeout_express = "90m"
out_trade_no = "111"
body = "111"
subject = "111"
result = zhifubao.make_zhi_fu_bao_url(seller_id=seller_id, body=body, subject=subject,
                                              total_amount=total_amount, timeout_express=timeout_express,
                                              out_trade_no=out_trade_no)


result, msg = zhifubao.queryalipay(out_trade_no)
print(result, msg)