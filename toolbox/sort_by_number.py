def sort_by_number(filelist, prefix, suffix):
    # remove prefix and suffix, and sort by number
    newlist = sorted(
        filelist, key=lambda f: int(f.replace(prefix, '').replace(suffix, '')))

    return newlist


if __name__ == '__main__':
    prefix = 'prefix'
    suffix = '.dat'
    filelist = []
    for i in range(1000):
        filelist.append(prefix + str(i) + suffix)

    # naive sort
    filelist = sorted(filelist)
    print('Built-in sort')
    print(filelist)

    filelist = sort_by_number(filelist, prefix, suffix)
    print('Number sort')
    print(filelist)
