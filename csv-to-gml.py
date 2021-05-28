def csv_to_gml(filename, nodes_file, edges_file):

    with open(nodes_file, encoding='utf-8') as file:
        nodes = file.readlines()
    
    with open(edges_file, encoding='utf-8') as file:
        edges = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('graph \n[\n')

        fields = nodes[0].strip().split(',')
        rows = nodes[1:]

        for row in rows:
            row = row.strip().split(',')

            file.write('\tnode \n\t[\n')
            for i, field in enumerate(fields):
                if field != 'id':
                    row[i] = '"' + row[i] + '"'
                file.write(f"\t\t{field} {row[i]}\n")
            file.write('\t]\n')

        fields = edges[0].strip().split(',')
        rows = edges[1:]

        for row in rows:
            row = row.strip().split(',')

            file.write('\tedge \n\t[\n')
            for i, field in enumerate(fields):
                file.write(f"\t\t{field} {row[i]}\n")
            file.write('\t]\n')

        file.write(']')


if __name__ == '__main__':

    filename = input('Введите название файла для сохранения графа: ')
    if not filename.endswith('.gml'):
        filename += '.gml'

    nodes_file = input('Введите название файла с вершинами: ')
    if not filename.endswith('.csv'):
        nodes_file += '.csv'
    
    edges_file = input('Введите название файла с ребрами: ')
    if not filename.endswith('.csv'):
        edges_file += '.csv'

    csv_to_gml(filename, nodes_file, edges_file)

