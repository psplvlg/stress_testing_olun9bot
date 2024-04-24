from Array import Array
from Variable import Variable


def generate_test(chat_id, test_format):
    test_case = {}
    in_file = open(f"user_files/{chat_id}/in.txt", "w", encoding="utf-8")
    for string in test_format:
        for elem in string:
            print(type(elem))
            if isinstance(elem, Variable):
                test_case[elem.name] = elem.generate()
                print(test_case[elem.name], end=' ', file=in_file)
            elif isinstance(elem, Array):
                test_case[elem.name] = [Variable(f'{elem.name}[{i}]', elem.minVal, elem.maxVal).generate() for i in
                                        range(test_case[elem.sz])]
                print(*test_case[elem.name], end=' ', file=in_file)
        print(file=in_file)
    in_file.close()
    return in_file