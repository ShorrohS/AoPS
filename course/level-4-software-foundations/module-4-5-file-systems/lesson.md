# Module 4.5 — File Systems

---

## The Problem

> You can read and write bytes at memory addresses.
> But when the power goes off, RAM forgets everything.
>
> How do you give data a name that persists across power cycles?
> How do you organise billions of bytes on a disk into something human-navigable?
> How does the OS know where one file ends and another begins?
>
> The answer is the **file system** — the layer that imposes order on the chaos of raw storage.

A file system solves three problems simultaneously: naming (how to find data by name), organisation (how to structure data into directories), and persistence (how to survive power loss without corruption).

---

## The Story

### Files Before File Systems

Early computers had no persistent storage. Programs and data were loaded from punch cards each run. The concept of a "file" — data with a name that persists — did not exist.

Magnetic tape (1950s) introduced persistence but no random access. Data was stored sequentially; to find record 1000, you had to scan past records 1–999. The concept of a "directory" had no meaning.

**Magnetic disk** (IBM RAMAC, 1956) introduced random access: the read/write head could seek to any location in milliseconds. Now you could have many files — but you needed a way to find them. The first file system concepts emerged: a table mapping names to disk locations.

Unix (1969) introduced the inode-based file system. This design — with refinements — is still used in ext4 (Linux) and HFS+ (macOS) today.

---

### Disks and Blocks

A magnetic hard disk is divided into fixed-size **blocks** (also called sectors or clusters). Typical block size: 4096 bytes (4 KB).

A file system works entirely in terms of blocks, not bytes:
- A 1-byte file occupies one full block (4 KB wasted internally — called **internal fragmentation**)
- A 5000-byte file occupies two blocks (8 KB on disk, 3 KB wasted)

The block is the smallest unit of allocation. The file system maintains a data structure tracking which blocks are free and which are in use.

---

### Inodes — The Heart of Unix File Systems

An **inode** (index node) is a data structure that stores all metadata about a file except its name:

```
inode {
  mode:      permissions (rwxrwxrwx) + file type
  uid, gid:  owner user and group IDs
  size:      file size in bytes
  atime:     last access time
  mtime:     last modification time
  ctime:     last metadata change time
  nlinks:    number of hard links to this inode
  blocks[]:  array of block addresses where data lives
             [direct blocks: 12 entries]
             [single indirect block pointer]
             [double indirect block pointer]
             [triple indirect block pointer]
}
```

**Direct blocks**: the first 12 entries point directly to data blocks. Supports files up to 12 × 4 KB = 48 KB with no indirection.

**Single indirect**: one block used as an array of block pointers. 4 KB / 4 bytes = 1024 pointers → 1024 × 4 KB = 4 MB additional data.

**Double indirect**: pointer → block of pointers → data. 1024 × 1024 × 4 KB = 4 GB.

**Triple indirect**: 1024³ × 4 KB = 4 TB.

This structure allows small files to be accessed very efficiently (direct blocks) while still supporting large files.

---

### Directories — Files About Files

A directory is simply a file whose data is a table of `(name → inode_number)` pairs:

```
Directory /home/user:
.    → inode 2  (this directory)
..   → inode 1  (parent directory)
hello.c → inode 417
notes.txt → inode 821
src  → inode 1024  (subdirectory inode)
```

When you access `/home/user/hello.c`:
1. Start at root inode (inode 2 on most systems)
2. Read root's directory data → find "home" → get its inode number
3. Read "home"'s directory data → find "user" → get inode number
4. Read "user"'s directory data → find "hello.c" → get inode 417
5. Read inode 417 → get list of data blocks
6. Read data blocks → file contents

This is why deep directory nesting (100 levels) is slow: each level requires at least one disk read.

---

### Hard Links and Soft Links

**Hard link**: a second directory entry pointing to the *same inode*. The inode's `nlinks` counter increments. The file has two names. Deleting one name decrements `nlinks`; data is only freed when `nlinks` reaches 0.

```bash
ln file.txt link.txt    # hard link: same inode, two names
```

**Symbolic link (symlink)**: a file whose data is a path string. Following a symlink reads its data (the path) and redirects the lookup. Symlinks can point to directories, span file systems, and point to things that don't exist.

