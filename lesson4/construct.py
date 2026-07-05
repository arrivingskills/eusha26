class Fund:
    def __init__(self, name, amount, rate, fund_class):
        self.name = name
        self.amount = amount
        self.rate = rate
        self.fund_class = fund_class
    @classmethod
    def mutual_fund(cls, name, amount, rate, fund_class):
        if fund_class == "bond":
            return cls("Bond", 100000, 0.03, cls)

        return cls("Mutual Fund", 100000, 0.05, cls)
