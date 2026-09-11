# Challenge 5.1 — C: Close to the Metal

**Type:** Pointer trace + memory layout + implementation  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Pointer Arithmetic

Trace the following C code. For each line, write the value of every variable and the state of memory.

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;        // (1)

printf("%d\n", *p);  // (2)
p++;                 // (3)
printf("%d\n", *p);  // (4)
p += 2;              // (5)
printf("%d\n", *p);  // (6)

int *q = arr + 4;    // (7)
printf("%d\n", q - p); // (8) — pointer subtraction
```

1. After line (1): what is the value of `p`? What is `*p`?
2. After `p++` (line 3): by how many **bytes** did `p` advance? Why?
3. What does line (8) print? What does pointer subtraction compute?
4. If `int` were 8 bytes (not 4), how would your answers change?

---

## Part B — Stack vs Heap

```c
void bad_function() {
    int local = 42;
    int *p = &local;
    return;          // local goes out of scope here
    // p is now a DANGLING POINTER
}

int *create_int(int val) {
    int *p = malloc(sizeof(int));
    *p = val;
    return p;        // this is SAFE — heap survives function return
}

int main() {
    int *a = create_int(99);
    printf("%d\n", *a);
    free(a);         // required — or memory leak
}
```

5. Why is returning a pointer to a local variable undefined behaviour?
6. The heap-allocated version is safe to return. What happens if `free(a)` is omitted?
7. What does `malloc(sizeof(int))` actually do? Describe in terms of the OS and the C runtime heap allocator.
8. Write a version of `create_int` that allocates an array of `n` integers and fills them with values `1, 2, ..., n`. The caller is responsible for freeing.

---

## Part C — Implement strlen from Scratch

Implement `my_strlen(const char *s)` that returns the number of characters before the null terminator. You may not use any standard library functions, not even `strlen`.

```c
size_t my_strlen(const char *s) {
    // your implementation here
}
```

9. What is the time complexity of your implementation?
10. What happens if `s` is `NULL`? What should a robust implementation do?
11. Can you implement it using only pointer arithmetic (no array indexing with `[]`)? Show both versions.

---

## Part D — Struct Layout and Padding

```c
struct A {
    char  c;    // 1 byte
    int   i;    // 4 bytes
    char  d;    // 1 byte
};

struct B {
    int   i;    // 4 bytes
    char  c;    // 1 byte
    char  d;    // 1 byte
};
```

12. What is `sizeof(struct A)`? Draw the memory layout with padding bytes marked.
13. What is `sizeof(struct B)`? Why is it smaller than `sizeof(struct A)`?
14. What alignment rule explains the padding in struct A?
15. A struct contains `double` (8 bytes), `char` (1 byte), `int` (4 bytes). What is the minimum possible `sizeof` if you can reorder fields? Show the optimal layout.

---

## Part E — Memory Leak Hunt

The following function has at least two bugs. Find and fix them.

```c
char *duplicate_upper(const char *src) {
    int len = strlen(src);
    char *result = malloc(len);       // BUG 1
    for (int i = 0; i < len; i++) {
        result[i] = toupper(src[i]);
    }
    return result;
    free(result);                     // BUG 2
}

int main() {
    char *s = duplicate_upper("hello");
    printf("%s\n", s);
    // BUG 3 — what's missing here?
}
```

16. What is Bug 1? Why does it cause a crash or undefined behaviour for any non-empty input?
17. Why does the `free(result)` in the function body never execute? What should happen instead?
18. What is Bug 3 in `main`? Write the corrected `main`.

---

## Rubric

| Part | Points |
|---|---|
| A pointer arithmetic (4 questions) | 24 |
| B stack vs heap (4 questions) | 24 |
| C strlen implementation | 20 |
| D struct layout | 20 |
| E memory leak hunt | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. `p` = address of `arr[0]` (e.g., `0x7FFF0000`). `*p` = 10.
2. `p` advances by 4 bytes (sizeof int = 4). Pointer arithmetic scales by the pointed-to type size.
3. Line 8 prints **2**. `q - p` computes the number of **elements** (not bytes) between the two pointers: (arr+4) - (arr+2) = 2.
4. If `int` were 8 bytes: `p++` would advance by 8 bytes, but the element count difference (`q - p`) would still be 2.
</details>

<details>
<summary>Part B.8 — Array creation</summary>

```c
int *create_array(int n) {
    int *arr = malloc(n * sizeof(int));
    if (!arr) return NULL;
    for (int i = 0; i < n; i++) arr[i] = i + 1;
    return arr;
}
// Caller: int *a = create_array(5); ... free(a);
```
</details>

<details>
<summary>Part C — strlen</summary>

```c
// Array index version
size_t my_strlen(const char *s) {
    if (!s) return 0;
    size_t n = 0;
    while (s[n] != '\0') n++;
    return n;
}

// Pointer arithmetic version
size_t my_strlen_ptr(const char *s) {
    if (!s) return 0;
    const char *p = s;
    while (*p) p++;
    return (size_t)(p - s);
}
```
</details>

<details>
<summary>Part D</summary>

12. struct A: char(1) + 3 padding + int(4) + char(1) + 3 padding = **12 bytes**. Padding after `c` aligns `i` to 4-byte boundary. Trailing padding aligns struct size to multiple of 4.

13. struct B: int(4) + char(1) + char(1) + 2 padding = **8 bytes**. Both chars after the int don't require inter-field padding.

14. Each field must be aligned to its own size. `int` requires 4-byte alignment, so padding is added after any smaller field that precedes it.

15. `double`(8) + `int`(4) + `char`(1) + 3 padding = **16 bytes**. Optimal order: double first (largest), then int, then char.
</details>

<details>
<summary>Part E</summary>

16. Bug 1: `malloc(len)` allocates `len` bytes but a C string needs `len + 1` bytes (for the null terminator `'\0'`). Writing to `result[len]` in the loop is out of bounds — undefined behaviour.

17. The `free(result)` is after the `return` statement — unreachable code. The compiler may warn. The fix is either to not free (let the caller free) or restructure. Here the correct fix is removing the dead `free`.

18. Bug 3: `free(s)` is missing after `printf`. Corrected:
```c
int main() {
    char *s = duplicate_upper("hello");
    if (!s) return 1;
    printf("%s\n", s);
    free(s);
    return 0;
}
```
The corrected `duplicate_upper` also needs `malloc(len + 1)` and `result[len] = '\0'`.
</details>