```bash
ln -s /path/to/target link.txt   # symlink
```

Hard links: same inode, same file, multiple names. Symlinks: separate inode, data = path string, like a shortcut.

---

### The Free Space Bitmap

The file system tracks which blocks are free using a **bitmap**: one bit per block. Bit = 0 means free; bit = 1 means in use. Allocating a block: find a 0 bit, flip it to 1. Freeing a block: find the bit, flip it to 0.

For a 1 TB disk with 4 KB blocks: 1 TB / 4 KB = 2²⁸ blocks → bitmap = 2²⁸ bits = 32 MB. A very compact structure that fits easily in memory.

---

### Journaling — Surviving Power Loss

Suppose the system loses power halfway through creating a file:
- The directory was updated (points to a new inode)
- But the inode was never written
- Or the data blocks were written but the inode size was not updated

Without protection, the file system is now **inconsistent** — internal data structures contradict each other. `fsck` (file system check) was the traditional solution: scan the entire disk on every boot after an unclean shutdown. For a 1 TB disk this takes minutes.

**Journaling** (ext3, ext4, NTFS, HFS+): before making changes, write a **journal entry** describing what changes are about to be made. After all changes are safely written, mark the journal entry as committed.

On recovery after a crash: replay the journal. Any committed entries not yet applied are re-applied. The file system is always in a consistent state — recovery takes seconds instead of minutes.

Three modes:
- **Journal** (safest): journal both metadata and data. Slowest.
- **Ordered** (default ext4): journal metadata only; data flushed before metadata. Good balance.
- **Writeback** (fastest): journal metadata only; no ordering guarantee for data.

---

### File System Comparison

| Feature | FAT32 | ext4 (Linux) | NTFS (Windows) | APFS (Apple) |
|---|---|---|---|---|
| Max file size | 4 GB | 16 TB | 16 TB | ~8 EB |
| Max volume size | 2 TB | 1 EB | 256 TB | ~8 EB |
| Journaling | No | Yes | Yes | Yes |
| Permissions | No | Yes (Unix) | Yes (ACLs) | Yes |
| Case sensitivity | No | Optional | No | Optional |
| Snapshots | No | No (btrfs does) | Limited | Yes |
| Special feature | Universal compatibility | Mature, stable | Windows integration | Snapshots, encryption |

FAT32 remains valuable for its universal compatibility — every device (cameras, USB drives, consoles) understands it. Everything else is better for primary storage.

---

## The Concept: A File System is a Structured Lie

Raw storage is just blocks numbered 0 to N. The file system imposes a hierarchical namespace, persistent naming, and metadata on top of these anonymous blocks. The "file" you edit in a text editor does not physically exist as a contiguous sequence of bytes on the disk — it is an abstraction maintained by the inode and block pointer structures.

Understanding this is essential for: diagnosing disk corruption, recovering deleted files, building databases (which often bypass the file system entirely for performance), and understanding why "formatting" a disk doesn't actually erase data.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Inode Explorer**
- A virtual 16-block disk with an inode table
- Create files, watch inodes be allocated and filled
- Follow the chain: name → directory entry → inode number → block list → data

**Tool 2 — Directory Tree Walker**
- A visual directory tree
- Click any file to trace the path lookup: root → intermediate dirs → target inode
- Watch each disk read occur at each directory level

**Tool 3 — Journal Visualiser**
- Create a file in journaled mode
- See journal entries written before the actual disk update
- Simulate a crash mid-write — see recovery replay the journal

---

## Going Deeper

**Log-structured file systems (LFS)**: instead of updating files in place, LFS writes everything sequentially to the end of the log. Updates are always appends — no seeks, no fragmentation. Garbage collection reclaims space from old versions. Modern SSDs with their inherent sequential-write performance advantage make LFS attractive again.

**B-trees in file systems**: large directories with thousands of files cannot use a flat array — binary search would be needed. Modern file systems (NTFS, HFS+, btrfs, XFS) store directory contents in B-trees for O(log n) lookup. The B-tree appears at every layer of systems programming: databases (Module 9.2) also use it for the same reason.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace a file lookup through the inode/directory structure, calculate disk space usage, reason about journaling, and compare file system design choices.
