from git import Repo


def get_modified_paths(diffs):
    result = []
    for diff in diffs:
        result += [diff.a_path]
    return result


def show_changed_paths(diffs):
    for diff in diffs:
        print(type(diff))
        print(diff)
        print(diff.a_path)
        print(diff.b_path)


def guava_filter(path):
    """
    Filter for the Guava repository.
    :param path: file path relative to project's root
    :return: True if path satisfies the filter
    """
    return ("android" not in path) or ('com/google/common' not in path)


if __name__ == '__main__':
    # Load repository
    repo = Repo("repositories/guava")

    # Which commits to go through?
    # We can either start from the first commit and onwards or go back in the history from a commit and then
    # look at evolution in the right order.

    # => easiest is to go from the current commit and go back in time to compare diffs.
    #    results are then presented in the right order.

    # Go through history, one commit at a time from the beginning.
    data = {}
    order = []
    current = repo.head.commit
    print(f"Reading commit history from {current}")
    for i in range(50):
        if len(current.parents) == 1:
            parent = current.parents[0]
            paths = get_modified_paths(parent.diff(current))

            clean_paths = []
            for path in paths:
                split_path = path.split('/')
                split_path.pop(0)

                if guava_filter(path):
                    clean_paths.append(split_path)

            data[parent] = clean_paths
            order.append(parent)
        else:
            print(f"[Warning] Commit {current} has multiple parents {current.parents}")

        current = parent

    order.reverse() # The last commit we processed is the starting point of the evolution.

    # Post-processing (actually done in main loop for performance)
    # Remove everything before com/google/common (might be easier to do in path form rather than list)

    # Export
    # Per commit, the top-level module that changed.

    # Visualization (in JS) (no need to have all the modules at the beginning. We can build incrementally)
    # Starting at the beginning, the top-level modules that changed, place a point in the changed modules
    # Then next commit, add new top level module if any, place a point in the changed modules. Link current point with previous point changed in the same module.

    # Write results to CSV
    for commit in order:
        print(f'Commit {commit}')
        paths = data[commit]
        for path in paths:
            print(f"- {path}")