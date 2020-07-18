def force_length(list_, length, filler):
    """ Forces a list to have a certain length.

    list_ is the list
    length is the desired length of the list
    filler is the value to fill the list with if it is too short
    """
    while len(list_) < length:
        list_.append(filler)
    while len(list_) > length:
        list_.pop()
