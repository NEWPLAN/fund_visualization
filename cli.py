import argparse


class Args(object):
    def __init__(self, info: str):
        self.parser = argparse.ArgumentParser(description=info)
        self.__register_args()
        self.args = self.__load_args()
        pass

    def __register_args(self):
        self.parser.add_argument(
            "--fid",
            type=int,
            required=True,
            help="the target fund to show the details",
        )
        pass

    def __load_args(self):
        return self.parser.parse_args()

    def show_args(self):
        print(self.args)
