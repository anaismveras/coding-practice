# Expense Tracker (terminal, CSV-backed)

Simple terminal-based expense tracker that stores expenses in a CSV file.

Usage examples:

- Interactive menu:

```bash
python -m expense_tracker.expense_tracker
```

- Add an expense from the command line:

```bash
python -m expense_tracker.expense_tracker add "Lunch" 12.50 Food
```

- List expenses:

```bash
python -m expense_tracker.expense_tracker list
```

- Show total:

```bash
python -m expense_tracker.expense_tracker total
```

By default the CSV is stored at `expense_tracker/expenses.csv`. Use `-f`/`--file` to provide a different path.
