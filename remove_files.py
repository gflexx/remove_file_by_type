import os, sys, argparse, time

def scan_directories(path):
    print('Scanning for child directories...\n')
    time.sleep(0.9)
    child_dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    for child in child_dirs:
        print('Found Directories: {}'.format(child))
    return child_dirs

def get_parent_directory(path):
    print('Getting parent directory')
    parent = os.path.dirname(path)
    print('Found: {}'.format(parent))
    return parent

def get_matches_in_directory(path, del_type):
    files = [x for x in os.listdir(path) if x.endswith('{}'.format(del_type))]
    print('Found: {} matches for [ {} ] in {}'.format(
        files.__len__(), 
        del_type,
        path
    ))
    full_path = []
    for f in files:
        p = os.path.join(path, f)
        full_path.append(p)
    return full_path

def main(args):
    path = r"{}".format(args.path)
    del_type = str(args.type)
    global verbose
    verbose = args.verbose
    
    # check if path exists else raise exception
    exists = os.path.exists(path)
    if not exists:
        raise Exception('Path entered does not exist')
    
    # if path is a directory check for child dir else get parent dir
    is_directory = os.path.isdir(path)
    
    deletions = []
    if is_directory:
        child_dirs = scan_directories(path)

        child = []
        for f in child_dirs:
            child.append(get_matches_in_directory(f, del_type))

        for chld in child:
            deletions.extend(chld)

        match_in_dir = get_matches_in_directory(path, del_type)
        deletions.extend(match_in_dir)
    else:
        parent_dir = get_parent_directory(path)
        child_dirs = scan_directories(parent_dir)

    time.sleep(1)
    delete_length = deletions.__len__()
    
    if delete_length > 0:
        confirm = str(
            input('\nDeleting is irreversible. \n[{}] files will be deleted. \nAre you sure?  (Y/N): '.format(deletions.__len__()))
        )
        if confirm.upper() == 'Y':
            pass
        else:
            print('Exited')
            return

        for f in deletions:
            print('Deleting : ' + f)
            os.remove(f)
        
        time.sleep(1)

        print('\n{} Files deleted!'.format(delete_length))
    else:
        print('\nZero {} matches found!'.format(del_type))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Removes files in a directory and its child directories by file type.'
    )
    parser.add_argument(
        '-p', '--path',
        help='Path of directory for removing files',
        required=True
    )
    parser.add_argument(
        '-t', '--type',
        help='File type to delete',
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
