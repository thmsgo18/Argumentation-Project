import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", required= True)
    parser.add_argument("-f", required= True)
    parser.add_argument("-a", required= True)

    args = parser.parse_args(argv)

    return {
        "probleme" : args.p,
        "file" : args.f,
        "arguments" : args.a
    }