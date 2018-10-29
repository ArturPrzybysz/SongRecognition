from fingerprint import Fingerprint


class Match:
    def __init__(self, query: Fingerprint, lib: Fingerprint):
        self.query_fingerprint: Fingerprint = query
        self.library_fingerprint: Fingerprint = lib
