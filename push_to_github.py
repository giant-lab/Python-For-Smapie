import git
import os

# Konfigurasi
repo_path = '/storage/emulated/0/Documents/python/AbsenGuru'
github_url = 'https://github.com/giant-lab/Python-For-Smapie.git'  # Ganti dengan URL repo Anda
commit_message = 'Commit dari Pydroid 3'

# Inisialisasi repo
repo = git.Repo.init(repo_path)

# Tambahkan semua file
repo.git.add(A=True)

# Commit perubahan
repo.index.commit(commit_message)

# Push ke GitHub (pastikan sudah set remote)
if 'origin' not in repo.remotes:
    repo.create_remote('origin', github_url)
    
origin = repo.remotes.origin
origin.push('master')

print("✅ Kode berhasil dipush ke GitHub!")