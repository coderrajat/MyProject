def dec(fu):
    def dec1():
        print("executing")
        fu()
        print("executed")
    return dec1
@dec
def demo():
    print("demo")
demo()