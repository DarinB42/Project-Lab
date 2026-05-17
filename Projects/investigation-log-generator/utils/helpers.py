from datetime import datetime


def ask_question(prompt):
    return input(prompt + " ")


def choose_option(prompt, options):
    print(f"\n{prompt}")

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        choice = input("Select option number: ").strip()

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(options):
            return options[choice - 1]

        print(f"Please enter a number between 1 and {len(options)}.")


def generate_case_id(data_folder):
    today = datetime.now().strftime("%Y-%m-%d")
    existing_files = list(data_folder.glob(f"{today}-*_data.json"))
    next_number = len(existing_files) + 1
    return f"{today}-{next_number:03d}"