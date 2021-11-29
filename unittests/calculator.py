class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        #return a /b
        try:
            return a / b
        except ZeroDivisionError as exception:
            print(f'An error occurred: {exception}')
        except:
            print('An unknown error occurred')
