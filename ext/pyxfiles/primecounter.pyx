

cpdef int prime_counter_cy(int range_from, int range_til):
    """ Returs the number of found prime numbers within a range. from and till are greedy """
    cdef int prime_count = 0
    cdef int num
    cdef int candidate_prime
    for num in range(range_from, range_til + 1):
      if (num > 1):
        for candidate_prime in range(2, num):

          if ((num % candidate_prime) == 0):
            break
        else:
          prime_count += 1
    return prime_count