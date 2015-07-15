def saver(f):
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        result=f(*args, **kwargs)
        return result
    return wrapper




@saver
def price_with_tax(tax_rate_percentage):
    price = 12
    return price * (1 + (tax_rate_percentage * .01))


print price_with_tax(10)