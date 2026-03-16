def my_ge():
   yield 1
   yield 2
   yield 3



me = my_ge()
print(next(me))
print(next(me))
print(next(me))
# print(next(me)) #gives error StopIteration

print()

for i in my_ge():
   print(i)


print()

def count_up_to(n):
   count = 1
   while count <= n:
      yield count
      count += 1

for num in count_up_to(5):
  print(num)



print()


def get_primes(start, end):
   primes = []

   for num in range(start, end+1):
      if num < 2:
         continue
      is_prime = True
      for i in range(2, num):
         if num % i == 0:
            is_prime = False
            break
      if is_prime:
         primes.append(num)
   return primes

get_primes(3, 100)


print()

def get_primes_gen(start, end):
   for num in range(start, end+1):
      if num < 2:
         continue
      is_prime = True
      for i in range(2, num):
         if num % i == 0:
            is_prime = False
            break
      if is_prime:
         yield num

prime = get_primes_gen(3, 100)

print(next(prime))
print(next(prime))
print(next(prime))


for i in get_primes_gen(3, 100):
   print(i)



def large_sequence(n):
  for i in range(n):
    yield i

# This doesn't create a million numbers in memory
gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))





# fibonacci sequence generator
def fibonacci():
   a, b = 0, 1
   while True:
      yield a
      a, b = b, a + b

# Get first 100 Fibonacci numbers
gen = fibonacci()
for _ in range(100):
   print(next(gen))





def echo_generator():
   while True:
      received = yield
      print("Received:", received)

gen = echo_generator()
next(gen) # Prime the generator
gen.send("Hello")
gen.send("World")




def my_gen():
   try:
      yield 1
      yield 2
      yield 3
   finally:
      print("Generator closed")

gen = my_gen()
print(next(gen))
gen.close()




def gen_primes(start, end):
   if start <= 2 <= end:
      yield 2
   for num in range(start, end + 1):
      if num < 3 or num % 2 == 0:
         continue
      
      is_prime = True

      for i in range(3, int(num ** 0.5) + 1, 2):
         if num % i == 0:
            is_prime = False
            break
      if is_prime:
         yield num

for value in gen_primes(50, 100):
   if value % 10 == 7:
      print(value)
      break

for value in gen_primes(50, 100):
   if value % 10 == 3:
      print(value)
      break


prime_list = list(gen_primes(50, 100))
print(prime_list)