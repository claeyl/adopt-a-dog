def unwrap(field):
  return getattr(field, "value", None)