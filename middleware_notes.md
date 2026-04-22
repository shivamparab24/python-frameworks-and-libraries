# FastAPI Middleware — Notes

---

# PART 1: One Middleware + Two Routes

## Code Structure

- 1 Middleware
- 2 Routes:
  - `/`
  - `/second_route`

---

## Execution Flow

Client → Middleware (before) → Route → Middleware (after) → Client

---

## Example Outputs

### `/`

1. before
2.1 inside route 1
3. after

### `/second_route`

1. before
2.2 inside route 2
3. after

---

## Key Concept

### Core Line

response = await call_next(request)

Meaning:
- Pass request to route
- Execute route
- Get response back

---

## Observations

1. Middleware runs for EVERY request
2. Middleware wraps route
3. Can short-circuit execution

---

## Important Rule

No call_next → route skipped  
No return → server error  

---

# PART 2: Two Middleware + Two Routes

## FastAPI Rule

Middleware executes in REVERSE order of definition

---

## Execution Order

m2 → m1 → route → m1 → m2

---

## Example Output

2. m2 before  
1. m1 before  
3. inside route  
6. m1 after  
5. m2 after  

---

## Mental Model

Middleware = onion layers  
Last defined = outermost  

---

# FINAL SUMMARY

One middleware:
before → route → after

Two middleware:
Last defined → First defined → route → First defined → Last defined
