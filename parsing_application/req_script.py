with open('requirements.txt', 'r+') as file:
    for line in file.readlines():
        line = line.split()
        res = '=='.join(line)
        file.write(f"{res}\n")