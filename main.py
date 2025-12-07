#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

from modules.github_client import GitHubClient, GitHubAPIError
from modules import create as create_mod
from modules import delete as delete_mod
from modules import list as list_mod
from modules import get as get_mod
from modules import update as update_mod

def load_token():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN tidak ditemukan di .env. Salin .env.example -> .env dan isi token Anda.")
        sys.exit(1)
    return token

def prompt_yes_no(prompt, default=False):
    yes = {"y", "yes"}
    no = {"n", "no"}
    if default:
        prompt = f"{prompt} [Y/n]: "
    else:
        prompt = f"{prompt} [y/N]: "
    while True:
        ans = input(prompt).strip().lower()
        if not ans:
            return default
        if ans in yes:
            return True
        if ans in no:
            return False
        print("Jawaban tidak dimengerti, ketik y/yes atau n/no.")

def whoami(client):
    try:
        user = client.get_authenticated_user()
        print(f"Authenticated as: {user}")
    except GitHubAPIError as e:
        print("Gagal mengambil user:", e)

def create_repo(client):
    name = input("Nama repository baru: ").strip()
    if not name:
        print("Nama repository wajib diisi.")
        return
    description = input("Deskripsi (opsional): ").strip()
    private = prompt_yes_no("Buat private?", default=False)
    org = input("Organization (kosong untuk user): ").strip() or None
    try:
        resp = create_mod.create_repo(client, name, private=private, description=description, org=org)
        print("Repository dibuat:")
        print("  full_name:", resp.get("full_name"))
        print("  html_url:", resp.get("html_url"))
    except GitHubAPIError as e:
        print("Gagal membuat repository:", e)

def delete_repo(client):
    owner = input("Owner repository (kosong = authenticated user): ").strip()
    repo = input("Nama repository yang akan dihapus: ").strip()
    if not repo:
        print("Nama repository wajib diisi.")
        return
    if not owner:
        try:
            owner = client.get_authenticated_user()
        except GitHubAPIError as e:
            print("Gagal mendapat informasi user:", e)
            return
    confirm = prompt_yes_no(f"Yakin ingin menghapus {owner}/{repo}? Tindakan ini tidak bisa dibatalkan.", default=False)
    if not confirm:
        print("Dibatalkan.")
        return
    try:
        delete_mod.delete_repo(client, owner, repo)
        print(f"Repository {owner}/{repo} berhasil dihapus.")
    except GitHubAPIError as e:
        print("Gagal menghapus repository:", e)

def list_repos(client):
    visibility = input("Visibility (all/public/private) [all]: ").strip().lower() or "all"
    if visibility not in ("all", "public", "private"):
        print("Pilihan visibility tidak valid. Menggunakan 'all'.")
        visibility = "all"
    per_page_raw = input("Per page (angka, default 100): ").strip()
    try:
        per_page = int(per_page_raw) if per_page_raw else 100
    except ValueError:
        per_page = 100
    try:
        repos = list_mod.list_repos(client, visibility=visibility, per_page=per_page)
        if not repos:
            print("Tidak ada repository ditemukan.")
            return
        for r in repos:
            print(f"- {r.get('full_name')} (private={r.get('private')}) - {r.get('html_url')}")
        print(f"Total: {len(repos)} repositories")
    except GitHubAPIError as e:
        print("Gagal mengambil daftar repository:", e)

def get_repo(client):
    owner = input("Owner repository: ").strip()
    repo = input("Nama repository: ").strip()
    if not owner or not repo:
        print("Owner dan nama repository wajib diisi.")
        return
    try:
        data = get_mod.get_repo(client, owner, repo)
        # tampilkan ringkasan
        print("Repository:")
        print("  full_name:", data.get("full_name"))
        print("  description:", data.get("description"))
        print("  private:", data.get("private"))
        print("  html_url:", data.get("html_url"))
        print("  default_branch:", data.get("default_branch"))
        print("  created_at:", data.get("created_at"))
        print("  updated_at:", data.get("updated_at"))
        print("  stargazers_count:", data.get("stargazers_count"))
        print("  forks_count:", data.get("forks_count"))
    except GitHubAPIError as e:
        print("Gagal mengambil data repository:", e)

def update_repo(client):
    owner = input("Owner repository: ").strip()
    repo = input("Nama repository: ").strip()
    if not owner or not repo:
        print("Owner dan nama repository wajib diisi.")
        return
    to_change = {}
    if prompt_yes_no("Ubah nama repository?"):
        new_name = input("Nama baru: ").strip()
        if new_name:
            to_change["name"] = new_name
    if prompt_yes_no("Ubah deskripsi?"):
        new_desc = input("Deskripsi baru (kosong = hapus): ")
        to_change["description"] = new_desc
    if prompt_yes_no("Ubah private/public?"):
        is_private = prompt_yes_no("Set menjadi private?", default=False)
        to_change["private"] = is_private
    if not to_change:
        print("Tidak ada perubahan diberikan.")
        return
    try:
        resp = update_mod.update_repo(client, owner, repo, **to_change)
        print("Update berhasil. Data terbaru:")
        print("  full_name:", resp.get("full_name"))
        print("  description:", resp.get("description"))
        print("  private:", resp.get("private"))
        print("  html_url:", resp.get("html_url"))
    except GitHubAPIError as e:
        print("Gagal mengupdate repository:", e)

def print_menu():
    print("\n=== GitHub CLI Menu ===")
    print("1) Whoami (tampilkan user yang terautentikasi)")
    print("2) Buat repository")
    print("3) Hapus repository")
    print("4) Daftar repository")
    print("5) Dapatkan info repository")
    print("6) Update repository")
    print("0) Keluar")
    print("========================")

def main():
    token = load_token()
    client = GitHubClient(token)

    actions = {
        "1": whoami,
        "2": create_repo,
        "3": delete_repo,
        "4": list_repos,
        "5": get_repo,
        "6": update_repo,
    }

    while True:
        print_menu()
        choice = input("Pilih angka: ").strip()
        if choice == "0":
            print("Selesai. Sampai jumpa.")
            break
        action = actions.get(choice)
        if not action:
            print("Pilihan tidak valid, coba lagi.")
            continue
        try:
            action(client)
        except KeyboardInterrupt:
            print("\nDibatalkan oleh pengguna.")
        except Exception as e:
            # Tangani semua error tak terduga agar CLI tidak crash
            print("Terjadi error:", e)

if __name__ == "__main__":
    main()