from fingerprint.Match import Match


def query_by_fingerprint(library, query_fingerprints):
    matches = _select_by_frequencies(library, query_fingerprints)

    most_common_origin = _find_most_common_origin(matches)
    return ''.join(most_common_origin)


def _find_most_common_origin(matches):
    occurrences = {}
    for m in matches:
        song_name = tuple(m.library_fingerprint.origin)
        if song_name not in occurrences:
            occurrences[song_name] = 1
        else:
            occurrences[song_name] += 1

    return max(occurrences.keys(), key=(lambda key: occurrences[key]))


def _select_by_frequencies(library, query_fingerprints):
    matches = []

    for query in query_fingerprints:
        for lib in library:
            if query.freq_1 == lib.freq_1 and query.freq_2 == lib.freq_2:
                matches.append(Match(query, lib))

    return matches
