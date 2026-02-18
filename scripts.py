import os
import re
import socket
from collections import Counter
from pathlib import Path


IF_PATH = "/home/data/IF.txt"
ALWAYS_PATH = "/home/data/AlwaysRememberUsThisWay.txt"
OUT_PATH = "/home/data/output/result.txt"


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def tokenize_keep_contractions(text):
    tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in tokens if t.strip("'")]
    return tokens


def tokenize_split_contractions(text):
    text = text.replace("’", "'")
    text = text.replace("'", " ")
    tokens = re.findall(r"[A-Za-z]+", text.lower())
    return tokens


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "UNKNOWN"


def main():
    if_text = read_text(IF_PATH)
    always_text = read_text(ALWAYS_PATH)

    if_tokens = tokenize_keep_contractions(if_text)
    always_tokens = tokenize_split_contractions(always_text)

    if_count = len(if_tokens)
    always_count = len(always_tokens)
    grand_total = if_count + always_count

    if_top3 = Counter(if_tokens).most_common(3)
    always_top3 = Counter(always_tokens).most_common(3)

    ip = get_ip()

    output = []
    output.append("Docker Word Count Results")
    output.append("=========================")
    output.append(f"IF.txt word count: {if_count}")
    output.append(f"AlwaysRememberUsThisWay.txt word count: {always_count}")
    output.append(f"Grand total words: {grand_total}")
    output.append("")
    output.append("Top 3 words in IF.txt:")
    for word, count in if_top3:
        output.append(f"  {word}: {count}")
    output.append("")
    output.append("Top 3 words in AlwaysRememberUsThisWay.txt (contractions split):")
    for word, count in always_top3:
        output.append(f"  {word}: {count}")
    output.append("")
    output.append(f"Container IP address: {ip}")

    Path("/home/data/output").mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(output))

    print("\n".join(output))


if __name__ == "__main__":
    main()
