dict = {}

known_numbers = [89867653009, 89167569880, 89161111524, 89866508295, 89859971245]

with open('out.txt') as file:

    for line in file:

        my_number = int(line.split(':')[1])

        for his_number in known_numbers:

            salt = abs (his_number - my_number)

            if salt not in dict:
                dict[salt]=0

            dict[salt] += 1

for key in filter (lambda k: dict[k] == 5, dict):
    print(key, dict[key])