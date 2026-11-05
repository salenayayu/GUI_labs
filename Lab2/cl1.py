class Data:
    def __init__(self):
        # условные курсы: стоимость валюты в рублях.
        self.rates = {"RUB": 1, "USD": 90, "EUR": 100}
        self.myData = [0.0, 0.0, 0.0]

    def setData(self, amount, currency):
        rub = amount * self.rates[currency]
        self.myData = [rub, rub / self.rates["USD"], rub / self.rates["EUR"]]

    def getData(self):
        return self.myData.copy()