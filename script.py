import spacy
import re
import itertools

nlp = spacy.load("en_core_web_md")

with open('cleaned-script.txt', 'r') as file:
    text = file.read()

def top_pos(doc, pos, n):
    pos_count = {}
    for token in doc:
        # avoid stop words
        if token.is_stop:
            continue

        if token.pos_ == pos:
            if token.lemma_ in pos_count:
                pos_count[token.lemma_] += 1
            else:
                pos_count[token.lemma_] = 1

    print("top 10 {} {}".format(pos, sorted(pos_count.items(), key=lambda kv: kv[1], reverse = True)[:n]))

def top_entities(doc, n):
    entities = {}
    # named entities
    for ent in doc.ents:
        # Print the entity text and its label
        if ent.text in entities:
            entities[ent.text] += 1
        else:
            entities[ent.text] = 1
    print("top 10 entities {}".format(sorted(entities.items(), key=lambda kv: kv[1], reverse = True)[:n]))

    
doc = nlp(text)
top_pos(doc, 'VERB', 10)
top_pos(doc, 'NOUN', 10)
top_pos(doc, 'ADJ', 10)
top_pos(doc, 'ADV', 10)
top_entities(doc, 10)



"""print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)"""


subjects = ['thor', 'tony stark', 'bruce banner', 'doctor strange', 'steve rogers', 'thanos', 'wanda maximoff', 'vision', 'natasha romanoff', 'gamora',
            'peter quill', 'ebony maw', 'james rhodes', 'rocket', 'peter parker']
subjects_docs = {}
for subject in subjects:
    print("Subject: {}".format(subject))
    with open('cleaned-script-subject.txt', 'r') as file:
        lines_with_subject = []
        for line in file:
            if line.lower().startswith(subject):
                # remove the subject, e.g. Thanos :.... before appending
                lines_with_subject.append(re.sub(r'.*:', '', re.sub(r'.*:', '', line.lower())))
    doc = nlp('\n'.join(lines_with_subject))
    top_pos(doc, 'VERB', 10)
    top_pos(doc, 'NOUN', 10)
    top_pos(doc, 'ADJ', 10)
    top_pos(doc, 'ADV', 10)
    top_entities(doc, 10)
    subjects_docs[subject] = doc


print(subjects_docs['thor'].similarity(subjects_docs['bruce banner']))

for a,b in itertools.combinations(subjects_docs, 2):
    print("Similarity between {} and {} docs is {}".format(a,b,subjects_docs[a].similarity(subjects_docs[b])))



