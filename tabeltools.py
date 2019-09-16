class LabeledList():


    def __init__(self, data=None, index=None):

        self.values = data
        self.index = self.set_index(data, index)
        self.next_count = 0

    def set_index(self, data, index):

        if index == None:
            return [index for index in range(len(data))]
        else:
            return [val for val in index]

    def map(self, func):

        new_vals = [func(val) for val in self]
        return LabeledList(new_vals, self.index)

    def __getitem__(self, keylist):

        if isinstance(keylist, LabeledList):
            return self.list_retrieval(keylist.values)
        elif isinstance(keylist, list):
            return self.list_retrieval(keylist)
        else:
            return self.single_retrieval(keylist)

    def single_retrieval(self, keylist):

        if keylist not in self:
            return None
        new_vals = []
        new_indices = []
        count = 0
        appearences = 0
        for val in self.index:
            if val == keylist:
                new_vals.append(self.values[count])
                new_indices.append(val)
                appearences += 1
            count += 1
        if appearences > 1:
            return LabeledList(new_vals, new_indices)
        else:
            return new_vals[0]



    def list_retrieval(self, ll):

        new_vals = []
        new_indices = []
        count = 0
        if not isinstance(ll[0], bool):
            for val in ll:
                if val in self.index:
                    new_vals.append(self[val])
            if self.has_nested(new_vals):
                newer_vals, newer_indices = self.cleaned_data(new_vals, ll)
                return LabeledList(newer_vals, newer_indices)
            else:
                return LabeledList(new_vals, ll)
        else:
            for val in ll:
                if val:
                    new_vals.append(self.values[count])
                    new_indices.append(self.index[count])
                count += 1
            return LabeledList(new_vals, new_indices)

    def cleaned_data(self, new_vals, new_indices):

        newer_vals = []
        newer_indices = []
        running_count = 0
        for val in new_vals:
            if isinstance(val, LabeledList):
                count = 0
                for cur in val:
                    newer_vals.append(cur)
                    newer_indices.append(val.index[count])
                    count += 1
                running_count += 1
            else:
                newer_vals.append(new_vals[running_count])
                newer_indices.append(new_indices[running_count])
                running_count += 1
        return (newer_vals, newer_indices)

    def has_nested(self, new_vals):

        for val in new_vals:
            if isinstance(val, LabeledList):
                return True
        return False

    def __eq__(self, other):

        new_vals = [val == other for val in self]
        return LabeledList(new_vals, self.index)

    def __ne__(self, other):

        new_vals = [val != other for val in self]
        return LabeledList(new_vals, self.index)

    def __gt__(self, other):

        new_vals = [val > other if type(val) == float else False for val in self]
        return LabeledList(new_vals, self.index)

    def __lt__(self, other):

        new_vals = [val < other if type(val) == float else False for val in self]
        return LabeledList(new_vals, self.index)

    def __iter__(self):

        return self

    def __next__(self):

        if self.next_count >= len(self.values):
            raise StopIteration
        next = self.values[self.next_count]
        self.next_count += 1
        return next

    def __contains__(self, item):
        return item in self.index

    def __repr__(self):

        return self.__str__()

    def __str__(self):

        data = zip(self.index, self.values)
        string = ""
        longest_val = 0
        longest_index = 0
        for i,v in data:
            cur_index = len(str(i))
            cur_val = len(str(v))
            if cur_index > longest_index:
                longest_index = cur_index
            if cur_val > longest_val:
                longest_val = cur_val

        data = zip(self.index, self.values)
        for i,v in data:
            string += f"{i:>{longest_index+ 2}}{str(v):>{longest_val + 2}}\n"
        return string


