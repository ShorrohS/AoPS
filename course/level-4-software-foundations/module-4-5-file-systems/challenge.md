# Challenge 4.5 — File Systems

**Type:** Calculation + trace + reasoning + design  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Setup

A Unix-like file system with:
- Block size: 4 KB (4096 bytes)
- Inode structure: 12 direct block pointers + 1 single-indirect + 1 double-indirect
- Each block pointer: 4 bytes
- Inode table starts at block 1; data blocks start at block 100

---

## Part A — File Size Limits

1. A file uses only **direct blocks** (12 entries). What is the maximum file size?

2. The **single-indirect block** holds block pointers. How many pointers fit in one 4 KB block? What additional file size does the single-indirect block support?

3. The **double-indirect block** adds another level. What is the total additional file size it can support?

4. What is the **total maximum file size** supported by this inode structure (direct + single + double indirect)?

5. A simple text file is 300 bytes. How many blocks does it consume? How many bytes are **wasted** (internal fragmentation)?

---

## Part B — Directory Lookup Trace

The following directory structure exists:

```
/ (root, inode 1)
├── home/ (inode 15)
│   └── alice/ (inode 42)
│       ├── notes.txt (inode 103)
│       └── code/ (inode 88)
│           └── main.c (inode 217)
└── etc/ (inode 7)
    └── passwd (inode 12)
```

