import pathlib

def get_filepath(file_name):
    """Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()

def solve():
    pass

if __name__ == "__main__":
    solve()
