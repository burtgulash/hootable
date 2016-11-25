#!/usr/bin/env python3

""" Simple Robin Hood linear probing hash table """

class Tab:

    LOAD_FACTOR_THRESHOLD = 0.7

    class Entry:

        def __init__(self, k, v, from_orig_slot):
            self.k = k
            self.v = v
            self.from_orig_slot = from_orig_slot


    def __init__(self, capacity=2):
        self.tab = [None for _ in range(capacity)]
        self.size = 0

    def __len__(self):
        return self.size

    def __setitem__(self, k, v):
        if self.size / len(self.tab) > self.LOAD_FACTOR_THRESHOLD:
            self.reallocate(len(self.tab) * 2)
        if self._add(k, v, self.tab):
            self.size += 1

    def _add(self, k, v, tab):
        slot = hash(k) % len(tab)
        from_orig_slot = 0
        entry = self.Entry(k, v, from_orig_slot)
        while True:
            # Insert new entry
            if tab[slot] is None:
                entry.from_orig_slot = from_orig_slot
                tab[slot] = entry
                return True

            # Update value if key exists
            if tab[slot].k == k:
                tab[slot].v = v
                return False

            # Robin Hood swap:
            if tab[slot].from_orig_slot < from_orig_slot:
                entry.from_orig_slot = from_orig_slot
                tab[slot], entry = entry, tab[slot]
                from_orig_slot = entry.from_orig_slot

            slot = (slot + 1) % len(tab)
            from_orig_slot += 1

    def __getitem__(self, k):
        slot = hash(k) % len(self.tab)
        while True:
            if self.tab[slot] is None:
                raise KeyError("Key '%s' not in table" % str(k))
            if self.tab[slot].k == k:
                return self.tab[slot].v
            slot = (slot + 1) % len(self.tab)

    def reallocate(self, capacity):
        new_tab = [None for _ in range(capacity)]
        for entry in self.tab:
            if entry is not None:
                self._add(entry.k, entry.v, new_tab)
        self.tab = new_tab


if __name__ == "__main__":
    keys = ["abc", "buba", "rak" , "a", "bebe", "111", "23", "lep", "mup", "muppet", "etc"]
    keys.extend(map(str, range(1337)))

    tab = Tab(capacity=2)
    for k in keys:
        tab[k] = k + "|" + k

    from_orig_mismatches = 0
    max_from_orig = 0
    for i, entry in enumerate(tab.tab):
        if entry:
            print(i, "%s -> %s  [%s]" % (entry.k, entry.v, entry.from_orig_slot))
            from_orig_mismatches += entry.from_orig_slot
            max_from_orig = max(max_from_orig, entry.from_orig_slot)
        else:
            print(i, "")
    print()
    print("FROM ORIG TOTAL:", from_orig_mismatches)
    print("MAX ORIG:", max_from_orig)

    # Verify
    # for k in keys:
    #     print("%s -> %s" % (k, tab[k]))
