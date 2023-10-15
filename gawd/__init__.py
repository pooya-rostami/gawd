import difflib
import itertools


__all__ = ["diff_workflows", "diff_workflow_files"]


# Threshold below which two items are considered mapped
THRESHOLD = 0.5
# Weight of the relative positions between two items
POSITION_WEIGHT = 0.1
# Weight of the difference between job names
JOB_NAME_WEIGHT = 0.1


def find_matches(s1, s2):
    """
    Return a list of matches between items from s1 and items from s2.

    A distance score is computed for all combinations.

    The returned list of matches is composed of (sorted) triples:
    ((i, a), (j, b), score) where `score` is the distance score, `a` and `b`
    are items respectively from `s1` and `s2`, and `i` and `j` their positions.
    """
    candidates = []

    # List all combinations and compute their distance scores
    for (i, a), (j, b) in itertools.product(enumerate(s1), enumerate(s2)):
        # Compute a score including a penalty if positions differ
        score = (1 - POSITION_WEIGHT) * distance(a, b) + POSITION_WEIGHT * abs(
            i - j
        ) / max(len(s1), len(s2))
        candidates.append(((i, a), (j, b), score))

    # Find best matches
    matches = []
    found_in_s1 = set()  # List of positions
    found_in_s2 = set()  # List of positions
    for (i, a), (j, b), score in sorted(candidates, key=lambda t: t[2]):
        if i in found_in_s1 or j in found_in_s2:
            continue

        matches.append(((i, a), (j, b), score))
        found_in_s1.add(i)
        found_in_s2.add(j)

    return matches


def dict_distance(s1, s2):
    """Compute a normalized distance between two dictionaries."""
    if s1 == s2:
        return 0

    common = [k for k in s1 if k in s2]
    removed = [k for k in s1 if k not in s2]
    added = [k for k in s2 if k not in s1]

    score = 0
    for k in common:
        score += distance(s1[k], s2[k])
    for k in removed:
        score += 1
    for k in added:
        score += 1

    return score / (len(common) + len(removed) + len(added))


def distance(v1, v2):
    """Compute a distance between two objects."""
    if v1 == v2:
        return 0
    elif (v1 is None) or (v2 is None):
        return 1
    elif isinstance(v1, dict) and isinstance(v2, dict):
        return dict_distance(v1, v2)
    elif isinstance(v1, list) and isinstance(v2, list):
        matches = find_matches(v1, v2)
        score = sum(score for _, _, score in matches)
        extra = max(len(v1), len(v2)) - len(matches)
        return (score + extra) / (len(matches) + extra)
    elif type(v1) == type(v2):
        if isinstance(v1, str):
            return 1 - difflib.SequenceMatcher(None, v1, v2).ratio()

    return 1


def dict_changes(lpath, v1, rpath, v2):
    """Return what changed between v1 and v2, being dictionaries."""
    common = [k for k in v1 if k in v2]
    removed = [k for k in v1 if k not in v2]
    added = [k for k in v2 if k not in v1]

    changes = []
    for k in removed:
        changes.append(("removed", "{}.{}".format(lpath, k), v1[k], None, None))
    for k in added:
        changes.append(("added", None, None, "{}.{}".format(rpath, k), v2[k]))
    for k in common:
        changes.extend(
            find_changes(
                "{}.{}".format(lpath, k), v1[k], "{}.{}".format(rpath, k), v2[k]
            )
        )

    return changes


def list_changes(lpath, v1, rpath, v2):
    """Return what changed between v1 and v2, being lists."""
    matches = find_matches(v1, v2)

    changes = []
    left_matched = set()
    right_matched = set()
    for (i, a), (j, b), score in matches:
        if score > THRESHOLD:
            break
        n_lpath = "{}[{}]".format(lpath, i)
        n_rpath = "{}[{}]".format(rpath, j)
        # Detect moves
        if i != j:
            changes.append(("moved", n_lpath, a, n_rpath, b))
        # Detect other changes
        changes.extend(find_changes(n_lpath, a, n_rpath, b))
        left_matched.add(i)
        right_matched.add(j)

    # Deal with added and removed items
    for i, a in enumerate(v1):
        if i not in left_matched:
            changes.append(("removed", "{}[{}]".format(lpath, i), a, None, None))
    for j, b in enumerate(v2):
        if j not in right_matched:
            changes.append(("added", None, None, "{}[{}]".format(rpath, j), b))

    return changes


def find_changes(lpath, v1, rpath, v2):
    if v1 == v2:
        return []

    # if v2 is None:
    #     return [("removed", lpath, v1)]
    # if v1 is None:
    #     return [("added", rpath, v2)]

    if isinstance(v1, dict) and isinstance(v2, dict):
        return dict_changes(lpath, v1, rpath, v2)
    elif isinstance(v1, list) and isinstance(v2, list):
        return list_changes(lpath, v1, rpath, v2)
    else:
        return [("changed", lpath, v1, rpath, v2)]


