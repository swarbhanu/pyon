
# A better name for this might emerge if the functions here share a theme


def load_value_from_file(filename, variable):
    """Load the value of a variable in a Python file.

    @param filename: string
    @param variable: string
    @param passphrase: string
    @note Ported from twisted.persisted
    """
    mode = 'r'
    fileObj = open(filename, mode)
    d = {'__file__': filename}
    exec fileObj in d, d
    value = d[variable]
    return value