class Table():

    def  __init__(self, data, index=None, columns=None):

       self.data = data;
       self.index = [val if index is None else index[val] for val in range(len(data))]
       self.columns = [val if columns is None else columns[val] for val in range(len(data[0]))]

    def __str__(self):

        map = {index: 0 for index in range(len(self.data[0]))}
        for index in range(len(self.data)):
            for pos in range(len(self.data[0])):
                if map[pos] < len(str(self.data[index][pos])):
                    map[pos] = len(str(self.data[index][pos]))
        map = {i:map[i]+7 for i in range(len(map))}
        string = ""

        for i in range(len(self.data)):
            temp = f"{self.index[i]:<5}"
            for j in range(len(self.data[0])):
                temp += f"{self.data[i][j]:>{map[j]}}"
            temp += "\n"
            string += temp

        temp = f"{'':>5}"

        for i in range(len(self.data[0])):
            temp += f"{self.columns[i]:>{map[i]}}"
        temp += "\n"

        return temp + string

    def __repr__(self):

        return self.__str__()

    def __getitem__(self, col_list):

        if isinstance(col_list, LabeledList):
            return self.table_list_retrieval(col_list.values)
        elif isinstance(col_list, list):
            return self.table_list_retrieval(col_list)
        else:
            return self.table_single_retrieval(col_list)

    def table_list_retrieval(self, col_list):

        if isinstance(col_list[0], bool):
            return self.bool_retrieval(col_list);

        mapping_of_occurrences = self.get_mapping(col_list)
        number_of_occurrences = {val:col_list.count(val) for val in col_list}
        accumulated_rows = []

        for index in range(len(self.data)):
            row = []
            for val in mapping_of_occurrences:
                for _ in range(number_of_occurrences[val]):
                    for i in range(len(mapping_of_occurrences[val])):
                        row.append(self.data[index][mapping_of_occurrences[val][i]])
            accumulated_rows.append(row)

        if len(accumulated_rows) > 0:
            if len(accumulated_rows[0]) == 1:
                new_array = [accumulated_rows[i][0] for i in range(len(accumulated_rows))]
                return LabeledList(new_array, self.index)
            else:
                new_columns = self.get_new_columns(mapping_of_occurrences, number_of_occurrences)
                return Table(accumulated_rows, self.index, new_columns)


    def get_new_columns(self, mapping_of_occurrences, number_of_occurrences):

        new_cols = []
        for val in mapping_of_occurrences:
            for _ in range(number_of_occurrences[val]):
                for _ in range(len(mapping_of_occurrences[val])):
                    new_cols.append(val)
        return new_cols


    def get_mapping(self, col_list):
        map = {}
        for val in col_list:
            if val not in map:
                map[val] = [i for i in range(len(self.columns)) if self.columns[i] == val]
            else:
                continue
        return map



    def table_single_retrieval(self, col_list):

        number_of_occurrences = self.columns.count(col_list)
        indices_of_occurrence = [i for i in range(len(self.columns)) if self.columns[i] == col_list]
        final_col_list = []
        final_cols = []

        for i in range(number_of_occurrences):

            new_col_list = []
            for j in range(len(self.data)):
                new_col_list.append(self.data[j][indices_of_occurrence[i]])
            final_col_list.append(new_col_list)
            final_cols.append(self.columns[indices_of_occurrence[i]])

        if len(final_col_list) == 1:
            return LabeledList(final_col_list[0], self.index)

        elif len(final_col_list) > 1:
            return Table(self.transpose_matrix(final_col_list), self.index, final_cols)

        else:
            return None

    def transpose_matrix(self, col_list):
        new_matrix = self.matrix(len(col_list), len(col_list[0]))

        for i in range(len(col_list)):
            for j in range(len(col_list[i])):
                new_matrix[j][i] = col_list[i][j]

        return new_matrix

    def matrix(self, rows, cols):
        new_matrix = []
        for i in range(cols):
            row = []
            for j in range(rows):
                row.append(0)
            new_matrix.append(row)
        return new_matrix

    def bool_retrieval(self, col_list):
        new_table_rows = []
        new_table_indices = []
        for i in range(len(col_list)):
            if col_list[i]:
                new_table_rows.append(self.data[i])
                new_table_indices.append(self.index[i])

        return Table(new_table_rows, new_table_indices, self.columns)


    def __contains__(self, item):
        return item in self.columns


    def shape(self):
        return (len(self.data), len(self.data[0]))


    def head(self, n):

        if n == 0:
            return

        new_rows = []
        new_indices = []

        for i in range(n):
            new_rows.append(self.data[i])
            new_indices.append(self.index[i])

        return Table(new_rows, new_indices, self.columns)

    def tail(self, n):

        if n == 0:
            return

        new_rows = []
        new_indices = []

        for i in range(len(self.data)-n, len(self.data)):
            new_rows.append(self.data[i])
            new_indices.append(self.index[i])

        return Table(new_rows, new_indices, self.columns)


def read_csv(fn):
    with open(fn, "r", encoding="utf-8-sig") as f:
        all_players = []
        all_columns = next(f).split(',')
        for line in f:
            new_line = line.strip()
            items = new_line.split(",")
            new_array = []
            for item in items:
                new_item = item.strip()
                try:
                    new_array.append(float(new_item))
                except ValueError:
                    new_array.append(new_item)
            all_players.append(new_array)
    return Table(all_players, columns=all_columns)





if __name__ == '__main__':

    a = read_csv('fb.csv')
    running_backs = a[a["FantPos"] == "RB"]
    running_backs_with_over_100_attemps = running_backs[running_backs[]]
    print(running_backs[running_backs["PPR"] > 300])
