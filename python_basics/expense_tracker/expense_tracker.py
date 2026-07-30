from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class Expense:
	name: str
	amount: float
	category: str


DEFAULT_CSV = Path(__file__).parent / "expenses.csv"


def load_expenses(csv_path: Path = DEFAULT_CSV) -> List[Expense]:
	expenses: List[Expense] = []
	if not csv_path.exists():
		return expenses
	with csv_path.open(newline="", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			try:
				amount = float(row.get("amount", "0") or 0)
			except ValueError:
				amount = 0.0
			expenses.append(Expense(name=row.get("name", ""), amount=amount, category=row.get("category", "")))
	return expenses


def save_expenses(expenses: List[Expense], csv_path: Path = DEFAULT_CSV) -> None:
	csv_path.parent.mkdir(parents=True, exist_ok=True)
	with csv_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=["name", "amount", "category"])
		writer.writeheader()
		for e in expenses:
			writer.writerow({"name": e.name, "amount": f"{e.amount:.2f}", "category": e.category})


def add_expense(name: str, amount: float, category: str, csv_path: Path = DEFAULT_CSV) -> None:
	expenses = load_expenses(csv_path)
	expenses.append(Expense(name=name, amount=amount, category=category))
	save_expenses(expenses, csv_path)


def list_expenses(csv_path: Path = DEFAULT_CSV, category: str | None = None) -> List[Expense]:
	expenses = load_expenses(csv_path)
	if category:
		expenses = [e for e in expenses if e.category.lower() == category.lower()]
	return expenses


def total_expenses(csv_path: Path = DEFAULT_CSV, category: str | None = None) -> float:
	expenses = list_expenses(csv_path, category)
	return sum(e.amount for e in expenses)


def remove_expense(index: int, csv_path: Path = DEFAULT_CSV) -> bool:
	expenses = load_expenses(csv_path)
	if 0 <= index < len(expenses):
		del expenses[index]
		save_expenses(expenses, csv_path)
		return True
	return False


def _print_expenses(expenses: List[Expense]) -> None:
	if not expenses:
		print("No expenses found.")
		return
	print(f"{'#':>3}  {'Name':30} {'Amount':>10}  {'Category'}")
	print("-" * 60)
	for i, e in enumerate(expenses):
		print(f"{i:3d}. {e.name:30} {e.amount:10.2f}  {e.category}")


def interactive_menu(csv_path: Path = DEFAULT_CSV) -> None:
	while True:
		print("\nExpense Tracker")
		print("1) Add expense")
		print("2) List expenses")
		print("3) Total expenses")
		print("4) Remove expense")
		print("5) Quit")
		choice = input("Choose an option: ").strip()
		if choice == "1":
			name = input("Name: ").strip()
			amt = input("Amount: ").strip()
			cat = input("Category: ").strip()
			try:
				amount = float(amt)
			except ValueError:
				print("Invalid amount")
				continue
			add_expense(name, amount, cat, csv_path)
			print("Added.")
		elif choice == "2":
			cat = input("Filter by category (enter for all): ").strip() or None
			expenses = list_expenses(csv_path, cat)
			_print_expenses(expenses)
		elif choice == "3":
			cat = input("Category to total (enter for all): ").strip() or None
			total = total_expenses(csv_path, cat)
			print(f"Total: {total:.2f}")
		elif choice == "4":
			expenses = list_expenses(csv_path)
			_print_expenses(expenses)
			idx = input("Index to remove: ").strip()
			try:
				i = int(idx)
			except ValueError:
				print("Invalid index")
				continue
			if remove_expense(i, csv_path):
				print("Removed.")
			else:
				print("Index out of range.")
		elif choice == "5":
			print("Goodbye")
			break
		else:
			print("Unknown choice")


def build_parser() -> argparse.ArgumentParser:
	p = argparse.ArgumentParser(prog="expense_tracker")
	p.add_argument("--file", "-f", default=str(DEFAULT_CSV), help="CSV file to use")
	sub = p.add_subparsers(dest="cmd")

	a = sub.add_parser("add", help="Add an expense")
	a.add_argument("name")
	a.add_argument("amount", type=float)
	a.add_argument("category")

	sub.add_parser("list", help="List expenses")
	t = sub.add_parser("total", help="Show total expenses")
	t.add_argument("--category", "-c", help="Category to total", default=None)
	r = sub.add_parser("remove", help="Remove expense by index")
	r.add_argument("index", type=int)

	return p


def main(argv: List[str] | None = None) -> None:
	parser = build_parser()
	args = parser.parse_args(argv)
	csv_path = Path(args.file)

	if not args.cmd:
		# run interactive menu
		interactive_menu(csv_path)
		return

	if args.cmd == "add":
		add_expense(args.name, args.amount, args.category, csv_path)
		print("Added.")
	elif args.cmd == "list":
		expenses = list_expenses(csv_path)
		_print_expenses(expenses)
	elif args.cmd == "total":
		total = total_expenses(csv_path, getattr(args, "category", None))
		print(f"Total: {total:.2f}")
	elif args.cmd == "remove":
		if remove_expense(args.index, csv_path):
			print("Removed.")
		else:
			print("Index out of range.")


if __name__ == "__main__":
	main()

