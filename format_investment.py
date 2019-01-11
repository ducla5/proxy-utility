with open('good.txt', 'r') as myfile:
    data = myfile.read().replace(':', '/').replace('\n', ';')
    f = open('output.txt', 'wt')
    f.write(data)
    f.close()
