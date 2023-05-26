def sentence_split(sentence, separator):
    for k in range(len(sentence)):
        a = sentence[k].split(separator)
        while '' in a:
            a.remove('')
        if a:
            sentence[k] = a[0].lower()
