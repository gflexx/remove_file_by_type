import os, sys, argparse

def scan_directories(path):
    print('Scanning for child directories')
    child_dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    for child in child_dirs:
        print('Found: {}'.format(child))
    return child_dirs

def get_parent_directory(path):
    print('Getting parent directory')
    parent = os.path.dirname(path)
    print('Found: {}'.format(parent))
    return parent

def delete_files_in_directory(path, del_type):
    files = [x for x in os.listdir(path) if x.endswith('{}'.format(del_type))]
    print('Found: {} matches for [ {} ]'.format(files.__len__(), del_type))

def main(args):
    path = r"{}".format(args.path)
    del_type = args.type
    global verbose
    verbose = args.verbose
    print(verbose)
    
    # check if path exists else raise exception
    exists = os.path.exists(path)
    if not exists:
        raise Exception('Path entered does not exist')
    
    # if path is a directory check for child dir else get parent dir
    is_directory = os.path.isdir(path)
    if is_directory:
        # child_dirs = scan_directories(path)
        delete_files_in_directory(path, del_type)
    else:
        parent_dir = get_parent_directory(path)
        child_dirs = scan_directories(parent_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Removes files in a directory and its child directories by file type.'
    )
    parser.add_argument(
        '-p', '--path',
        help='Path of directory for removing files',
        type=str,
        required=True
    )
    parser.add_argument(
        '-t', '--type',
        help='File type to delete',
        type=str,
        required=True
    )
    parser.add_argument(
        '-v', '--verbose',
        default='none',
        choices=['all', 'none'],
        help='Display verbose information; all to show info, none to hide info',
        required=False
    )
    args = parser.parse_args()
    main(args)