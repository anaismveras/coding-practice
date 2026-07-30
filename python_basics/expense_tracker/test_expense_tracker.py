from pathlib import Path

from python_basics.expense_tracker.expense_tracker import add_expense, load_expenses, save_expenses, Expense


def test_add_and_load(tmp_path: Path):
    csv = tmp_path / "test.csv"
    # start empty
    assert load_expenses(csv) == []

    add_expense("Coffee", 3.5, "Food", csv)
    add_expense("Bus", 2.25, "Transport", csv)

    ex = load_expenses(csv)
    assert len(ex) == 2
    assert any(e.name == "Coffee" and abs(e.amount - 3.5) < 1e-6 for e in ex)


def test_save_and_overwrite(tmp_path: Path):
    csv = tmp_path / "test2.csv"
    expenses = [Expense("A", 1.0, "X"), Expense("B", 2.0, "Y")]
    save_expenses(expenses, csv)
    loaded = load_expenses(csv)
    assert len(loaded) == 2
    assert loaded[0].name == "A"
