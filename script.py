import spacy
import re
import itertools
import matplotlib.pyplot as plt
import numpy as np


def produce_plot(result, fig_name, kind):
    """Save plot of result

    Parameters:
    result: data to draw
    fig_name: figure name
    kind: type of data used to plot
    """
    
    plt.bar(["\"{}\"".format(i[0]) for i in result], [i[1] for i in result])
    plt.ylabel('total')
    plt.xlabel('term')
    plt.xticks(rotation=45, fontsize=12)
    plt.title("Top {}{} ({})".format(kind, 's', fig_name.title()))
    plt.subplots_adjust(bottom=0.30)
    plt.savefig("plots/{}_{}.png".format(fig_name.replace(" ", "_"), kind))
    plt.close()


def top_pos(doc, pos, n, fig_name=""):
    """Finds the top n spaCy pos

    Parameters:
    doc: spaCy's doc
    pos: pos we are interesting in finding; one of "VERB", "NOUN", "ADJ" or "ADV"
    n: how many pos
    fig_name: name of the plot
    """
    
    pos_count = {}
    for token in doc:
        # ignore stop words
        if token.is_stop:
            continue

        if token.pos_ == pos:
            if token.lemma_ in pos_count:
                pos_count[token.lemma_] += 1
            else:
                pos_count[token.lemma_] = 1

    # sort by values, but before get only those keys where value > 1;
    # I want lemmas that appear more than one
    # lastly, get the first n results
    result = sorted({k: v for (k, v) in pos_count.items() if v > 1}.items(),
                    key=lambda kv: kv[1], reverse=True)[:n]

    print("top 10 {} {}".format(pos, result))
    produce_plot(result, fig_name, pos)


def top_entities(doc, n, fig_name=""):
    """Finds the top n spaCy entities

    Parameters:
    doc: spaCy's doc
    n: how many entities
    fig_name: name of the plot
    """
    
    entities = {}
    # named entities
    for ent in doc.ents:
        # Print the entity text and its label
        if ent.text in entities:
            entities[ent.text] += 1
        else:
            entities[ent.text] = 1
    result = sorted(entities.items(), key=lambda kv: kv[1], reverse=True)[:n]
    print("top 10 entities {}".format(result))

    plt.bar(["\"{}\"".format(i[0]) for i in result], [i[1] for i in result])
    plt.ylabel('total')
    plt.xlabel('named entity')
    plt.xticks(rotation='vertical', fontsize=10)
    plt.title("Top {} named entities ({})".format(n, fig_name.title()))
    plt.subplots_adjust(bottom=0.40)
    plt.savefig("plots/{}_entity.png".format(fig_name.replace(" ", "_")))
    plt.close()


def overall_results(doc):
    # get the top 10 verbs, nouns, adj and adv
    top_pos(doc, 'VERB', 10, "overall")
    top_pos(doc, 'NOUN', 10, "overall")
    top_pos(doc, 'ADJ', 10, "overall")
    top_pos(doc, 'ADV', 10, "overall")
    top_entities(doc, 30, "overall")


def character_results(nlp):
    """Creates a doc per character using their lines,
    and calculate the top 10 pos and entities

    Parameters:
    nlp: spaCy's nlp

    Returns:
    character:doc dict
   """
    # these are the characters I want to analyze
    subjects = ['thor', 'tony stark', 'bruce banner', 'doctor strange',
                'steve rogers', 'thanos', 'wanda maximoff', 'vision',
                'natasha romanoff', 'gamora', 'peter quill', 'ebony maw',
                'james rhodes', 'rocket', 'peter parker', 'groot', 'drax']
    # create a map of character:doc
    subjects_docs = {}

    for subject in subjects:
        print("Subject: {}".format(subject))
        with open('cleaned-script-subject.txt', 'r') as file:
            # this list will contain all the lines produced by the subject
            lines_with_subject = []
            for line in file:
                if line.lower().startswith(subject):
                    # remove the subject, e.g. Thanos :.... before appending
                    lines_with_subject.append(re.sub(r'.*:', '', line.lower()))
        # create a doc using a long string with line break between line
        # made from all the lines spoken by the subject
        doc = nlp('\n'.join(lines_with_subject))
        top_pos(doc, 'VERB', 10, subject)
        top_pos(doc, 'NOUN', 10, subject)
        top_pos(doc, 'ADJ', 10, subject)
        top_pos(doc, 'ADV', 10, subject)
        top_entities(doc, 10, subject)
        subjects_docs[subject] = doc

    return subjects_docs


def docs_similarities(subjects_docs):
    # remove Groot from dict 
    del subjects_docs['groot']
    # create a square ndarray of len(subjects_docs) filled with 1's
    similarities_matrix = np.full((len(subjects_docs), len(subjects_docs)), fill_value=1.0)

    # for every possible combination pair
    # e.g. (Tony, Strange), (Tony, Rocket) and so on
    for a, b in itertools.product(enumerate(subjects_docs), repeat=2):
        similarity_score = subjects_docs[a[1]].similarity(subjects_docs[b[1]])
        print("Similarity between {} and {} docs is {}".format(a[1], b[1], similarity_score))
        similarities_matrix[a[0], b[0]] = similarity_score

    plt.matshow(similarities_matrix, interpolation='nearest')
    plt.yticks(range(len(subjects_docs)), subjects_docs.keys())
    plt.xticks(range(len(subjects_docs)), subjects_docs.keys(), rotation='vertical')
    plt.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
    plt.colorbar()
    plt.title("Character's Corpus Similarity Matrix")
    plt.savefig("plots/similarity_matrix.png", bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_md")
    with open('cleaned-script.txt', 'r') as file:
        text = file.read()

    doc = nlp(text)
    overall_results(doc)
    subjects_docs = character_results(nlp)
    docs_similarities(subjects_docs)
