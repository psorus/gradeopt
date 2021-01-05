import hashlib as h


def bhash(q):
  return int(h.sha256(str(q).encode('ASCII')).hexdigest(),16)
