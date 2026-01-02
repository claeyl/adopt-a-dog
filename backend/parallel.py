from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def slow_operation(item):
  time.sleep(4)
  return f"Processed {item}"

items = [1, 2, 3, 4, 5, 6, 7, 8]
results = []

with ThreadPoolExecutor(max_workers=4) as executor:
  # Submit all tasks
  future_to_item = {executor.submit(slow_operation, item): item for item in items}
  
  # Process results as they complete (not necessarily in order)
  for future in as_completed(future_to_item):
    result = future.result()
    results.append(result)
    print(f"Completed: {result}")

print(results)