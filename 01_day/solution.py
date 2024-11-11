
input_lines = None

def read_input_file(filepath: str) -> list:
    with open(filepath, "r") as ifile:
        input_lines = ifile.readlines()

    return [line.strip() for line in input_lines]


def sliding_window(window_size: int = 1) -> int:

    increase_n = 0
    previous_measurement = -1

    for window_index in range(0, len(input_lines)):
    
        measurement = 0
        for w_index in range(0, window_size - 1):
            measurement += int(input_lines[window_index + w_index])

        print(f"Window {window_index} = {measurement}")

        if measurement > previous_measurement and previous_measurement != -1:
            increase_n += 1

        previous_measurement = measurement

    return increase_n



if __name__ == "__main__":
    input_lines = read_input_file("example_1.txt")
    
    result = sliding_window(3)

    print(f"Number if increases: {result}")
