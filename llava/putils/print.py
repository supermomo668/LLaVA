
def print_pload(pload):
  return {
    f'Key:{k}\n\t: Value{v}\n\tType:{type(v)}' for k,v in pload.items()
  }