def diff_workflows(w1, w2):
    changes = []

    # Compare workflows except their "on" and "jobs" keys (specific treatment for them)
    changes.extend(
        find_changes(
            "", 
            [{k: v} for k, v in w1.items() if k not in ["on", "jobs"]], 
            "", 
            [{k: v} for k, v in w2.items() if k not in ["on", "jobs"]], 
        )
    )

    # Specific handling of "on" when it's a list or str and not a dict
    if 'on' in w1: 
        if 'on' not in w2: 
            changes.append(('removed', 'on', w1['on'], None, None))
        else:
            w1_on = w1['on']
            w2_on = w2['on']

            # Convert w1['on'] to dict
            if not isinstance(w1_on, dict):
                if not isinstance(w1_on, list):
                    w1_on = [w1_on]
                w1_on = {k: None for k in w1_on}

            # Convert w2['on'] to dict
            if not isinstance(w2_on, dict):
                if not isinstance(w2_on, list):
                    w2_on = [w2_on]
                w2_on = {k: None for k in w2_on}
            
            changes.extend(find_changes('on', w1_on, 'on', w2_on))
    elif 'on' in w2:
        changes.append(('added', None, None, 'on', w2['on']))

    # Specific handling of jobs
    jobs1 = list(w1.get("jobs", {}).items())
    jobs2 = list(w2.get("jobs", {}).items())
    matches = find_matches([v for _, v in jobs1], [v for _, v in jobs2])

    # Update score to take the names into account
    n_matches = []
    for (i, a), (j, b), score in matches:
        left_name = jobs1[i][0]
        right_name = jobs2[j][0]

        n_score = (1 - JOB_NAME_WEIGHT) * score + JOB_NAME_WEIGHT * distance(
            left_name, right_name
        )
        if n_score <= THRESHOLD:
            n_matches.append(((i, a), (j, b), n_score))
    matches = sorted(n_matches, key=lambda t: t[2])

    # Detect renamings and changes
    left_matched = set()
    right_matched = set()
    for (i, a), (j, b), score in matches:
        left_name = jobs1[i][0]
        right_name = jobs2[j][0]

        # Did we rename a job?
        if left_name != right_name:
            changes.append(("renamed", "jobs." + left_name, a, "jobs." + right_name, b))

        changes.extend(find_changes("jobs." + left_name, a, "jobs." + right_name, b))
        left_matched.add(left_name)
        right_matched.add(right_name)

    # Handling of non-matched jobs
    for name, job in jobs1:
        if name not in left_matched:
            changes.append(("removed", "jobs." + name, job, None, None))
    for name, job in jobs2:
        if name not in right_matched:
            changes.append(("added", None, None, "jobs." + name, job))

    return changes


def diff_workflow_files(w1, w2):
    import ruamel.yaml as yaml

    with open(w1) as f1:
        with open(w2) as f2:
            parser = yaml.YAML(pure=True)
            w1 = parser.load(f1)
            w2 = parser.load(f2)
    return diff_workflows(w1, w2)


def cli():
    import argparse

    global THRESHOLD, POSITION_WEIGHT, JOB_NAME_WEIGHT

    parser = argparse.ArgumentParser(
        prog="gawd",
        description="GAWD is a GitHub Actions Workflow Differ",
    )

    parser.add_argument("old", type=str, help="path to old workflow file")
    parser.add_argument("new", type=str, help="path to new workflow file")
    parser.add_argument(
        "--threshold",
        "-t",
        dest="THRESHOLD",
        metavar="X",
        type=float,
        help=f'distance threshold to map items, higher values favours "changed", lower values favours "added" and "removed" (default is {THRESHOLD})',
        default=THRESHOLD,
    )
    parser.add_argument(
        "--position-weight",
        "-p",
        dest="POSITION_WEIGHT",
        metavar="X",
        type=float,
        help=f"weight of list positions when comparing sequences (default is {POSITION_WEIGHT})",
        default=POSITION_WEIGHT,
    )
    parser.add_argument(
        "--job-name-weight",
        "-j",
        dest="JOB_NAME_WEIGHT",
        metavar="X",
        type=float,
        help=f"weight of job names when comparing jobs (default is {JOB_NAME_WEIGHT})",
        default=JOB_NAME_WEIGHT,
    )

    args, parameters = parser.parse_known_args()

    THRESHOLD = args.THRESHOLD
    POSITION_WEIGHT = args.POSITION_WEIGHT
    JOB_NAME_WEIGHT = args.JOB_NAME_WEIGHT

    for kind, o_path, o_value, n_path, n_value in diff_workflow_files(
        args.old, args.new
    ):
        if kind == "added":
            print(f"added {n_path} with {n_value!r}")
        elif kind == "removed":
            print(f"removed {o_path} with {o_value!r}")
        elif kind == "changed":
            print(f"changed {o_path} from {o_value!r} to {n_value!r}")
        elif kind == "moved":
            print(f"moved {o_path} to {n_path}")
        elif kind == "renamed":
            print(f"renamed {o_path} to {n_path}")
        else:
            raise ValueError(f"Unsupported change {kind}, please open an issue")
