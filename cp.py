'''

'''

import argparse
import pandas

parser = argparse.ArgumentParser()
parser.add_argument("val", type=int, help="display a square of a given number")
parser.add_argument("power", type=int, nargs="?", default=2, help="power to apply to val. 2 if not specified.")
parser.add_argument("-d", "--data", nargs="", help="increase output verbosity")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")

def enterLoop():
    stop = False

    while not stop:
        inputStr = input("Waiting for command (q to quit): ")
        if inputStr.upper() == 'Q':
            stop = True
        else:
            try:
                inputList = inputStr.split() # ArgumentParser accepts a list of arguments
                args = parser.parse_args(inputList)
                answer = args.val ** args.power

                if args.verbosity == 2:
                    print("{} power {} equals {}".format(args.val, args.power, answer))
                elif args.verbosity == 1:
                    print("{}^{} == {}".format(args.val, args.power, answer))
                else:
                    print(answer)
            except SystemExit:
                # exception thrown by the ArgumentParser.exit method called on error or on help request.
                # ArgumentParser prints its help and then the loop continues.
                continue


if __name__ == '__main__':
    enterLoop()
