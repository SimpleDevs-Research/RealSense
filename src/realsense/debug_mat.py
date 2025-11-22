import argparse
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import sys

def load_mat(path):
    try:
        data = scipy.io.loadmat(path, squeeze_me=True, struct_as_record=False)
    except Exception as e:
        print(f"Failed to load MAT file: {e}")
        sys.exit(1)

    # remove MATLAB metadata entries
    data = {k: v for k, v in data.items() if not k.startswith("__")}
    return data


def describe_variable(name, value):
    """Produce a human-readable description of a variable."""
    dtype = type(value).__name__

    if isinstance(value, np.ndarray):
        return f"{name}: ndarray, shape={value.shape}, dtype={value.dtype}"

    elif hasattr(value, "__dict__"):  # MATLAB struct -> simple object
        fields = list(value.__dict__.keys())
        return f"{name}: struct with fields {fields}"

    else:
        return f"{name}: {dtype}"


def show_variable(name, value):
    """Display variable details or visualization."""
    print("\n=== Variable: {} ===".format(name))

    if isinstance(value, np.ndarray):
        print("Shape:", value.shape)
        print("Dtype:", value.dtype)

        # Try visualizing array if 2D or 3D
        if value.ndim == 2:
            plt.imshow(value)
            plt.title(name)
            plt.colorbar()
            plt.show()

        elif value.ndim == 3 and value.shape[2] in (3, 4):
            plt.imshow(value.astype(np.uint8))
            plt.title(name)
            plt.show()

        else:
            print(value)

    elif hasattr(value, "__dict__"):  # MATLAB struct
        print("Fields:")
        for f in value.__dict__.keys():
            print("  -", f)

    else:
        print(value)


def main():
    parser = argparse.ArgumentParser(description="Simple .mat Viewer")
    parser.add_argument("mat_file", help="Path to MAT file")
    args = parser.parse_args()

    data = load_mat(args.mat_file)

    print("\nLoaded variables:")
    for name, value in data.items():
        print(" ", describe_variable(name, value))

    # Interactive prompt
    while True:
        choice = input("\nEnter variable name to view (or 'q' to quit): ").strip()

        if choice.lower() == "q":
            break

        if choice not in data:
            print("Variable not found.")
            continue

        show_variable(choice, data[choice])


if __name__ == "__main__":
    main()