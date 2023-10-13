import difflib
import itertools


__all__ = ['diff_workflows', 'diff_workflow_files']


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
        return sum(score for _, _, score in matches) / len(matches)
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
        changes.append(("removed", "{}.{}".format(lpath, k), v1[k]))
    for k in added:
        changes.append(("added", "{}.{}".format(rpath, k), v2[k]))
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
        n_lpath = "{}.[{}]".format(lpath, i)
        n_rpath = "{}.[{}]".format(rpath, j)
        # Detect moves
        if i != j:
            changes.append(("moved", n_lpath, n_rpath))
        # Detect other changes
        changes.extend(find_changes(n_lpath, a, n_rpath, b))
        left_matched.add(i)
        right_matched.add(j)

    # Deal with added and removed items
    for i, a in enumerate(v1):
        if i not in left_matched:
            changes.append(("removed", "{}.[{}]".format(lpath, i), a))
    for j, b in enumerate(v2):
        if j not in right_matched:
            changes.append(("added", "{}.[{}]".format(rpath, j), b))

    # Sort changes by position, for clarity
    changes = sorted(changes, key=lambda d: d[1])

    return changes


def find_changes(lpath, v1, rpath, v2):
    if v1 == v2:
        return []
    if v2 is None:
        return [("removed", lpath, v1)]
    if v1 is None:
        return [("added", rpath, v2)]    

    if isinstance(v1, dict) and isinstance(v2, dict):
        return dict_changes(lpath, v1, rpath, v2)
    elif isinstance(v1, list) and isinstance(v2, list):
        return list_changes(lpath, v1, rpath, v2)
    else:
        return [("changed", lpath, v1, rpath, v2)]


def diff_workflows(w1, w2):
    changes = []

    # Keys from left
    for key in w1.keys():
        if key != "jobs":
            changes.extend(find_changes(key, w1[key], key, w2.get(key, None)))

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
            changes.append(("renamed", "jobs." + left_name, "jobs." + right_name))

        changes.extend(find_changes("jobs." + left_name, a, "jobs." + right_name, b))
        left_matched.add(left_name)
        right_matched.add(right_name)

    # Handling of non-matched jobs
    for name, job in jobs1:
        if name not in left_matched:
            changes.append(("removed", "jobs." + name, job))
    for name, job in jobs2:
        if name not in right_matched:
            changes.append(("added", "jobs." + name, job))

    # Keys from right
    for key in w2.keys():
        if key not in w1 and key != "jobs":
            changes.extend(find_changes(key, None, key, w2[key]))

    return changes


def diff_workflow_files(w1, w2):
    raise NotImplementedError()


def cli():
    raise NotImplementedError()


if __name__ == '__main__':
    import sys
    
    sys.exit(cli())