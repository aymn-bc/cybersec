# Write-up – Exposed `.git` Repository Enumeration

## Objective

The target only exposed a web service on port **8080**, so the assessment focused on web enumeration.

---

## 1. Port Enumeration

An Nmap scan revealed that only port **8080** was open.

```bash
nmap -sV -sC <TARGET_IP>
```

Since no other services were available, the web application became the primary attack surface.

---

## 2. Directory Enumeration

To discover hidden files and directories, directory brute-forcing was performed using Gobuster and FFUF.

```bash
gobuster dir -u http://<TARGET_IP>:8080 \
-w SecLists/Discovery/Web-Content/raft-large-directories.txt
```

and

```bash
ffuf -u http://<TARGET_IP>:8080/FUZZ \
-w common.txt
```

The enumeration revealed several interesting resources:

```
.git/
.git/HEAD
.git/index
.git/config
.git/logs/
```

The presence of an exposed **`.git`** directory indicated that the application's Git repository was publicly accessible.

---

## 3. Downloading the Repository Metadata

The exposed Git directory was downloaded recursively.

```bash
wget -r http://<TARGET_IP>:8080/.git/
```

This retrieved the repository metadata, including:

```
HEAD
refs/
objects/
index
config
```

---

## 4. Repository Verification

The repository head was inspected.

```bash
cat .git/HEAD
```

Output:

```
ref: refs/heads/main
```

The branch reference was then examined.

```bash
cat .git/refs/heads/main
```

Output:

```
0f13550b4cb13e9f30c61d5b342c532d21e45bda
```

This confirmed the existence of a valid commit.

---

## 5. Inspecting the Commit

The commit type was verified.

```bash
git cat-file -t 0f13550b4cb13e9f30c61d5b342c532d21e45bda
```

Output:

```
commit
```

The commit metadata was displayed.

```bash
git cat-file -p 0f13550b4cb13e9f30c61d5b342c532d21e45bda
```

Result:

```
tree fa45db...
author ...
committer ...

initial Byte Lotus guest platform
```

---

## 6. Enumerating Repository Files

The tree object was inspected to determine which files were stored inside the repository.

```bash
git ls-tree -r HEAD
```

Output:

```
README.md
app.js
index.html
```

At this point it was confirmed that the repository contained only three tracked files.

---

## 7. Extracting File Contents

Instead of relying on a working tree, the files were extracted directly from the Git object database.

Examples:

```bash
git show HEAD:README.md
```

```bash
git show HEAD:app.js
```

```bash
git show HEAD:index.html
```

Alternatively, the blob hashes obtained from `git ls-tree` can be viewed with:

```bash
git cat-file -p <blob_hash>
```

---

## 8. JavaScript Analysis

The recovered `app.js` contained a minimal frontend stub.

```javascript
const API = "/api/guest";
```

The referenced endpoint `/api/guest` returned **404 Not Found**, indicating that it was either unimplemented or only a placeholder.

No credentials, secrets, API keys, or hidden endpoints were present in the JavaScript source.

---

## Conclusion

The key finding during enumeration was the publicly exposed **`.git`** directory. Recovering and inspecting the repository allowed direct access to the application's tracked source files without requiring access to the server itself.

This demonstrates why exposed version-control metadata should always be investigated during web application assessments, as it can reveal application source code, historical commits, configuration files, credentials, or other sensitive information depending on the contents of the repository.
