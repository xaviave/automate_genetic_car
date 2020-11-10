from test_algo.DigitalcodeFounder import DigitalcodeFounder


def main():
    f = DigitalcodeFounder(20, password_len=20, mutation=4)
    f.launch()


if "__main__" == __name__:
    main()
