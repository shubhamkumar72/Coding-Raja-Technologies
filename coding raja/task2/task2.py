import json
from collections import defaultdict

class BudgetTracker:
    def __init__(self, file_path="transactions.json"):
        self.file_path = file_path
        self.transactions = self.load_transactions()
        self.categories = set()

    def load_transactions(self):
        try:
            with open(self.file_path, 'r') as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            transactions = []
        return transactions

    def save_transactions(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.transactions, file, indent=2)

    def add_transaction(self, category, amount, transaction_type):
        transaction = {
            "category": category,
            "amount": amount,
            "type": transaction_type,
        }
        self.transactions.append(transaction)
        self.categories.add(category)
        self.save_transactions()
        print(f'{transaction_type.capitalize()} of {amount} added successfully to category "{category}".')

    def calculate_budget(self):
        total_income = sum(transaction["amount"] for transaction in self.transactions if transaction["type"] == "income")
        total_expense = sum(transaction["amount"] for transaction in self.transactions if transaction["type"] == "expense")
        remaining_budget = total_income - total_expense
        return remaining_budget

    def analyze_expenses(self):
        expense_by_category = defaultdict(float)
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                expense_by_category[transaction["category"]] += transaction["amount"]

        if not expense_by_category:
            print("No expenses recorded.")
            return

        print("\nExpense Analysis:")
        for category, amount in expense_by_category.items():
            print(f"{category}: {amount}")

    def display_budget_summary(self):
        remaining_budget = self.calculate_budget()
        print("\nBudget Summary:")
        print(f"Total Income: {sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'income')}")
        print(f"Total Expenses: {sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'expense')}")
        print(f"Remaining Budget: {remaining_budget}")

def main():
    budget_tracker = BudgetTracker()

    while True:
        print("\nOptions:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Budget Summary")
        print("4. Analyze Expenses")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            budget_tracker.add_transaction(category, amount, "income")

        elif choice == '2':
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            budget_tracker.add_transaction(category, amount, "expense")

        elif choice == '3':
            budget_tracker.display_budget_summary()

        elif choice == '4':
            budget_tracker.analyze_expenses()

        elif choice == '5':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
