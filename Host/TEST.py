import lib
import time


def main():
    while(True):
        lib.set_GPIO_pin(13, 0)
        time.sleep(5)
        lib.set_GPIO_pin(13, 1)
        time.sleep(5)
    return


if __name__ == "__main__":
    main()
