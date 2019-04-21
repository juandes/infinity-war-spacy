import spacy
import re
import itertools
import matplotlib.pyplot as plt


def produce_plot(result, fig_name, kind):
    plt.bar(["\"{}\"".format(i[0]) for i in result], [i[1] for i in result])
    plt.ylabel('total')
    plt.xlabel('term')
    plt.xticks(rotation=45)
    plt.title("Top {}{} ({})".format(kind, 's', fig_name.title()))
    plt.subplots_adjust(bottom=0.30)
    plt.savefig("plots/{}_{}.png".format(fig_name.replace(" ", "_"), kind))
    plt.close()


def top_pos(doc, pos, n, fig_name=""):
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

    # sort by values, but before get only those keys where value > 1; I want lemmas that appear more than one
    # lastly, get the first n results
    result = sorted({k: v for (k, v) in pos_count.items() if v > 1}.items(), 
                    key=lambda kv: kv[1], reverse=True)[:n]

    print("top 10 {} {}".format(pos, result))
    produce_plot(result, fig_name, pos)


def top_entities(doc, n, fig_name=""):
    entities = {}
    # named entities
    for ent in doc.ents:
        # Print the entity text and its label
        if ent.text in entities:
            entities[ent.text] += 1
        else:
            entities[ent.text] = 1
    result = sorted(entities.items(), key=lambda kv: kv[1], reverse = True)[:n]
    print("top 10 entities {}".format(result))

    plt.bar(["\"{}\"".format(i[0]) for i in result], [i[1] for i in result])
    plt.ylabel('total')
    plt.xlabel('named entity')
    plt.xticks(rotation='vertical', fontsize=10)
    plt.title("Top {} named entities ({})".format(n, fig_name.title()))
    plt.subplots_adjust(bottom=0.40)    
    plt.savefig("plots/{}_entity.png".format(fig_name.replace(" ", "_")))
    
    plt.close()

    

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_md")
    with open('cleaned-script.txt', 'r') as file:
        text = file.read()

    doc = nlp(text)
    top_pos(doc, 'VERB', 10, "overall")
    top_pos(doc, 'NOUN', 10, "overall")
    top_pos(doc, 'ADJ', 10, "overall")
    top_pos(doc, 'ADV', 10, "overall")
    top_entities(doc, 30, "overall")

    subjects = ['thor', 'tony stark', 'bruce banner', 'doctor strange', 
                'steve rogers', 'thanos', 'wanda maximoff', 'vision', 'natasha romanoff', 'gamora',
                'peter quill', 'ebony maw', 'james rhodes', 'rocket', 'peter parker', 'groot', 'drax']
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
        top_pos(doc, 'VERB', 10, subject)
        top_pos(doc, 'NOUN', 10, subject)
        top_pos(doc, 'ADJ', 10, subject)
        top_pos(doc, 'ADV', 10, subject)
        top_entities(doc, 10, subject)
        subjects_docs[subject] = doc


    print(subjects_docs['thor'].similarity(subjects_docs['bruce banner']))

    for a, b in itertools.combinations(subjects_docs, 2):
        print("Similarity between {} and {} docs is {}".format(a,b,subjects_docs[a].similarity(subjects_docs[b])))  




