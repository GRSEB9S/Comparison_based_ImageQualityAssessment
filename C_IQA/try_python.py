def addnum(a):
    a[0] = a[0]+2
    return a
if __name__ == '__main__':
    a = [2]
    b = addnum(a)
    print a[0]
    b[0] = 20
    print a[0]