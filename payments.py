from yoomoney import Client, Quickpay

class YooPayment:
    def __init__(self, ACCESS_TOKEN_APP):
        self.client = Client(ACCESS_TOKEN_APP)

    def get_all_client_history(self):
        history = self.client.operation_history()
        print("Next page starts with: ", history.next_record)

        print("List of operations:")

        for operation in history.operations:
            print()
            print("Operation:",operation.operation_id)
            print("\tStatus     -->", operation.status)
            print("\tDatetime   -->", operation.datetime)
            print("\tTitle      -->", operation.title)
            print("\tPattern id -->", operation.pattern_id)
            print("\tDirection  -->", operation.direction)
            print("\tAmount     -->", operation.amount)
            print("\tLabel      -->", operation.label)
            print("\tType       -->", operation.type)
    def is_success_payment(self, key_str):
        history = self.client.operation_history()
        for operation in history.operations:
            if operation.label == key_str and operation.status == "success":
                return True
        return False
    
    def get_yoom_account_info(self):
        user = self.client.account_info()
        print("Account number:", user.account)
        print("Account balance:", user.balance)
        print("Account currency code in ISO 4217 format:", user.currency)
        print("Account status:", user.account_status)
        print("Account type:", user.account_type)
        print("Extended balance information:")
        for pair in vars(user.balance_details):
            print("\t-->", pair, ":", vars(user.balance_details).get(pair))
        print("Information about linked bank cards:")
        cards = user.cards_linked
        if len(cards) != 0:
            for card in cards:
                print(card.pan_fragment, " - ", card.type)
        else:
            print("No card is linked to the account")
            
    @staticmethod
    def get_payment_url(order_id_str, cost, key_str):
        quickpay = Quickpay(
            receiver="4100117797762983",
            quickpay_form="shop",
            targets="Оплата заказа №"+order_id_str,
            paymentType="SB",
            label=key_str, 
            formcomment="CP Shop: Заказ №"+order_id_str,
            sum=cost,
        )
        return quickpay.redirected_url