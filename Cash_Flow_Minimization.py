from itertools import chain
from collections import defaultdict

class Bank:
    def __init__(self, name, types):
        self.name = name
        self.netAmount = 0
        self.types = set(types)

def get_min_index(list_of_net_amounts):
    min_amount = float('inf')
    min_index = -1
    for i, bank in enumerate(list_of_net_amounts):
        if bank.netAmount == 0:
            continue
        if bank.netAmount < min_amount:
            min_index = i
            min_amount = bank.netAmount
    return min_index

def get_simple_max_index(list_of_net_amounts):
    max_amount = float('-inf')
    max_index = -1
    for i, bank in enumerate(list_of_net_amounts):
        if bank.netAmount == 0:
            continue
        if bank.netAmount > max_amount:
            max_index = i
            max_amount = bank.netAmount
    return max_index

def get_max_index(list_of_net_amounts, min_index, input_banks):
    max_amount = float('-inf')
    max_index = -1
    matching_type = None

    for i, bank in enumerate(list_of_net_amounts):
        if bank.netAmount == 0 or bank.netAmount < 0:
            continue
        
        common_types = list_of_net_amounts[min_index].types.intersection(bank.types)
        if common_types and bank.netAmount > max_amount:
            max_amount = bank.netAmount
            max_index = i
            matching_type = common_types.pop()

    return max_index, matching_type

def print_ans(ans_graph, num_banks, input_banks):
    print("\nThe transactions for minimum cash flow are as follows:\n")
    for i in range(num_banks):
        for j in range(num_banks):
            if i == j:
                continue

            if ans_graph[i][j][0] != 0 and ans_graph[j][i][0] != 0:
                if ans_graph[i][j][0] == ans_graph[j][i][0]:
                    ans_graph[i][j][0] = 0
                    ans_graph[j][i][0] = 0
                elif ans_graph[i][j][0] > ans_graph[j][i][0]:
                    ans_graph[i][j][0] -= ans_graph[j][i][0]
                    ans_graph[j][i][0] = 0
                    print(f"{input_banks[i].name} pays Rs {ans_graph[i][j][0]} to {input_banks[j].name} via {ans_graph[i][j][1]}")
                else:
                    ans_graph[j][i][0] -= ans_graph[i][j][0]
                    ans_graph[i][j][0] = 0
                    print(f"{input_banks[j].name} pays Rs {ans_graph[j][i][0]} to {input_banks[i].name} via {ans_graph[j][i][1]}")
            elif ans_graph[i][j][0] != 0:
                print(f"{input_banks[i].name} pays Rs {ans_graph[i][j][0]} to {input_banks[j].name} via {ans_graph[i][j][1]}")
            elif ans_graph[j][i][0] != 0:
                print(f"{input_banks[j].name} pays Rs {ans_graph[j][i][0]} to {input_banks[i].name} via {ans_graph[j][i][1]}")

            ans_graph[i][j][0] = 0
            ans_graph[j][i][0] = 0
    print("\n")

def minimize_cash_flow(num_banks, input_banks, index_of, num_transactions, graph, max_num_types):
    list_of_net_amounts = [Bank(bank.name, bank.types) for bank in input_banks]

    for b in range(num_banks):
        amount = sum(graph[i][b] for i in range(num_banks))
        amount -= sum(graph[b][j] for j in range(num_banks))
        list_of_net_amounts[b].netAmount = amount

    ans_graph = [[[0, ""] for _ in range(num_banks)] for _ in range(num_banks)]

    num_zero_net_amounts = sum(1 for bank in list_of_net_amounts if bank.netAmount == 0)

    while num_zero_net_amounts != num_banks:
        min_index = get_min_index(list_of_net_amounts)
        max_index, matching_type = get_max_index(list_of_net_amounts, min_index, input_banks)

        if max_index == -1:
            ans_graph[min_index][0][0] += abs(list_of_net_amounts[min_index].netAmount)
            ans_graph[min_index][0][1] = list_of_net_amounts[min_index].types.pop()

            simple_max_index = get_simple_max_index(list_of_net_amounts)
            ans_graph[0][simple_max_index][0] += abs(list_of_net_amounts[min_index].netAmount)
            ans_graph[0][simple_max_index][1] = list_of_net_amounts[simple_max_index].types.pop()

            list_of_net_amounts[simple_max_index].netAmount += list_of_net_amounts[min_index].netAmount
            list_of_net_amounts[min_index].netAmount = 0

            if list_of_net_amounts[min_index].netAmount == 0:
                num_zero_net_amounts += 1
            if list_of_net_amounts[simple_max_index].netAmount == 0:
                num_zero_net_amounts += 1
        else:
            transaction_amount = min(abs(list_of_net_amounts[min_index].netAmount), list_of_net_amounts[max_index].netAmount)
            ans_graph[min_index][max_index][0] += transaction_amount
            ans_graph[min_index][max_index][1] = matching_type

            list_of_net_amounts[min_index].netAmount += transaction_amount
            list_of_net_amounts[max_index].netAmount -= transaction_amount

            if list_of_net_amounts[min_index].netAmount == 0:
                num_zero_net_amounts += 1
            if list_of_net_amounts[max_index].netAmount == 0:
                num_zero_net_amounts += 1

    print_ans(ans_graph, num_banks, input_banks)

def main():
    print("\n\t\t\t\t********************* Welcome to CASH FLOW MINIMIZER SYSTEM ***********************\n\n\n")
    print("This system minimizes the number of transactions among multiple banks in the different corners of the world that use different modes of payment. There is one world bank (with all payment modes) to act as an intermediary between banks that have no common mode of payment. \n\n")
    num_banks = int(input("Enter the number of banks participating in the transactions:\n"))

    input_banks = []
    index_of = {}
    
    print("Enter the details of the banks and transactions as stated:")
    print("Bank name ,number of payment modes it has and the payment modes.")
    print("Bank name and payment modes should not contain spaces")

    max_num_types = 0

    for i in range(num_banks):
        if i == 0:
            print("World Bank: ", end="")
        else:
            print(f"Bank {i}: ", end="")
        
        name = input().strip()
        index_of[name] = i
        num_types = int(input().strip())

        if i == 0:
            max_num_types = num_types

        types = input().strip().split()

        input_banks.append(Bank(name, types))

    num_transactions = int(input("Enter number of transactions:\n"))

    graph = [[0] * num_banks for _ in range(num_banks)]

    print("Enter the details of each transaction as stated:")
    print("Debtor Bank , creditor Bank and amount")
    print("The transactions can be in any order")
    
    for i in range(num_transactions):
        print(f"{i} th transaction: ", end="")
        s1, s2, amount = input().strip().split()
        amount = int(amount)

        graph[index_of[s1]][index_of[s2]] = amount

    minimize_cash_flow(num_banks, input_banks, index_of, num_transactions, graph, max_num_types)

if __name__ == "__main__":
    main()
