from sentence_transformers import SentenceTransformer, util


def run_model(chat_lines, script_lines):
    """
    chat_lines   : list of strings (WhatsApp chat)
    script_lines : list of strings (movie script)
    returns      : dict {person : matched_character}
    """

    # -------- CHAT PROCESSING --------
    txt2 = []
    for line in chat_lines:
        if '<Media omitted>' not in line and len(line) > 18:
            txt2.append(line[18:].strip())

    d = {}
    for line in txt2:
        if ':' in line:
            name = line.split(':')[0]
            d.setdefault(name, []).extend(line.split(':')[1:])

    d2 = {k: v for k, v in d.items() if v}

    d4 = {}
    for key in d2:
        s = ""
        for msg in d2[key]:
            s += " " + msg
        d4[key] = s


    # -------- SCRIPT PROCESSING --------
    script1 = [i.strip() for i in script_lines if i and i[0] != "["]
    script2 = [i for i in script1 if i != ""]

    sd = {}
    for line in script2:
        if ':' in line:
            char = line.split(':')[0]
            sd.setdefault(char, []).extend(line.split(':')[1:])

    sd4 = {}
    for key in sd:
        s = ""
        for msg in sd[key]:
            s += " " + msg
        sd4[key] = s

    # manual personality hints
    


    # -------- EMBEDDINGS --------
    model = SentenceTransformer("all-MiniLM-L6-v2")

    d5 = {k: model.encode(v) for k, v in d4.items()}
    sd5 = {k: model.encode(v) for k, v in sd4.items()}


    # -------- COSINE SIMILARITY --------
    results = {}

    for person in d5:
        scores = {}
        for character in sd5:
            sim = util.cos_sim(d5[person], sd5[character]).item()
            scores[character] = sim

        best_match = max(scores, key=scores.get)
        results[person] = best_match

    return results
