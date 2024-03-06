from proj.tasks import add, mul


if __name__ == "__main__":
    result = add.delay(1, 2)
    print(result.ready())
    print(result.state)
    print(result.get())
    print(result.state)
    print(result.ready())
    result = mul.apply_async((2, 2))
    print(result.get())
    print(result.state)
    result = add.apply_async((2, '2'), )
    print(result.state)
    print(result.get(propagate=False))
    print(result.state)

# python -m proj.main