Each directory read requires one disk access (to read the directory's data block).

6. Trace all disk accesses required to open `/home/alice/notes.txt`. List each step in order.

7. How many disk accesses are needed to open `/home/alice/code/main.c`? List them.

8. Why does accessing a deeply nested file like `/a/b/c/d/e/f/g/data.txt` (7 levels deep) have worse performance than a file at `/data.txt`? What is the worst-case disk access count?

9. Modern file systems maintain a **dentrycache** (directory entry cache) in RAM. How does this change the answer to question 7 for frequently accessed files?

---

## Part C — Disk Space Calculation

A disk has:
- Total capacity: 100 MB
- Block size: 4 KB
- Inode table: 100 inodes, each 128 bytes

10. How many data blocks does the disk have? (Ignore inode table space for simplicity.)

11. A directory contains 50 files, each exactly 1 byte of data. How much disk space is used in total? (Consider inodes, directory entries, and data blocks.)

12. The same 50 files are each 5000 bytes. How much total disk space is used now?

13. **Fragmentation**: a disk is 50% full. Files have been deleted and new ones added many times. The free blocks are scattered. A new 100 KB file is allocated. How many block reads might be needed to read this file sequentially? Compare to a defragmented disk. What does this imply about database storage?

---

## Part D — Hard Links, Symlinks, and Deletion

14. User runs:
```bash
echo "hello" > file.txt     # creates file.txt, inode 500
ln file.txt link.txt        # hard link
rm file.txt                 # delete file.txt
cat link.txt                # read via link.txt
```
Does the data still exist after `rm file.txt`? What is the inode's `nlinks` value after each command?

15. User creates a symlink: `ln -s /home/alice/notes.txt shortcut.txt`
Then `/home/alice/notes.txt` is deleted. What happens when you `cat shortcut.txt`? Why? How does this differ from the hard link case?

16. A user runs `rm bigfile.txt` on a 10 GB file. The `rm` command returns almost instantly. Did the 10 GB of data get "erased"? What actually happened? How long does the space become available for reuse?

17. Forensic investigators can often recover "deleted" files from a disk. Why? What would need to happen to make recovery impossible?

---

## Part E — Journaling and Consistency

An ext4 file system is in "ordered" journal mode. A program creates a new file:

Operations needed:
1. Allocate inode (update inode bitmap)
2. Write file data to data blocks
3. Update inode (fill in block pointers, size)
4. Update directory (add entry: "newfile" → inode)

The system loses power after step 2 but before step 3.

18. Without journaling: what inconsistency exists on disk after power loss? What would `fsck` have to do to repair it?

19. With journaling (ordered mode): what was written to the journal before the crash? What happens during recovery?

20. With journaling (writeback mode): is the data guaranteed to be present after recovery? What might be missing or corrupted, even with the metadata repaired?

21. A programmer argues: "I'll skip `fsync()` after writing — the journal will protect my data." Is this correct? What exactly does journaling protect, and what does it not protect?

---

## Rubric

| Part | Points |
|------|--------|
| A file size limits | 20 |
| B directory lookup | 20 |
| C disk space | 20 |
| D links and deletion | 22 |
| E journaling | 18 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. 12 × 4 KB = **48 KB** maximum with direct blocks only.
2. Pointers per block = 4096 / 4 = **1024**. Additional size = 1024 × 4 KB = **4 MB**.
3. Double indirect: 1024 × 1024 × 4 KB = **4 GB**.
4. Total = 48 KB + 4 MB + 4 GB ≈ **~4 GB** (dominated by double-indirect).
5. 300-byte file occupies **1 block** (4 KB). Wasted = 4096 − 300 = **3796 bytes** (92.6% waste!).
</details>

<details>
<summary>Part B trace</summary>

6. `/home/alice/notes.txt`:
   1. Read root inode (inode 1) — know block of root directory
   2. Read root directory block → find "home" → inode 15
   3. Read inode 15 → find home's data block
   4. Read home's directory block → find "alice" → inode 42
   5. Read inode 42 → find alice's data block
   6. Read alice's directory block → find "notes.txt" → inode 103
   7. Read inode 103 → get block list
   8. Read data block(s) of notes.txt
   
   **8 disk accesses** (minimum, assuming no caching).

7. `/home/alice/code/main.c`: one more directory level → +2 accesses (code's inode + code's directory block) = **10 disk accesses**.
</details>

<details>
<summary>Part D</summary>

14. After `echo > file.txt`: nlinks=1. After `ln file.txt link.txt`: nlinks=2. After `rm file.txt`: nlinks=1 (the data still exists, only the directory entry was removed). `cat link.txt` succeeds — data is fully intact. The inode and data blocks are freed only when nlinks reaches 0.

15. After deleting `/home/alice/notes.txt` (assuming nlinks drops to 0, data freed): `cat shortcut.txt` fails with "No such file or directory". The symlink still exists but its target path no longer resolves. Hard links avoid this because they reference the inode directly, not the path.

16. `rm bigfile.txt` removes the directory entry and decrements nlinks to 0 in the inode — essentially instant (one metadata write). The **inode and block bitmap bits are cleared**, marking the space as available. The data bytes are NOT overwritten. The space becomes available immediately for new allocations. The old data physically remains until new files overwrite those blocks.

17. Recovery is possible because the data bytes remain until overwritten. To make recovery impossible: overwrite the data blocks with zeros (or random data) before freeing them — the `shred` command does this. Secure deletion tools and full-disk encryption make forensic recovery infeasible.
</details>

<details>
<summary>Part E</summary>

18. Without journaling: inode not updated → inode points to no data blocks but bitmap says data blocks are allocated → "orphaned" blocks (allocated but not referenced). fsck must: scan all inodes, compare against block bitmap, find discrepancies, mark orphaned blocks as free. Time = proportional to disk size.

19. In ordered mode: data blocks written first, then journal entry written with metadata changes (inode + directory). After crash: data is on disk (step 2 done), journal entry for steps 3+4 may or may not exist. Recovery: if journal entry present, replay it (write inode and directory). If not, the file doesn't exist in the directory and inode isn't updated — no inconsistency, just the file is not created. No fsck needed.

20. Writeback: journal protects metadata consistency but data and metadata order is not guaranteed. After recovery, the file might exist (metadata written) but contain garbage data from old blocks that happened to be allocated. The journal ensures you won't have an inconsistent inode structure, but the file's content may be corrupt.

21. **Incorrect**. Journaling protects **file system metadata consistency** — inode structures, directory entries, block allocations. It does NOT guarantee that application data written to a file reaches durable storage. Without `fsync()`, data may still be in the kernel's page cache (not yet on disk). A power loss drops the cached but unsynced data. `fsync()` forces the OS to flush all pending writes for that file to disk before returning.
</details>
